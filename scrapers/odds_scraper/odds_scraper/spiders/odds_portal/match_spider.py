# odds_scraper/odds_scraper/spiders/odds_portal/match_spider.py
from .base_spider import BaseSpider
from odds_scraper.items.odds_portal.items import MatchItem, OddsItem, \
    HeaderLoader, BodyLoader, PageVarLoader
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
        
        # Parse betting types and scopes from command line
        self.selected_bet_types = bet_types.split(',') if bet_types else None
        self.selected_scopes = scopes.split(',') if scopes else None
        
        # For now, if nothing specified, default to 1X2 fulltime
        if not self.selected_bet_types:
            self.selected_bet_types = ['1'] # 1X2
        
        if not self.selected_scopes:
            self.selected_scopes = ['2']    # Full Time
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        self.endpoint_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Referer': self.match_url,
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        # Store collected data
        self.collected_data = {
            'event_header': None,
            'event_body': None,
            'page_var': None,
            'odds_data': {}
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
        
        # Store for later use
        self.collected_data['event_header'] = dict(event_header_item)
        self.collected_data['event_body'] = dict(event_body_item)

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
        self.collected_data['page_var'] = dict(page_var_item)
        
        yield page_var_item

        # --- Generate odds requests ---
        # IMPORTANT: We need to yield from the generator
        for request in self.generate_odds_requests(event_header_item, page_var_item):
            yield request

    def generate_odds_requests(self, event_header: Dict, page_var: Dict):
        """Generate requests for odds endpoints based on selected bet types and scopes"""
        domain_name = "https://www.oddsportal.com"
        
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
        
        # Priority order for bet types (if no specific selection)
        priority_bet_types = ['1', '2', '5', '4', '13', '3', '6', '12', '7', '8', '9', '10']
        
        request_count = 0
        
        for bet_type_key, bet_type_scopes in nav_filtered.items():
            # Skip if not in selected types (if provided)
            if self.selected_bet_types and bet_type_key not in self.selected_bet_types:
                continue
            
            # Skip non-priority types if no specific selection and we already have enough requests
            if not self.selected_bet_types and bet_type_key not in priority_bet_types[:5] and request_count > 10:
                self.logger.info(f"Skipping non-priority bet type: {bet_type_key}")
                continue
            
            if isinstance(bet_type_scopes, dict):
                for scope_key, scope_value in bet_type_scopes.items():
                    # Skip if not in selected scopes (if provided)
                    if self.selected_scopes and scope_key not in self.selected_scopes:
                        continue
                    
                    # Construct endpoint
                    # Pattern: /match-event/{version}-{sportId}-{eventId}-{betTypeId}-{scopeId}-{xhash}.dat
                    endpoint = f"{domain_name}/match-event/{version_id}-{sport_id}-{event_id}-{bet_type_key}-{scope_key}-{xhash}.dat"
                    
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
                        },
                        dont_filter=True,
                        priority=10 if bet_type_key in priority_bet_types[:3] else 5
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
            
            # Store the decrypted data
            odds_key = f"{bet_type}_{scope}"
            self.collected_data['odds_data'][odds_key] = {
                'bet_type': bet_type,
                'scope': scope,
                'data': decrypted_data,
                'endpoint': meta.get('endpoint')
            }
            
            # Log some details about the data structure
            if isinstance(decrypted_data, dict):
                self.logger.info(f"Decrypted data keys: {list(decrypted_data.keys())[:10]}")  # First 10 keys
                
                # Check for common keys
                if 'back' in decrypted_data:
                    self.logger.info(f"Found 'back' data with {len(decrypted_data['back'])} entries")
                if 'lay' in decrypted_data:
                    self.logger.info(f"Found 'lay' data with {len(decrypted_data['lay'])} entries")
                if 'history' in decrypted_data:
                    self.logger.info("Found historical odds data")
            
            # For now, just yield the raw decrypted data
            # Later you can process this into proper OddsItem objects
            yield {
                'type': 'odds_data',
                'bet_type': bet_type,
                'scope': scope,
                'match_id': self.collected_data['event_header'].get('match_id'),
                'sport_id': self.collected_data['event_header'].get('sport_id'),
                'tournament': self.collected_data['event_header'].get('tournament_name'),
                'home': self.collected_data['event_header'].get('home'),
                'away': self.collected_data['event_header'].get('away'),
                'data': decrypted_data
            }
            
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

    def parse_next_link(self, response):
        """Override the typo in base class"""
        return self.parse_next_links(response)
        
    def parse_next_links(self, response):
        """For match spider, we typically don't follow links"""
        return []

    def closed(self, reason):
        """Called when spider closes"""
        self.logger.info(f"Spider closed: {reason}")
        self.logger.info(f"Collected odds data for {len(self.collected_data['odds_data'])} bet type/scope combinations")
        
        # Summary of collected data
        for odds_key, odds_data in self.collected_data['odds_data'].items():
            self.logger.info(f"  - {odds_key}: {odds_data['bet_type']} / {odds_data['scope']}")