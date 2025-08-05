from typing import Dict, Any, Optional
from .base_spider import FootyStatsBaseSpider
from ...items.footystats.team_items import (
    TeamItem,
    validate_team_item,
    create_team_item
)

class TeamSpider(FootyStatsBaseSpider):
    """
    Spider for FootyStats /team endpoint
    
    Extracts comprehensive statistics for a specific team:
    - Basic team information
    - Season statistics (goals, form, position)
    - 700+ detailed statistical fields
    
    Usage:
    scrapy crawl footystats_team -a team_id=2624 -O team.json
    scrapy crawl footystats_team -a api_key=your_key -a team_id=149
    scrapy crawl footystats_team -a team_id=2624 -a season_id=2012
    """
    
    name = "footystats_team"
    endpoint_name = "team"
    allowed_domains = ["api.football-data-api.com"]
    
    def __init__(self, api_key: str = "example", team_id: str = None,
                 season_id: str = None, **kwargs):
        """
        Initialize team spider
        
        Args:
            api_key: FootyStats API key
            team_id: Team ID to retrieve statistics for (required)
            season_id: Specific season ID (optional, defaults to latest)
        """
        super().__init__(api_key=api_key, **kwargs)
        
        if not team_id:
            raise ValueError("team_id parameter is required")
        
        self.team_id = team_id
        self.season_id = season_id
        
        self.logger.info(f"Team spider initialized - Team ID: {team_id}")
        if season_id:
            self.logger.info(f"Season ID: {season_id}")
    
    def get_request_params(self) -> Dict[str, Any]:
        """Build request parameters for team endpoint"""
        params = {
            'team_id': self.team_id
        }
        
        if self.season_id:
            params['season_id'] = self.season_id
            
        return params
    
    def parse_data_item(self, item_data: Dict[str, Any]) -> Optional[TeamItem]:
        """
        Parse team data from API response
        
        Args:
            item_data: Single team object from data[] array
            
        Returns:
            TeamItem or None if invalid
        """
        # Validate team data
        if not validate_team_item(item_data):
            team_name = item_data.get('name', 'Unknown')
            self.logger.warning(f"Invalid team data: {team_name}")
            return None
        
        try:
            # Create team item using helper function
            team_item = create_team_item(item_data)
            
            # Log progress
            team_name = team_item.get('name', 'Unknown')
            league = team_item.get('league_name', 'Unknown')
            position = team_item.get('form_overall_position', 'Unknown')
            points = team_item.get('seasonPoints', 0)
            
            self.logger.debug(f"Processed team: {team_name} ({league}) - Pos: {position}, Pts: {points}")
            
            return team_item
            
        except Exception as e:
            team_name = item_data.get('name', 'Unknown')
            self.logger.error(f"Error processing team {team_name}: {e}")
            return None