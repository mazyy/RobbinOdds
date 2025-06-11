from scrapers.odds_scraper.odds_scraper.spiders.odds_portal.base_spider import BaseSpider
from scrapers.odds_scraper.odds_scraper.spiders.odds_portal.parser import decrypt_data_PBKDF2HMAC
from scrapers.odds_scraper.odds_scraper.spiders.odds_portal.utils.league_results_parser import parse_league_results_page
import scrapy
import json
import re
import time
from urllib.parse import urljoin

class LeagueResultsSpider(BaseSpider):
    """Spider for scraping league results with pagination"""
    name = "oddsportal_league_results_spider"
    allowed_domains = ["oddsportal.com"]
    
    custom_settings = {
        'CONCURRENT_REQUESTS': 2,
        'DOWNLOAD_DELAY': 2.0,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1.5,
        'AUTOTHROTTLE_MAX_DELAY': 5,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 2.0,
    }
    
    def __init__(self, league_url: str = None, season: str = None, 
                 max_pages: int = None, start_page: int = 1, **kwargs):
        """
        Initialize league results spider.
        
        Args:
            league_url: League URL (e.g., https://www.oddsportal.com/basketball/usa/nba/)
            season: Optional season (e.g., "2023-2024"). If not provided, scrapes current season
            max_pages: Maximum number of pages to scrape (optional)
            start_page: Starting page number (default: 1)
        """
        super().__init__(**kwargs)
        
        if not league_url:
            raise ValueError("league_url parameter is required")
        
        self.league_url = league_url.rstrip('/')
        self.season = season
        self.max_pages = int(max_pages) if max_pages else None
        self.start_page = int(start_page)
        
        # Extract sport and league info from URL
        url_parts = self.league_url.split('/')
        self.sport_name = url_parts[-3] if len(url_parts) >= 3 else 'unknown'
        self.country_name = url_parts[-2] if len(url_parts) >= 2 else 'unknown'
        self.league_name = url_parts[-1] if url_parts else 'unknown'
        
        # Construct results URL
        if season:
            # Historical season: /basketball/usa/nba-2023-2024/results/
            self.results_url = f"{self.league_url}-{season}/results/"
        else:
            # Current season: /basketball/usa/nba/results/
            self.results_url = f"{self.league_url}/results/"
        
        self.start_urls = [self.results_url]
        
        # Store tournament info as we discover it
        self.tournament_info = {
            'encoded_tournament_id': None,
            'numeric_tournament_id': None,
            'sport_id': None,
            'tournament_name': self.league_name.upper(),
            'season': season or 'current'
        }
    
    def parse_items(self, response):
        """Parse the results page to extract tournament data and setup AJAX calls"""
        
        self.logger.info(f"Parsing results page: {response.url}")
        
        # Extract encoded tournament ID from pageOutrightsVar
        script_text = response.xpath('//script[contains(text(), "pageOutrightsVar")]/text()').get()
        if not script_text:
            # Try alternative patterns
            script_text = response.xpath('//script[contains(text(), "var pageVar")]/text()').get()
        
        if script_text:
            # Try multiple patterns
            patterns = [
                r'var\s+pageOutrightsVar\s*=\s*\'({.*?})\'',
                r'var\s+pageVar\s*=\s*\'({.*?})\'',
                r'"id"\s*:\s*"([^"]+)".*?"sid"\s*:\s*(\d+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, script_text, re.DOTALL)
                if match:
                    if pattern == patterns[2]:
                        # Direct extraction
                        self.tournament_info['encoded_tournament_id'] = match.group(1)
                        self.tournament_info['sport_id'] = int(match.group(2))
                    else:
                        # JSON parsing
                        try:
                            page_data = json.loads(match.group(1))
                            self.tournament_info['encoded_tournament_id'] = page_data.get('id')
                            self.tournament_info['sport_id'] = page_data.get('sid', 1)
                            break
                        except json.JSONDecodeError:
                            continue
        
        if not self.tournament_info['encoded_tournament_id']:
            self.logger.error("Failed to extract encoded tournament ID")
            return
        
        self.logger.info(f"Found tournament: {self.tournament_info['encoded_tournament_id']}, "
                        f"sport: {self.tournament_info['sport_id']}")
        
        # Extract numeric tournament ID from ajax URLs
        tournament_id_patterns = [
            r'/ajax-sport-country-tournament-archive_/\d+/[^/]+/([^/]+)/',  # From main AJAX URL
            r'/t/(\d+)/',  # From user-data URL
            r'"tid"\s*:\s*(\d+)',  # From inline scripts
        ]
        
        # Search in scripts
        all_scripts = response.xpath('//script/text()').getall()
        for script in all_scripts:
            for pattern in tournament_id_patterns:
                match = re.search(pattern, script)
                if match:
                    # The third segment in AJAX URL is the bookiehash/numeric ID combo
                    if '/' in pattern and 'archive_' in pattern:
                        # This might be the bookiehash, skip
                        continue
                    potential_id = match.group(1)
                    if potential_id.isdigit():
                        self.tournament_info['numeric_tournament_id'] = potential_id
                        break
            if self.tournament_info['numeric_tournament_id']:
                break
        
        # Extract the AJAX endpoint pattern
        ajax_pattern = re.search(
            r'/ajax-sport-country-tournament-archive_/(\d+)/([^/]+)/([^/]+)/',
            response.text
        )
        
        if ajax_pattern:
            sport_id = ajax_pattern.group(1)
            encoded_id = ajax_pattern.group(2)
            bookiehash = ajax_pattern.group(3)
            
            self.logger.info(f"Found AJAX pattern - sport: {sport_id}, "
                           f"encoded_id: {encoded_id}, bookiehash: {bookiehash}")
            
            # Start scraping from the specified page
            yield from self._request_page(
                sport_id=sport_id,
                encoded_id=encoded_id,
                bookiehash=bookiehash,
                page=self.start_page,
                referer=response.url
            )
        else:
            self.logger.error("Failed to find AJAX endpoint pattern")
    
    def _request_page(self, sport_id: str, encoded_id: str, bookiehash: str, 
                     page: int, referer: str):
        """Request a specific page of results"""
        
        # Check if we've reached max pages
        if self.max_pages and page > self.start_page + self.max_pages - 1:
            self.logger.info(f"Reached maximum pages limit ({self.max_pages})")
            return
        
        # Build AJAX URL
        ajax_base = f"/ajax-sport-country-tournament-archive_/{sport_id}/{encoded_id}/{bookiehash}"
        timestamp = int(time.time() * 1000)
        
        # Timezone offset (using 3.5 as default, you might want to make this configurable)
        timezone = "3.5"
        
        ajax_url = f"https://www.oddsportal.com{ajax_base}/{page}/{timezone}/?_={timestamp}"
        
        self.logger.info(f"Requesting page {page}: {ajax_url}")
        
        yield scrapy.Request(
            url=ajax_url,
            callback=self.parse_ajax_results,
            headers={
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': referer,
                'Accept': 'application/json, text/plain, */*'
            },
            meta={
                'page': page,
                'sport_id': sport_id,
                'encoded_id': encoded_id,
                'bookiehash': bookiehash,
                'referer': referer
            },
            errback=self.handle_ajax_error
        )
    
    def parse_ajax_results(self, response):
        """Parse AJAX response containing match results"""
        
        meta = response.meta
        current_page = meta['page']
        
        self.logger.info(f"Parsing AJAX response for page {current_page}, status: {response.status}")
        
        if response.status != 200:
            self.logger.error(f"Failed to fetch page {current_page}: HTTP {response.status}")
            return
        
        # Decrypt response
        encrypted_data = response.text.strip()
        if not encrypted_data:
            self.logger.error("Empty response received")
            return
        
        try:
            decrypted_data = decrypt_data_PBKDF2HMAC(encrypted_data)
            if not decrypted_data:
                self.logger.error("Failed to decrypt response")
                return
        except Exception as e:
            self.logger.error(f"Decryption error: {e}")
            return
        
        # Parse the results page
        try:
            page_item = parse_league_results_page(
                response_data=decrypted_data,
                tournament_id=self.tournament_info['numeric_tournament_id'],
                tournament_name=self.tournament_info['tournament_name'],
                season=self.tournament_info['season']
            )
            
            # Yield the entire page item
            yield page_item
            
            # Also yield individual matches if you want them separately
            for match in page_item.get('matches', []):
                yield match
            
            # Log summary
            total_matches = len(page_item.get('matches', []))
            self.logger.info(f"Page {current_page}: Found {total_matches} matches")
            
            # Check for pagination
            if page_item.get('has_next_page'):
                # Request next page
                yield from self._request_page(
                    sport_id=meta['sport_id'],
                    encoded_id=meta['encoded_id'],
                    bookiehash=meta['bookiehash'],
                    page=current_page + 1,
                    referer=meta['referer']
                )
            else:
                self.logger.info(f"Reached last page ({current_page})")
                
        except Exception as e:
            self.logger.error(f"Error parsing results page: {e}")
            self.logger.exception("Full traceback:")
    
    def handle_ajax_error(self, failure):
        """Handle errors when fetching AJAX pages"""
        request = failure.request
        meta = request.meta
        
        self.logger.error(f"Error fetching page {meta.get('page')}: {failure.value}")
        
        # You could implement retry logic here if needed
    
    def parse_next_link(self, response):
        """No pagination needed - handled via AJAX"""
        return []