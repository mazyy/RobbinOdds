from odds_scraper.spiders.odds_portal.base_spider import BaseSpider
from odds_scraper.spiders.odds_portal.parser import decrypt_data_PBKDF2HMAC
from odds_scraper.spiders.odds_portal.utils.season_matches_parser import parse_season_matches
from odds_scraper.items.odds_portal.league_items import (
    MatchInfoItem, SeasonMatchesItem, MatchInfoLoader, SeasonMatchesLoader
)
import scrapy
import json
import re
import time
from urllib.parse import urlparse, parse_qs
from datetime import datetime

class SeasonSpider(BaseSpider):
    """Spider for extracting match lists from seasons"""
    name = "oddsportal_season_spider"
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
    
    def __init__(self, league_id: str = None, season_id: str = None, 
                 season_url: str = None, sport_id: str = None,
                 mode: str = "results", max_pages: int = None, 
                 start_page: int = 1, league_name: str = None,
                 sport_name: str = None, country_name: str = None, **kwargs):
        """
        Initialize season spider.
        
        Args:
            league_id: Encoded league ID from discovery
            season_id: Season identifier (e.g., "2023-2024" or "current")
            season_url: Full URL to season page
            sport_id: Sport ID for AJAX calls
            mode: "results" (past matches) or "fixtures" (upcoming)
            max_pages: Maximum pages to scrape (optional)
            start_page: Starting page number (default: 1)
            league_name: League name for context
            sport_name: Sport name for context
            country_name: Country name for context
        """
        super().__init__(**kwargs)
        
        # Validate required parameters
        if not all([league_id, season_id, season_url, sport_id]):
            raise ValueError("Required parameters: league_id, season_id, season_url, sport_id")
        
        self.league_id = league_id
        self.season_id = season_id
        self.season_url = season_url.rstrip('/')
        self.sport_id = sport_id
        self.mode = mode.lower()
        self.max_pages = int(max_pages) if max_pages else None
        self.start_page = int(start_page)

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # Context info
        self.league_name = league_name or self._extract_from_url(season_url, 'league')
        self.sport_name = sport_name or self._extract_from_url(season_url, 'sport')
        self.country_name = country_name or self._extract_from_url(season_url, 'country')
        
        # Validate mode
        if self.mode not in ["results", "fixtures"]:
            raise ValueError("mode must be 'results' or 'fixtures'")
        
        # Set appropriate start URL based on mode
        if self.mode == "results":
            # For results, always go to /results/ page
            if not self.season_url.endswith('/results/'):
                self.start_urls = [f"{self.season_url}/results/"]
            else:
                self.start_urls = [self.season_url]
        else:  # fixtures mode
            # For fixtures, go to main page without /results/
            base_url = self.season_url.replace('/results/', '')
            self.start_urls = [base_url]
        
        self.logger.info(f"Season spider initialized - Mode: {self.mode}, URL: {self.start_urls[0]}")
        
        # Store AJAX pattern info as we discover it
        self.ajax_info = {}
    
    def _extract_from_url(self, url: str, part: str) -> str:
        """Extract sport, country, or league name from URL"""
        parts = url.rstrip('/').split('/')
        if part == 'sport' and len(parts) >= 4:
            return parts[-4]
        elif part == 'country' and len(parts) >= 3:
            return parts[-3]
        elif part == 'league' and len(parts) >= 2:
            # Handle both "nba" and "nba-2023-2024" formats
            league_part = parts[-2] if '/results' in parts[-1] else parts[-1]
            return league_part.split('-')[0]
        return 'unknown'
    
    def parse_items(self, response):
        """Parse the initial page to extract AJAX endpoint pattern"""
        self.logger.info(f"Parsing {self.mode} page: {response.url}")
        
        if self.mode == "results":
            # For results, extract AJAX pattern from scripts
            yield from self._parse_results_init(response)
        else:
            # For fixtures, extract from pageOutrightsVar and odds request
            yield from self._parse_fixtures_init(response)
    
    def _parse_results_init(self, response):
        """Initialize results extraction"""
        # Method 1: Try to extract from tournament-component
        ajax_pattern = self._extract_ajax_pattern_from_component(response)
        
        # Method 2: If not found, try from pageOutrightsVar
        if not ajax_pattern:
            ajax_pattern = self._extract_ajax_pattern_from_pagevar(response)
        
        # Method 3: Try next-matches component
        if not ajax_pattern:
            ajax_pattern = self._extract_ajax_pattern_from_next_matches(response)
        
        if not ajax_pattern:
            self.logger.error("Failed to find AJAX endpoint pattern for results")
            return
        
        self.ajax_info = ajax_pattern
        
        # Start pagination
        yield from self._request_results_page(
            page=self.start_page,
            referer=response.url
        )
    
    def _extract_ajax_pattern_from_component(self, response):
        """Extract AJAX pattern from tournament-component"""
        # Look for tournament-component
        tournament_component = response.css('tournament-component::attr(:sport-data)').get()
        
        if tournament_component:
            try:
                data = json.loads(tournament_component)
                odds_request = data.get('oddsRequest', {})
                url = odds_request.get('url', '')
                
                # Parse the URL to extract pattern
                # Format: /ajax-sport-country-tournament-archive_/1/jDTEm9zs/
                if '/ajax-sport-country-tournament-archive_/' in url:
                    parts = url.strip('/').split('/')
                    if len(parts) >= 3:
                        return {
                            'sport_id': parts[1],
                            'encoded_id': parts[2],
                            'base_url': f"/ajax-sport-country-tournament-archive_/{parts[1]}/{parts[2]}"
                        }
            except json.JSONDecodeError:
                self.logger.warning("Failed to parse tournament-component data")
        
        return None
    
    def _extract_ajax_pattern_from_pagevar(self, response):
        """Extract pattern from pageOutrightsVar"""
        # Look for pageOutrightsVar script
        pagevar_script = response.xpath('//script[contains(text(), "pageOutrightsVar")]/text()').get()
        
        if pagevar_script:
            # Extract the JSON string
            match = re.search(r'var\s+pageOutrightsVar\s*=\s*\'({.*?})\'', pagevar_script)
            if match:
                try:
                    data = json.loads(match.group(1))
                    return {
                        'sport_id': str(data.get('sid', self.sport_id)),
                        'encoded_id': data.get('id', self.league_id),
                        'base_url': f"/ajax-sport-country-tournament-archive_/{data.get('sid', self.sport_id)}/{data.get('id', self.league_id)}"
                    }
                except json.JSONDecodeError:
                    pass
        
        return None
    
    def _extract_ajax_pattern_from_next_matches(self, response):
        """Extract from next-matches component"""
        next_matches = response.css('next-matches::attr(:odds-request)').get()
        
        if next_matches:
            try:
                data = json.loads(next_matches)
                url = data.get('url', '')
                
                if '/ajax-sport-country-tournament-archive_/' in url:
                    parts = url.strip('/').split('/')
                    if len(parts) >= 3:
                        return {
                            'sport_id': parts[1],
                            'encoded_id': parts[2],
                            'base_url': f"/ajax-sport-country-tournament-archive_/{parts[1]}/{parts[2]}"
                        }
            except json.JSONDecodeError:
                pass
        
        return None
    
    def _parse_fixtures_init(self, response):
        """Initialize fixtures extraction"""
        # First, extract matches from JSON-LD structured data
        matches_from_html = self._extract_matches_from_jsonld(response)
        
        if matches_from_html:
            self.logger.info(f"Found {len(matches_from_html)} matches in JSON-LD data")
            
            # Create page item with matches from HTML
            page_loader = SeasonMatchesLoader()
            page_loader.add_value('league_id', self.league_id)
            page_loader.add_value('league_name', self.league_name)
            page_loader.add_value('season_id', self.season_id)
            page_loader.add_value('sport_id', self.sport_id)
            page_loader.add_value('sport_name', self.sport_name)
            page_loader.add_value('country_name', self.country_name)
            page_loader.add_value('extraction_type', 'fixtures')
            page_loader.add_value('page_number', 1)
            page_loader.add_value('total_pages', 1)
            page_loader.add_value('has_next_page', False)
            page_loader.add_value('source_url', response.url)
            page_loader.add_value('extraction_timestamp', None)
            page_loader.add_value('matches', matches_from_html)
            page_loader.add_value('total_matches', len(matches_from_html))
            
            page_item = page_loader.load_item()
            
            # Yield the container
            yield page_item
            
            # Also yield individual matches
            for match in matches_from_html:
                yield match
        else:
            # Fallback to AJAX method if no JSON-LD data found
            self.logger.info("No JSON-LD data found, trying AJAX method")
            
            # Extract tournament info from pageOutrightsVar
            tournament_info = self._extract_tournament_info(response)
            
            if not tournament_info:
                self.logger.error("Failed to extract tournament info for fixtures")
                return
            
            # Extract odds request URL
            odds_request_url = self._extract_odds_request_url(response)
            
            if odds_request_url:
                # Make AJAX request for fixtures
                yield scrapy.Request(
                    url=odds_request_url,
                    callback=self.parse_fixtures_ajax,
                    headers={
                        'X-Requested-With': 'XMLHttpRequest',
                        'Referer': response.url,
                        'Accept': 'application/json, text/plain, */*'
                    },
                    meta={
                        'tournament_info': tournament_info,
                        'source_url': response.url
                    },
                    errback=self.handle_ajax_error
                )
            else:
                # Try to extract matches directly from the page
                yield from self._parse_fixtures_from_page(response, tournament_info)
    
    def _extract_tournament_info(self, response):
        """Extract tournament info from page"""
        # Look for pageOutrightsVar using selector
        pagevar_script = response.xpath('//script[contains(text(), "pageOutrightsVar")]/text()').get()
        
        if pagevar_script:
            match = re.search(r'var\s+pageOutrightsVar\s*=\s*\'({.*?})\'', pagevar_script, re.DOTALL)
            if match:
                try:
                    data = json.loads(match.group(1))
                    return {
                        'encoded_id': data.get('id', self.league_id),
                        'sport_id': data.get('sid', self.sport_id)
                    }
                except json.JSONDecodeError:
                    pass
        
        # Fallback to provided values
        return {
            'encoded_id': self.league_id,
            'sport_id': self.sport_id
        }
    
    def _extract_odds_request_url(self, response):
        """Extract odds request URL for fixtures"""
        # Look for tournament-component first
        tournament_component = response.css('tournament-component::attr(:sport-data)').get()
        
        if tournament_component:
            try:
                data = json.loads(tournament_component)
                odds_request = data.get('oddsRequest', {})
                url = odds_request.get('url', '')
                if url:
                    # Make it absolute
                    if url.startswith('/'):
                        return f"https://www.oddsportal.com{url}"
                    return url
            except json.JSONDecodeError:
                pass
        
        return None
    
    def _request_results_page(self, page: int, referer: str):
        """Request a specific page of results"""
        if self.max_pages and page > self.start_page + self.max_pages - 1:
            self.logger.info(f"Reached maximum pages limit ({self.max_pages})")
            return
        
        # Build AJAX URL for results
        # The pattern from the HTML shows it should be: /ajax-sport-country-tournament-archive_/{sport_id}/{encoded_id}/
        # But for pagination, we need to add page and timezone parameters
        
        # Get base URL from ajax_info
        base_url = self.ajax_info.get('base_url')
        if not base_url:
            base_url = f"/ajax-sport-country-tournament-archive_/{self.ajax_info['sport_id']}/{self.ajax_info['encoded_id']}"
        
        # Add pagination parameters
        # Based on OddsPortal patterns, the full URL is:
        # /ajax-sport-country-tournament-archive_/{sport_id}/{encoded_id}/{page}/{timezone}/?_={timestamp}
        timestamp = int(time.time() * 1000)
        timezone = "0"  # Use 0 for UTC
        
        ajax_url = f"https://www.oddsportal.com{base_url}/{page}/{timezone}/?_={timestamp}"
        
        self.logger.info(f"Requesting results page {page}: {ajax_url}")
        
        yield scrapy.Request(
            url=ajax_url,
            callback=self.parse_results_ajax,
            headers={
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': referer,
                'Accept': 'application/json, text/plain, */*',
                'User-Agent': self.headers['User-Agent']
            },
            meta={
                'page': page,
                'referer': referer
            },
            errback=self.handle_ajax_error
        )
    
    def parse_results_ajax(self, response):
        """Parse AJAX response for results
        
        Note: This spider intentionally does not extract match scores/results.
        The season spider focuses on match discovery, while detailed match data
        (including scores) should be extracted by the match spider.
        """
        meta = response.meta
        current_page = meta['page']
        
        if response.status != 200:
            self.logger.error(f"Failed to fetch results page {current_page}: HTTP {response.status}")
            return
        
        # Decrypt response
        try:
            encrypted_data = response.text.strip()
            decrypted_data = decrypt_data_PBKDF2HMAC(encrypted_data)
            
            if not decrypted_data or decrypted_data.get('s') != 1:
                self.logger.error("Failed to decrypt or invalid response")
                return
        except Exception as e:
            self.logger.error(f"Decryption error: {e}")
            return
        
        # Parse results
        try:
            page_item = parse_season_matches(
                response_data=decrypted_data,
                league_id=self.league_id,
                league_name=self.league_name,
                season_id=self.season_id,
                sport_id=self.sport_id,
                sport_name=self.sport_name,
                country_name=self.country_name,
                extraction_type="results",
                source_url=response.url
            )
            
            # Yield the page container
            yield page_item
            
            # Also yield individual matches
            for match in page_item.get('matches', []):
                yield match
            
            # Log summary
            total_matches = len(page_item.get('matches', []))
            self.logger.info(f"Results page {current_page}: Found {total_matches} matches")
            
            # Continue pagination
            if page_item.get('has_next_page'):
                yield from self._request_results_page(
                    page=current_page + 1,
                    referer=meta['referer']
                )
            else:
                self.logger.info(f"Reached last results page ({current_page})")
                
        except Exception as e:
            self.logger.error(f"Error parsing results page: {e}")
            self.logger.exception("Full traceback:")
    
    def parse_fixtures_ajax(self, response):
        """Parse AJAX response for fixtures"""
        meta = response.meta
        tournament_info = meta['tournament_info']
        
        if response.status != 200:
            self.logger.error(f"Failed to fetch fixtures: HTTP {response.status}")
            return
        
        # Parse JSON response (fixtures are not encrypted)
        try:
            data = json.loads(response.text)
            
            if data.get('s') != 1:
                self.logger.error(f"Invalid fixtures response status: {data.get('s')}")
                return
            
            # Extract matches from oddsData
            odds_data = data.get('d', {}).get('oddsData', {})
            
            # Create a page item for fixtures
            page_loader = SeasonMatchesLoader()
            page_loader.add_value('league_id', self.league_id)
            page_loader.add_value('league_name', self.league_name)
            page_loader.add_value('season_id', self.season_id)
            page_loader.add_value('sport_id', self.sport_id)
            page_loader.add_value('sport_name', self.sport_name)
            page_loader.add_value('country_name', self.country_name)
            page_loader.add_value('extraction_type', 'fixtures')
            page_loader.add_value('page_number', 1)
            page_loader.add_value('total_pages', 1)
            page_loader.add_value('has_next_page', False)
            page_loader.add_value('source_url', meta['source_url'])
            page_loader.add_value('extraction_timestamp', None)
            
            # Parse each match from oddsData
            match_items = []
            for match_id, match_data in odds_data.items():
                if match_id and match_data.get('event'):
                    # Create minimal match info
                    loader = MatchInfoLoader()
                    loader.add_value('match_id', match_id)
                    loader.add_value('match_url', f"/basketball/{self.country_name.lower()}/{self.league_name.lower()}/match-{match_id}/")
                    loader.add_value('status', 'scheduled')
                    loader.add_value('league_id', self.league_id)
                    loader.add_value('league_name', self.league_name)
                    loader.add_value('season_id', self.season_id)
                    loader.add_value('sport_id', self.sport_id)
                    loader.add_value('tournament_stage', None)
                    loader.add_value('extracted_at', None)
                    
                    match_item = loader.load_item()
                    match_items.append(match_item)
                    yield match_item
            
            page_loader.add_value('matches', match_items)
            page_loader.add_value('total_matches', len(match_items))
            
            # Yield the container
            yield page_loader.load_item()
            
            self.logger.info(f"Fixtures: Found {len(match_items)} upcoming matches")
            
        except Exception as e:
            self.logger.error(f"Error parsing fixtures: {e}")
            self.logger.exception("Full traceback:")
    
    def _parse_fixtures_from_page(self, response, tournament_info):
        """Fallback: try to extract fixtures directly from page HTML"""
        # This would parse the HTML table if AJAX fails
        # Implementation depends on the specific HTML structure
        self.logger.warning("Attempting to parse fixtures from HTML (AJAX failed)")
        
        # Look for match containers in the page
        matches = response.css('div[class*="match"], tr[class*="match"]')
        
        if matches:
            self.logger.info(f"Found {len(matches)} matches in HTML")
            # Parse each match...
        else:
            self.logger.error("No matches found in HTML")
    
    def _extract_matches_from_jsonld(self, response):
        """Extract match information from JSON-LD structured data"""
        matches = []
        
        # Find all JSON-LD scripts with sports event data
        jsonld_scripts = response.xpath('//script[@type="application/ld+json"]/text()').getall()
        
        for script_text in jsonld_scripts:
            try:
                data = json.loads(script_text.strip())
                
                # Check if this is a sports event
                if isinstance(data.get('@type'), list) and 'SportsEvent' in data['@type']:
                    # Extract match ID from URL
                    match_url = data.get('url', '')
                    match_id_match = re.search(r'-([a-zA-Z0-9]+)/?$', match_url)
                    if not match_id_match:
                        self.logger.warning(f"Could not extract match ID from URL: {match_url}")
                        continue
                    
                    match_id = match_id_match.group(1)
                    
                    # Parse teams from name
                    match_name = data.get('name', '')
                    teams = match_name.split(' - ')
                    home_team = teams[0].strip() if len(teams) >= 2 else None
                    away_team = teams[1].strip() if len(teams) >= 2 else None
                    
                    # Parse timestamp
                    start_date = data.get('startDate')
                    timestamp = None
                    if start_date:
                        try:
                            # Parse ISO format with timezone
                            dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                            timestamp = int(dt.timestamp())
                        except Exception as e:
                            self.logger.warning(f"Failed to parse date {start_date}: {e}")
                    
                    # Extract venue
                    location = data.get('location', {})
                    venue = location.get('name')
                    
                    # Create match item using loader
                    loader = MatchInfoLoader()
                    loader.add_value('match_id', match_id)
                    loader.add_value('match_url', match_url)
                    loader.add_value('match_timestamp', timestamp)
                    loader.add_value('status', 'scheduled' if data.get('eventStatus') == 'https://schema.org/EventScheduled' else 'unknown')
                    loader.add_value('home_team', home_team)
                    loader.add_value('away_team', away_team)
                    loader.add_value('league_id', self.league_id)
                    loader.add_value('league_name', self.league_name)
                    loader.add_value('season_id', self.season_id)
                    loader.add_value('sport_id', self.sport_id)
                    loader.add_value('tournament_stage', None)
                    loader.add_value('extracted_at', None)
                    
                    match_item = loader.load_item()
                    matches.append(match_item)
                    self.logger.debug(f"Extracted match from JSON-LD: {match_id} - {home_team} vs {away_team}")
                    
            except json.JSONDecodeError as e:
                self.logger.warning(f"Failed to parse JSON-LD script: {e}")
                continue
            except Exception as e:
                self.logger.warning(f"Error parsing JSON-LD: {e}")
                continue
        
        return matches
    
    def handle_ajax_error(self, failure):
        """Handle errors when fetching AJAX data"""
        request = failure.request
        self.logger.error(f"AJAX request failed: {failure.value}")
    
    def parse_next_link(self, response):
        """No pagination needed - handled via AJAX"""
        return []