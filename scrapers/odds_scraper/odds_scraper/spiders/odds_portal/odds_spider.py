from .base_spider import BaseSpider
from .parser import decrypt_data_PBKDF2HMAC
from .utils.match_event_parser import parse_match_event_odds
from .utils.default_mappings import DEFAULT_MAPPINGS
import urllib.parse
import scrapy
import json

class OddsSpider(BaseSpider):
    """Spider for scraping odds data - focused on directly fetching odds endpoints"""
    name = "oddsportal_odds_spider"
    allowed_domains = ["oddsportal.com"]
    
    # Custom settings for rate limiting
    custom_settings = {
        'CONCURRENT_REQUESTS': 2,
        'DOWNLOAD_DELAY': 1.5,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 5,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 2.0,
        'AUTOTHROTTLE_DEBUG': True,
    }
    
    def __init__(self, match_url: str = None, match_id: str = None, 
                 xhashf: str = None, sport_id: str = None,
                 version_id: str = None, bet_types: str = None, 
                 scopes: str = None, is_started: str = None,
                 bookmaker_names: str = None, betting_type_names: str = None,
                 scope_names: str = None, handicap_names: str = None, **kwargs):
        """
        Initialize odds spider with direct parameters.
        
        Args:
            match_url: Match URL (for referer header)
            match_id: Match ID 
            xhashf: URL-encoded xhash
            sport_id: Sport ID
            version_id: Version ID (default: "1")
            bet_types: Comma-separated bet type IDs to scrape
            scopes: Comma-separated scope IDs to scrape
            is_started: Whether match has started ("true"/"false")
            bookmaker_names: JSON string of bookmaker ID to name mappings
            betting_type_names: JSON string of betting type mappings
            scope_names: JSON string of scope ID to name mappings
            handicap_names: JSON string of handicap mappings
        """
        super().__init__(**kwargs)
        
        # Validate required parameters
        if not all([match_url, match_id, xhashf, sport_id]):
            raise ValueError("Required parameters: match_url, match_id, xhashf, sport_id")
        
        self.domain_name = "https://www.oddsportal.com"
        self.match_url = match_url
        self.match_id = match_id
        self.xhashf = xhashf
        self.sport_id = sport_id
        self.version_id = version_id or "1"
        
        # Parse boolean
        self.is_started = is_started.lower() == "true" if is_started else False
        
        # Parse betting types and scopes
        self.selected_bet_types = bet_types.split(',') if bet_types else ['1']
        self.selected_scopes = scopes.split(',') if scopes else ['2']
        
        # Parse mappings or use defaults
        self.bookmaker_names_map = self._parse_mapping(bookmaker_names, 'bookmaker_names')
        self.betting_type_names_map = self._parse_mapping(betting_type_names, 'betting_type_names')
        self.scope_names_map = self._parse_mapping(scope_names, 'scope_names')
        self.handicap_names_map = self._parse_mapping(handicap_names, 'handicap_names')
        
        # Headers for API requests
        self.endpoint_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Referer': self.match_url,
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        # Start URLs will be generated in start_requests
        self.start_urls = []
    
    def _parse_mapping(self, mapping_str, mapping_name):
        """Parse mapping from JSON string or use default"""
        if mapping_str:
            try:
                return json.loads(mapping_str)
            except json.JSONDecodeError:
                self.logger.warning(f"Failed to parse {mapping_name}, using defaults")
                return DEFAULT_MAPPINGS.get(mapping_name, {})
        return DEFAULT_MAPPINGS.get(mapping_name, {})

    def start_requests(self):
        """Generate requests for odds endpoints based on selected bet types and scopes"""
        # Decode the URL-encoded hash
        xhash = urllib.parse.unquote(self.xhashf)
        self.logger.info(f"Using decoded xhash: {xhash} (from {self.xhashf})")
        
        # Generate requests for all combinations of bet types and scopes
        for bet_type in self.selected_bet_types:
            for scope in self.selected_scopes:
                # Pattern: /match-event/{version}-{sportId}-{eventId}-{betTypeId}-{scopeId}-{xhash}.dat
                endpoint = f"{self.domain_name}/match-event/{self.version_id}-{self.sport_id}-{self.match_id}-{bet_type}-{scope}-{xhash}.dat"
                endpoint += "?_="  # Empty timestamp parameter
                
                self.logger.info(f"Requesting odds for bet_type={bet_type}, scope={scope}: {endpoint}")
                
                yield scrapy.Request(
                    url=endpoint,
                    headers=self.endpoint_headers,
                    callback=self.parse_odds,
                    errback=self.handle_odds_error,
                    meta={
                        'bet_type': bet_type,
                        'scope': scope,
                        'endpoint': endpoint,
                    }
                )

    def parse_items(self, response):
        """Not used - start_requests generates the requests directly"""
        pass

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

            # Parse the odds with provided mappings
            parsed_odds = parse_match_event_odds(
                odds_response=decrypted_data,
                match_id=self.match_id,
                bookmaker_names=self.bookmaker_names_map,
                betting_type_names=self.betting_type_names_map,
                scope_names=self.scope_names_map,
                handicap_names=self.handicap_names_map,
                is_started=self.is_started
            )

            yield parsed_odds

        except Exception as e:
            self.logger.error(f"Error processing odds data: {type(e).__name__}: {str(e)}")
            self.logger.exception("Full traceback:")

    def handle_odds_error(self, failure):
        """Handle errors when fetching odds"""
        request = failure.request
        meta = request.meta
        
        self.logger.error(f"Error fetching odds for bet_type={meta.get('bet_type')}, scope={meta.get('scope')}: {failure.value}")

    def parse_next_link(self, response):
        """No pagination needed for odds endpoints"""
        return []