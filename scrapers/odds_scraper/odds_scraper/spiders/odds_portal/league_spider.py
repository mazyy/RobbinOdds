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
            # Log summary
            league = discovery_item.get('league', {})
            seasons = discovery_item.get('seasons', [])
            
            self.logger.info(
                f"Discovered league: {league.get('league_name')} "
                f"(ID: {league.get('league_id')}) with {len(seasons)} seasons"
            )
            
            for season in seasons:
                self.logger.info(
                    f"  - {season.get('season_name')} "
                    f"({'Current' if season.get('is_current') else season.get('season_id')})"
                )
            
            yield discovery_item
        else:
            self.logger.error("Failed to parse discovery data")
    
    def parse_next_link(self, response):
        """No pagination needed for league discovery"""
        return []