# scrapers/odds_scraper/odds_scraper/spiders/odds_portal/league_spider.py

from odds_scraper.spiders.odds_portal.base_spider import BaseSpider
from odds_scraper.spiders.odds_portal.utils.league_discovery_parser import LeagueDiscoveryParser
import scrapy

class LeagueSpider(BaseSpider):
    """Spider for discovering leagues and their available seasons"""
    name = "oddsportal_league_spider"
    allowed_domains = ["oddsportal.com"]
    
    custom_settings = {
        'CONCURRENT_REQUESTS': 2,
        'DOWNLOAD_DELAY': 1.5,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
    }
    
    def __init__(self, league_url: str = None, **kwargs):
        """
        Initialize league discovery spider.
        
        Args:
            league_url: Base league URL (e.g., https://www.oddsportal.com/basketball/usa/nba/)
        """
        super().__init__(**kwargs)
        
        if not league_url:
            raise ValueError("league_url parameter is required")
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.league_url = league_url.rstrip('/')
        self.start_urls = [self.league_url + '/results/']  # Start with results page
        
        self.logger.info(f"Discovering league: {self.league_url}")
    
    def parse_items(self, response):
        """Parse the league page for discovery"""
        self.logger.info(f"Parsing league discovery page: {response.url}")
        
        # Initialize parser
        parser = LeagueDiscoveryParser(self.league_url)
        
        # Parse and yield discovery data
        discovery_item = parser.parse_discovery_page(response)
        
        if discovery_item:
            yield discovery_item
        else:
            self.logger.error("Failed to parse discovery data")
    
    def parse_next_link(self, response):
        """No pagination needed for league discovery"""
        return []