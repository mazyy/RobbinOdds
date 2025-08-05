from typing import Dict, Any, Optional
from .base_spider import FootyStatsBaseSpider
from ...items.footystats.league_stats_items import (
    LeagueStatsItem,
    validate_league_stats_item,
    create_league_stats_item
)

class LeagueStatsSpider(FootyStatsBaseSpider):
    """
    Spider for FootyStats /league-stats endpoint
    
    Extracts comprehensive league statistics including:
    - Basic league information
    - Goal statistics and averages
    - BTTS (Both Teams To Score) data
    - Corner statistics
    - Card statistics
    - Over 100+ statistical data points
    
    Usage:
    scrapy crawl footystats_league_stats -a season_id=2012 -O league_stats.json
    scrapy crawl footystats_league_stats -a api_key=your_key -a season_id=1625
    scrapy crawl footystats_league_stats -a season_id=2012 -a max_time=1537984169
    """
    
    name = "footystats_league_stats"
    endpoint_name = "league-stats"
    allowed_domains = ["api.football-data-api.com"]
    
    def __init__(self, api_key: str = "example", season_id: str = None,
                 max_time: str = None, **kwargs):
        """
        Initialize league stats spider
        
        Args:
            api_key: FootyStats API key
            season_id: Season ID to retrieve stats for (required)
            max_time: UNIX timestamp to get historical stats up to specific time (optional)
        """
        super().__init__(api_key=api_key, **kwargs)
        
        if not season_id:
            raise ValueError("season_id parameter is required")
        
        self.season_id = season_id
        self.max_time = max_time
        
        self.logger.info(f"League stats spider initialized - Season ID: {season_id}")
        if max_time:
            self.logger.info(f"Historical stats requested up to timestamp: {max_time}")
    
    def get_request_params(self) -> Dict[str, Any]:
        """Build request parameters for league-stats endpoint"""
        params = {
            'season_id': self.season_id
        }
        
        if self.max_time:
            params['max_time'] = self.max_time
            
        return params
    
    def parse_data_item(self, item_data: Dict[str, Any]) -> Optional[LeagueStatsItem]:
        """
        Parse league stats from API response
        
        Args:
            item_data: Single league stats object from data[] array
            
        Returns:
            LeagueStatsItem or None if invalid
        """
        # Validate league stats data
        if not validate_league_stats_item(item_data):
            league_name = item_data.get('name', 'Unknown')
            self.logger.warning(f"Invalid league stats data: {league_name}")
            return None
        
        try:
            # Create league stats item using helper function
            stats_item = create_league_stats_item(item_data)
            
            # Log progress
            league_name = stats_item.get('name', 'Unknown')
            season = stats_item.get('season', 'Unknown')
            matches = stats_item.get('totalMatches', 0)
            self.logger.debug(f"Processed league stats: {league_name} {season} ({matches} matches)")
            
            return stats_item
            
        except Exception as e:
            league_name = item_data.get('name', 'Unknown')
            self.logger.error(f"Error processing league stats {league_name}: {e}")
            return None