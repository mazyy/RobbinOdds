from typing import Dict, Any, Optional
from .base_spider import FootyStatsBaseSpider
from ...items.footystats.league_referees_items import (
    LeagueRefereeItem,
    validate_league_referee_item,
    create_league_referee_item
)

class LeagueRefereesSpider(FootyStatsBaseSpider):
    """
    Spider for FootyStats /league-referees endpoint
    
    Extracts referees active in a specific league season with statistics:
    - Basic referee information (name, nationality)
    - Appearance statistics in the league
    - Match statistics (goals, cards, BTTS percentages)
    - Performance indicators specific to this league
    
    Usage:
    scrapy crawl footystats_league_referees -a season_id=2012 -O referees.json
    scrapy crawl footystats_league_referees -a api_key=your_key -a season_id=1625
    """
    
    name = "footystats_league_referees"
    endpoint_name = "league-referees"
    allowed_domains = ["api.football-data-api.com"]
    
    def __init__(self, api_key: str = "example", season_id: str = None, **kwargs):
        """
        Initialize league referees spider
        
        Args:
            api_key: FootyStats API key
            season_id: Season ID to retrieve referees for (required)
        """
        super().__init__(api_key=api_key, **kwargs)
        
        if not season_id:
            raise ValueError("season_id parameter is required")
        
        self.season_id = season_id
        
        self.logger.info(f"League referees spider initialized - Season ID: {season_id}")
    
    def get_request_params(self) -> Dict[str, Any]:
        """Build request parameters for league-referees endpoint"""
        return {
            'season_id': self.season_id
        }
    
    def parse_data_item(self, item_data: Dict[str, Any]) -> Optional[LeagueRefereeItem]:
        """
        Parse individual referee from API response
        
        Args:
            item_data: Single referee object from data[] array
            
        Returns:
            LeagueRefereeItem or None if invalid
        """
        # Validate referee data
        if not validate_league_referee_item(item_data):
            referee_name = item_data.get('full_name', 'Unknown')
            self.logger.warning(f"Invalid referee data: {referee_name}")
            return None
        
        try:
            # Create referee item using helper function
            referee_item = create_league_referee_item(item_data)
            
            # Log progress
            referee_name = referee_item.get('full_name', 'Unknown')
            nationality = referee_item.get('nationality', 'Unknown')
            appearances = referee_item.get('appearances_overall', 0)
            goals_per_match = referee_item.get('goals_per_match_overall', 0)
            btts_percentage = referee_item.get('btts_percentage', 0)
            
            self.logger.debug(f"Processed referee: {referee_name} ({nationality}) - {appearances} apps, {goals_per_match:.2f} goals/match, {btts_percentage:.1f}% BTTS")
            
            return referee_item
            
        except Exception as e:
            referee_name = item_data.get('full_name', 'Unknown')
            self.logger.error(f"Error processing referee {referee_name}: {e}")
            return None