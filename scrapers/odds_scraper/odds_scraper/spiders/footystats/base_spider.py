import scrapy
import json
from abc import abstractmethod
from typing import Dict, Any, Iterator, Optional
from urllib.parse import urlencode

class FootyStatsBaseSpider(scrapy.Spider):
    """Base spider for all FootyStats API endpoints"""
    
    endpoint_name = None
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1.5,
        'AUTOTHROTTLE_MAX_DELAY': 5,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 2.0,
        'CONCURRENT_REQUESTS': 2,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 408, 429],
    }
    
    def __init__(self, api_key: str = "example", **kwargs):
        super().__init__(**kwargs)
        
        if not self.endpoint_name:
            raise ValueError(f"{self.__class__.__name__} must set endpoint_name")
        
        self.api_key = api_key
        self.base_url = "https://api.football-data-api.com"
        
        self.stats = {
            'requests_made': 0,
            'successful_responses': 0,
            'failed_responses': 0,
            'items_processed': 0,
            'items_yielded': 0,
            'pagination_requests': 0
        }
        
        self.logger.info(f"{self.name} initialized with {'test' if api_key == 'example' else 'production'} key")
    
    def start_requests(self) -> Iterator[scrapy.Request]:
        params = self.get_request_params()
        params['key'] = self.api_key
        
        url = f"{self.base_url}/{self.endpoint_name}?{urlencode(params)}"
        
        self.logger.info(f"Starting {self.endpoint_name} request")
        self.stats['requests_made'] += 1
        
        yield scrapy.Request(
            url=url,
            callback=self.parse_response,
            errback=self.handle_error,
            meta={
                'endpoint': self.endpoint_name,
                'page': params.get('page', 1),
                'is_pagination': False
            }
        )
    
    def get_request_params(self) -> Dict[str, Any]:
        """Override in child spiders to add specific parameters"""
        return {}
    
    def parse_response(self, response) -> Iterator:
        meta = response.meta
        page = meta.get('page', 1)
        
        self.logger.info(f"Parsing {self.endpoint_name} response (page {page}), status: {response.status}")
        
        if response.status != 200:
            self.logger.error(f"HTTP {response.status} for {self.endpoint_name}")
            self.stats['failed_responses'] += 1
            return
        
        try:
            data = json.loads(response.text)
            
            if not self.validate_api_response(data):
                self.stats['failed_responses'] += 1
                return
            
            self.stats['successful_responses'] += 1
            self.log_api_metadata(data, page)
            
            # Handle both list and single object responses
            data_items = data.get('data', [])
            
            # Check if data is a list or single object
            if isinstance(data_items, list):
                # Standard case: array of items
                self.logger.info(f"Processing {len(data_items)} items from {self.endpoint_name}")
                
                for item_data in data_items:
                    self.stats['items_processed'] += 1
                    
                    try:
                        item = self.parse_data_item(item_data)
                        if item:
                            self.stats['items_yielded'] += 1
                            yield item
                    except Exception as e:
                        self.logger.error(f"Error parsing item: {e}")
                        continue
                
                # Handle pagination for list responses
                yield from self.handle_pagination(data, response)
                
            elif isinstance(data_items, dict):
                # Special case: single object (like match endpoint)
                self.logger.info(f"Processing single object from {self.endpoint_name}")
                self.stats['items_processed'] += 1
                
                try:
                    item = self.parse_data_item(data_items)
                    if item:
                        self.stats['items_yielded'] += 1
                        yield item
                except Exception as e:
                    self.logger.error(f"Error parsing single object: {e}")
                    
                # No pagination for single object responses
                
            else:
                self.logger.error(f"Unexpected data type: {type(data_items)}. Expected list or dict.")
                self.stats['failed_responses'] += 1
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON response: {e}")
            self.stats['failed_responses'] += 1
        except Exception as e:
            self.logger.error(f"Error parsing response: {e}")
            self.stats['failed_responses'] += 1
    
    def validate_api_response(self, data: Dict[str, Any]) -> bool:
        if not isinstance(data, dict):
            self.logger.error("Response is not a JSON object")
            return False
        
        if not data.get('success', False):
            self.logger.error(f"API returned success=false: {data.get('message', 'No message')}")
            return False
        
        if 'data' not in data:
            self.logger.error("Response missing 'data' field")
            return False
        
        # Accept both list and dict for data field
        data_field = data['data']
        if not isinstance(data_field, (list, dict)):
            self.logger.error(f"Response 'data' field is neither list nor dict: {type(data_field)}")
            return False
        
        return True
    
    def log_api_metadata(self, data: Dict[str, Any], page: int):
        pager = data.get('pager', {})
        if pager:
            current_page = pager.get('current_page', page)
            max_page = pager.get('max_page', 1)
            total_results = pager.get('total_results', 0)
            self.logger.info(f"Page {current_page}/{max_page}, Total results: {total_results}")
        
        metadata = data.get('metadata', {})
        if metadata:
            remaining = metadata.get('request_remaining')
            if remaining is not None:
                self.logger.info(f"API requests remaining: {remaining}")
    
    def handle_pagination(self, data: Dict[str, Any], response) -> Iterator[scrapy.Request]:
        """Only handle pagination for list responses"""
        pager = data.get('pager', {})
        if not pager:
            return
        
        current_page = pager.get('current_page', 1)
        max_page = pager.get('max_page', 1)
        
        if current_page < max_page:
            next_page = current_page + 1
            
            params = self.get_request_params()
            params['key'] = self.api_key
            params['page'] = next_page
            
            url = f"{self.base_url}/{self.endpoint_name}?{urlencode(params)}"
            
            self.logger.info(f"Requesting next page {next_page}/{max_page}")
            self.stats['requests_made'] += 1
            self.stats['pagination_requests'] += 1
            
            yield scrapy.Request(
                url=url,
                callback=self.parse_response,
                errback=self.handle_error,
                meta={
                    'endpoint': self.endpoint_name,
                    'page': next_page,
                    'is_pagination': True
                }
            )
    
    @abstractmethod
    def parse_data_item(self, item_data: Dict[str, Any]):
        """Parse individual data item from API response"""
        raise NotImplementedError("Child spiders must implement parse_data_item()")
    
    def handle_error(self, failure):
        request = failure.request
        meta = request.meta
        endpoint = meta.get('endpoint', 'unknown')
        page = meta.get('page', 1)
        
        self.logger.error(f"Request failed for {endpoint} (page {page}): {failure.value}")
        self.stats['failed_responses'] += 1
        
        if failure.check(scrapy.exceptions.HttpError):
            response = failure.value.response
            if response.status == 401:
                self.logger.error("Authentication failed - check API key")
            elif response.status == 403:
                self.logger.error("Access forbidden - check subscription")
            elif response.status == 429:
                self.logger.error("Rate limit exceeded - will retry automatically")
        
        elif failure.check(scrapy.exceptions.TimeoutError):
            self.logger.error("Request timeout")
        
        elif failure.check(scrapy.exceptions.DNSLookupError):
            self.logger.error("DNS lookup failed")
    
    def closed(self, reason):
        self.logger.info(f"{self.name} closed: {reason}")
        self.logger.info("FINAL STATISTICS:")
        self.logger.info(f"   Requests made: {self.stats['requests_made']}")
        self.logger.info(f"   Successful responses: {self.stats['successful_responses']}")
        self.logger.info(f"   Failed responses: {self.stats['failed_responses']}")
        self.logger.info(f"   Items processed: {self.stats['items_processed']}")
        self.logger.info(f"   Items yielded: {self.stats['items_yielded']}")
        self.logger.info(f"   Pagination requests: {self.stats['pagination_requests']}")
        
        if self.stats['requests_made'] > 0:
            success_rate = (self.stats['successful_responses'] / self.stats['requests_made']) * 100
            self.logger.info(f"   Success rate: {success_rate:.1f}%")
        
        if self.stats['items_processed'] > 0:
            yield_rate = (self.stats['items_yielded'] / self.stats['items_processed']) * 100
            self.logger.info(f"   Item yield rate: {yield_rate:.1f}%")