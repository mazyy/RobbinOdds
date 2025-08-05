from typing import Dict, Any, Optional
from .base_spider import FootyStatsBaseSpider
from ...items.footystats.league_matches_items import (
    LeagueMatchItem,
    validate_league_match_item,
    create_league_match_item
)

class LeagueMatchesSpider(FootyStatsBaseSpider):
    """
    Spider for FootyStats /league-matches endpoint
    
    Extracts all matches for a specific league season with detailed statistics:
    - Match details (teams, scores, timing)
    - Match statistics (corners, cards, shots, possession)
    - Goal timing information
    - Pre-match odds
    - Referee and venue information
    - 100+ statistical data points per match
    
    Usage:
    scrapy crawl footystats_league_matches -a season_id=2012 -O matches.json
    scrapy crawl footystats_league_matches -a api_key=your_key -a season_id=1625
    scrapy crawl footystats_league_matches -a season_id=2012 -a page=2
    scrapy crawl footystats_league_matches -a season_id=2012 -a max_per_page=500
    scrapy crawl footystats_league_matches -a season_id=2012 -a max_time=1537984169
    """
    
    name = "footystats_league_matches"
    endpoint_name = "league-matches"
    allowed_domains = ["api.football-data-api.com"]
    
    def __init__(self, api_key: str = "example", season_id: str = None,
                 max_time: str = None, page: str = None, 
                 max_per_page: str = None, **kwargs):
        """
        Initialize league matches spider
        
        Args:
            api_key: FootyStats API key
            season_id: Season ID to retrieve matches for (required)
            max_time: UNIX timestamp for historical data (optional)
            page: Page number for pagination (optional)
            max_per_page: Results per page, max 500 (optional, default: 300)
        """
        super().__init__(api_key=api_key, **kwargs)
        
        if not season_id:
            raise ValueError("season_id parameter is required")
        
        self.season_id = season_id
        self.max_time = max_time
        self.page = page
        self.max_per_page = max_per_page
        
        self.logger.info(f"League matches spider initialized - Season ID: {season_id}")
        if max_time:
            self.logger.info(f"Historical data requested up to timestamp: {max_time}")
        if page:
            self.logger.info(f"Requesting page: {page}")
        if max_per_page:
            self.logger.info(f"Max per page: {max_per_page}")
    
    def get_request_params(self) -> Dict[str, Any]:
        """Build request parameters for league-matches endpoint"""
        params = {
            'season_id': self.season_id
        }
        
        if self.max_time:
            params['max_time'] = self.max_time
            
        if self.page:
            params['page'] = self.page
            
        if self.max_per_page:
            params['max_per_page'] = self.max_per_page
            
        return params
    
    def parse_data_item(self, item_data: Dict[str, Any]) -> Optional[LeagueMatchItem]:
        """
        Parse individual match from API response
        
        Args:
            item_data: Single match object from data[] array
            
        Returns:
            LeagueMatchItem or None if invalid
        """
        # Validate match data
        if not validate_league_match_item(item_data):
            match_info = f"{item_data.get('home_name', 'Unknown')} vs {item_data.get('away_name', 'Unknown')}"
            self.logger.warning(f"Invalid match data: {match_info}")
            return None
        
        try:
            # Create match item using helper function
            match_item = create_league_match_item(item_data)
            
            # Log progress
            match_info = f"{match_item.get('home_name')} vs {match_item.get('away_name')}"
            score = f"{match_item.get('homeGoalCount', 0)}-{match_item.get('awayGoalCount', 0)}"
            status = match_item.get('status', 'unknown')
            self.logger.debug(f"Processed match: {match_info} {score} ({status})")
            
            return match_item
            
        except Exception as e:
            match_info = f"{item_data.get('home_name', 'Unknown')} vs {item_data.get('away_name', 'Unknown')}"
            self.logger.error(f"Error processing match {match_info}: {e}")
            return None