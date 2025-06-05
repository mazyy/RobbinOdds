# odds_scraper/odds_scraper/spiders/odds_portal/match_spider.py
from .base_spider import BaseSpider
from odds_scraper.items.odds_portal.items import HeaderLoader, BodyLoader, PageVarLoader
from .parser import MATCH_EVENT_REACT_HEADER_COMPONENT_XPATH, PAGE_VAR_XPATH, PAGE_VAR_KEYS_DICT,\
    EVENT_HEADERS_KEYS_DICT, EVENT_BODY_KEYS_DICT, load_json_str, add_json_value_to_itemloader, \
    extract_pagevar_data, decrypt_data_PBKDF2HMAC
import urllib.parse
import scrapy
import json
from typing import Dict, List, Optional, Any


class MatchSpider(BaseSpider):
    name = "oddsportal_match_spider"
    allowed_domains = ["oddsportal.com"]
    
    # Custom settings for rate limiting
    custom_settings = {
        'CONCURRENT_REQUESTS': 2,
        'DOWNLOAD_DELAY': 1.5,  # 1.5 seconds between requests
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 5,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 2.0,
        'AUTOTHROTTLE_DEBUG': True,  # Enable to see autothrottle stats
    }
    
    def __init__(self, match_url: str = None, bet_types: str = None, scopes: str = None, **kwargs):
        super().__init__(**kwargs)
        if not match_url:
            raise ValueError("Provide match_url parameter")
        
        self.match_url = match_url
        self.start_urls = [match_url]
        self.domain_name = "https://www.oddsportal.com"
        
        # Parse betting types and scopes from command line
        self.selected_bet_types = bet_types.split(',') if bet_types else None
        self.selected_scopes = scopes.split(',') if scopes else None
        
        # For now, if nothing specified, default to 1X2 fulltime
        if not self.selected_bet_types:
            self.selected_bet_types = ['1'] # 1X2
        
        if not self.selected_scopes:
            self.selected_scopes = ['2']    # Full Time
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        
        self.endpoint_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Referer': self.match_url,
            'X-Requested-With': 'XMLHttpRequest'
        }

    def parse_items(self, response):
        """Parse the main page and extract event data"""
        self.logger.info(f"Parsing match page: {response.url}")
        
        # --- Parse header and body ---
        react_header_str = response.xpath(MATCH_EVENT_REACT_HEADER_COMPONENT_XPATH).get()
        if not react_header_str:
            self.logger.error("No React header component found")
            return
            
        react_header_json = load_json_str(react_header_str)
        if not react_header_json:
            self.logger.error("Failed to parse React header JSON")
            return
            
        event = react_header_json.get('eventData', {})
        body = react_header_json.get('eventBody', {})     
        
        # Load items
        header_loader = HeaderLoader()
        body_loader = BodyLoader()

        header_loader = add_json_value_to_itemloader(header_loader, event, keymaps=EVENT_HEADERS_KEYS_DICT)
        body_loader = add_json_value_to_itemloader(body_loader, body, keymaps=EVENT_BODY_KEYS_DICT)
        body_loader = add_json_value_to_itemloader(body_loader, react_header_json, keymaps=EVENT_BODY_KEYS_DICT)

        event_header_item = header_loader.load_item()
        event_body_item = body_loader.load_item()

        # Yield header and body items
        yield event_header_item
        yield event_body_item

        # --- Parse pageVar ---
        page_var_json = extract_pagevar_data(response, PAGE_VAR_XPATH)
        if not page_var_json:
            self.logger.error("Failed to extract pageVar data")
            return
            
        default_settings = page_var_json.get('default_settings', {})

        page_var_loader = PageVarLoader()
        page_var_loader = add_json_value_to_itemloader(page_var_loader, default_settings, keymaps=PAGE_VAR_KEYS_DICT)
        page_var_loader = add_json_value_to_itemloader(page_var_loader, page_var_json, keymaps=PAGE_VAR_KEYS_DICT)
        
        page_var_item = page_var_loader.load_item()
        
        yield page_var_item

        # --- Generate odds requests --
        for request in self.generate_odds_requests(event_header_item, page_var_item):
            yield request

    def generate_odds_requests(self, event_header: Dict, page_var: Dict):
        """Generate requests for odds endpoints based on selected bet types and scopes"""
        # Extract necessary data
        version_id = str(event_header.get('version_id', '1'))  # From header if available, else default to 1
        sport_id = str(event_header.get('sport_id', ''))
        event_id = event_header.get('match_id', '')
        
        # IMPORTANT: Use xhashf and decode it
        xhash_encoded = event_header.get('xhashf', event_header.get('xhash', ''))
        if not xhash_encoded:
            self.logger.error("No xhash found in event header")
            return
            
        # Decode the URL-encoded hash
        xhash = urllib.parse.unquote(xhash_encoded)
        self.logger.info(f"Using decoded xhash: {xhash} (from {xhash_encoded})")
        
        # Get available navigation data
        nav_filtered = page_var.get('nav_filtered', {})
        
        if not nav_filtered:
            self.logger.warning("No nav_filtered data found")
            return
        
        self.logger.info(f"Available bet types: {list(nav_filtered.keys())}")
        
        request_count = 0

        for bet_type_key, bet_type_scopes in nav_filtered.items():

            if isinstance(bet_type_scopes, dict):
                for scope_key, scope_value in bet_type_scopes.items():
                    # Construct endpoint
                    # Pattern: /match-event/{version}-{sportId}-{eventId}-{betTypeId}-{scopeId}-{xhash}.dat
                    if scope_key in self.selected_scopes and bet_type_key in self.selected_bet_types:
                        endpoint = f"{self.domain_name}/match-event/{version_id}-{sport_id}-{event_id}-{bet_type_key}-{scope_key}-{xhash}.dat"
                        
                        # Add query parameters
                        endpoint += "?_="  # Empty timestamp parameter as seen in the requests
                        
                        self.logger.info(f"Requesting odds for bet_type={bet_type_key}, scope={scope_key}: {endpoint}")
                        
                        yield scrapy.Request(
                            url=endpoint,
                            headers=self.endpoint_headers,
                            callback=self.parse_odds,
                            errback=self.handle_odds_error,
                            meta={
                                'bet_type': bet_type_key,
                                'scope': scope_key,
                                'endpoint': endpoint,
                            }
                        )
                        
                        request_count += 1

    def parse_odds(self, response):
        """Parse the odds data from the endpoint"""
        meta = response.meta
        bet_type = meta.get('bet_type')
        scope = meta.get('scope')
        
        self.logger.info(f"Parsing odds response for bet_type={bet_type}, scope={scope}, status={response.status}")
        
        if response.status != 200:
            self.logger.error(f"Failed to fetch odds: HTTP {response.status}")
            return
        
        try:
            # Get the raw response text
            encrypted_data = response.text.strip()
            
            if not encrypted_data:
                self.logger.error("Empty response received")
                return
            
            # Decrypt the data
            self.logger.debug(f"Attempting to decrypt data of length: {len(encrypted_data)}")
            decrypted_data = decrypt_data_PBKDF2HMAC(encrypted_data)
            
            if not decrypted_data:
                self.logger.error("Failed to decrypt odds data")
                return
            
            self.logger.info(f"Successfully decrypted odds data for bet_type={bet_type}, scope={scope}")
            
            yield decrypted_data

        except Exception as e:
            self.logger.error(f"Error processing odds data: {type(e).__name__}: {str(e)}")
            self.logger.exception("Full traceback:")

    def handle_odds_error(self, failure):
        """Handle errors when fetching odds"""
        request = failure.request
        meta = request.meta
        
        self.logger.error(f"Error fetching odds for bet_type={meta.get('bet_type')}, scope={meta.get('scope')}: {failure.value}")
        
        # You could implement retry logic here if needed
        # For now, just log the error