from typing import Dict, Any, Optional
from .base_spider import FootyStatsBaseSpider
from ...items.footystats.league_table_items import (
    LeagueTableItem,
    validate_league_table_item,
    create_league_table_item
)

class LeagueTableSpider(FootyStatsBaseSpider):
    """
    Spider for FootyStats /league-table endpoint
    
    Extracts league standings with position, points, goal difference:
    - Team position and points data
    - Win/draw/loss statistics
    - Goal statistics (for/against, difference)
    - Home and away performance breakdown
    - Clean sheets and failed to score metrics
    
    Usage:
    scrapy crawl footystats_league_table -a season_id=1625 -O table.json
    scrapy crawl footystats_league_table -a api_key=your_key -a season_id=2012
    """
    
    name = "footystats_league_table"
    endpoint_name = "league-tables"
    allowed_domains = ["api.football-data-api.com"]
    
    def __init__(self, api_key: str = "example", season_id: str = None, **kwargs):
        """
        Initialize league table spider
        
        Args:
            api_key: FootyStats API key
            season_id: Season ID to retrieve table for (required)
        """
        super().__init__(api_key=api_key, **kwargs)
        
        if not season_id:
            raise ValueError("season_id parameter is required")
        
        self.season_id = season_id
        
        self.logger.info(f"League table spider initialized - Season ID: {season_id}")
    
    def get_request_params(self) -> Dict[str, Any]:
        """Build request parameters for league-table endpoint"""
        params = {
            'season_id': self.season_id
        }
        
        return params
    
    def extract_data_items(self, data: Dict[str, Any]):
        """Extract league table data from nested response structure"""
        # League tables API returns data.league_table array
        return data.get('league_table', [])
    
    def parse_data_item(self, item_data: Dict[str, Any]) -> Optional[LeagueTableItem]:
        """
        Parse individual team from league table API response
        
        Args:
            item_data: Single team object from data[] array
            
        Returns:
            LeagueTableItem or None if invalid
        """
        # Validate table entry data
        if not validate_league_table_item(item_data):
            team_name = item_data.get('name', 'Unknown')
            self.logger.warning(f"Invalid league table data: {team_name}")
            return None
        
        try:
            # Create table item using helper function
            table_item = create_league_table_item(item_data)
            
            # Log progress
            team_name = table_item.get('name', 'Unknown')
            position = table_item.get('position', 'Unknown')
            points = table_item.get('points', 0)
            goals_for = table_item.get('goals_for', 0)
            goals_against = table_item.get('goals_against', 0)
            goal_diff = table_item.get('goal_difference', 0)
            
            self.logger.debug(f"Processed team: {team_name} (Pos: {position}, Pts: {points}, GD: {goal_diff}, GF: {goals_for}, GA: {goals_against})")
            
            return table_item
            
        except Exception as e:
            team_name = item_data.get('name', 'Unknown')
            self.logger.error(f"Error processing league table entry {team_name}: {e}")
            return None