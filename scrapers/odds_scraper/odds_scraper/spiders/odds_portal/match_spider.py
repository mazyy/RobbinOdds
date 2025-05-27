# odds_scraper/odds_scraper/spiders/odds_portal/match_spider.py
from .base_spider import BaseSpider
from odds_scraper.items.odds_portal.items import MatchItem, OddsItem, \
    HeaderLoader, BodyLoader, PageVarLoader
from .parser import MATCH_EVENT_REACT_HEADER_COMPONENT_XPATH, PAGE_VAR_XPATH, PAGE_VAR_KEYS_DICT,\
    EVENT_HEADERS_KEYS_DICT, EVENT_BODY_KEYS_DICT, load_json_str, add_json_value_to_itemloader, extract_pagevar_data
import urllib.parse

class MatchSpider(BaseSpider):
    name = "oddsportal_match_spider"
    allowed_domains = ["oddsportal.com"]
    # we’ll pass `start_url` via -a on the CLI
    def __init__(self, match_url=None, **kwargs):
        super().__init__(**kwargs)
        if not match_url:
            raise ValueError("Provide match_url parameter")
        self.match_url = match_url
        self.start_urls = [match_url]
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
        # --- parse header and body ---
        react_header_str = response.xpath(MATCH_EVENT_REACT_HEADER_COMPONENT_XPATH).get()
        react_header_json = load_json_str(react_header_str)
        event = react_header_json.get('eventData', {})
        body = react_header_json.get('eventBody', {})     
        
        header_loader = HeaderLoader()
        body_loader = BodyLoader()

        header_loader = add_json_value_to_itemloader(header_loader, event, keymaps=EVENT_HEADERS_KEYS_DICT)
        body_loader = add_json_value_to_itemloader(body_loader, body, keymaps=EVENT_BODY_KEYS_DICT)
        body_loader = add_json_value_to_itemloader(body_loader, react_header_json, keymaps=EVENT_BODY_KEYS_DICT)

        event_header_item = header_loader.load_item()
        event_body_item = body_loader.load_item()

        yield event_header_item
        yield event_body_item

        # --- parse pageVar ---
        page_var_json = extract_pagevar_data(response, PAGE_VAR_XPATH)
        default_settings = event = page_var_json.get('default_settings', {})

        page_var_loader = PageVarLoader()
        page_var_loader = add_json_value_to_itemloader(page_var_loader, default_settings, keymaps=PAGE_VAR_KEYS_DICT)
        page_var_loader = add_json_value_to_itemloader(page_var_loader, page_var_json, keymaps=PAGE_VAR_KEYS_DICT)
        
        page_var_item = page_var_loader.load_item()
        yield page_var_item

        # --- parse odds ---
        # /match-event/{betType}-{scope}-{xhashf}.dat
        domain_name = "https://www.oddsportal.com"
        unhashedf = urllib.parse.unquote(event_header_item['xhashf'])
        for k, v in page_var_item['nav_filtered'].items():
            print(k, v.keys())

    def parse_next_links(self, response):
        # if you want to follow inplay odds:
        return []
