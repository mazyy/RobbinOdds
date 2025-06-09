from .base_spider import BaseSpider
from odds_scraper.items.odds_portal.items import HeaderLoader, BodyLoader, PageVarLoader
from .parser import MATCH_EVENT_REACT_HEADER_COMPONENT_XPATH, PAGE_VAR_XPATH, PAGE_VAR_KEYS_DICT,\
    EVENT_HEADERS_KEYS_DICT, EVENT_BODY_KEYS_DICT, load_json_str, add_json_value_to_itemloader, \
    extract_pagevar_data
import scrapy

class MatchSpider(BaseSpider):
    """Spider for scraping match metadata - runs once per match"""
    name = "oddsportal_match_spider"
    allowed_domains = ["oddsportal.com"]
    
    # Custom settings for rate limiting
    custom_settings = {
        'CONCURRENT_REQUESTS': 4,
        'DOWNLOAD_DELAY': 1.0,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
    }
    
    def __init__(self, match_url: str = None, **kwargs):
        super().__init__(**kwargs)
        if not match_url:
            raise ValueError("Provide match_url parameter")
        
        self.match_url = match_url
        self.start_urls = [match_url]
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
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
        
        # Add the match URL to header for reference
        event_header_item['match_url'] = self.match_url

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

        # Log available markets for reference
        nav_filtered = page_var_item.get('nav_filtered', {})
        if nav_filtered:
            self.logger.info(f"Match {event_header_item.get('match_id')} has available bet types: {list(nav_filtered.keys())}")
            for bet_type, scopes in nav_filtered.items():
                if isinstance(scopes, dict):
                    self.logger.info(f"  Bet type {bet_type} has scopes: {list(scopes.keys())}")

    def parse_next_link(self, response):
        """No pagination needed for individual match pages"""
        return []