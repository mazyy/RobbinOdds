from typing import Dict, Any, Optional
from .base_spider import FootyStatsBaseSpider
from ...items.footystats.league_teams_items import (
    LeagueTeamItem,
    validate_league_team_item,
    create_league_team_item
)

class LeagueTeamsSpider(FootyStatsBaseSpider):
    """
    Spider for FootyStats /league-teams endpoint
    
    Extracts all teams in a league season with comprehensive statistics:
    - Basic team information (name, IDs)
    - Season record (wins, draws, losses)
    - Goal statistics (for/against, clean sheets)
    - Form and positioning data
    - Optional: 700+ detailed statistical fields with include=stats
    
    Usage:
    scrapy crawl footystats_league_teams -a season_id=2012 -O teams.json
    scrapy crawl footystats_league_teams -a api_key=your_key -a season_id=1625
    scrapy crawl footystats_league_teams -a season_id=2012 -a include=stats
    scrapy crawl footystats_league_teams -a season_id=2012 -a max_time=1537984169
    """
    
    name = "footystats_league_teams"
    endpoint_name = "league-teams"
    allowed_domains = ["api.football-data-api.com"]
    
    def __init__(self, api_key: str = "example", season_id: str = None,
                 include: str = None, max_time: str = None, **kwargs):
        """
        Initialize league teams spider
        
        Args:
            api_key: FootyStats API key
            season_id: Season ID to retrieve teams for (required)
            include: Add "stats" to include detailed team statistics (optional)
            max_time: UNIX timestamp for historical data (optional)
        """
        super().__init__(api_key=api_key, **kwargs)
        
        if not season_id:
            raise ValueError("season_id parameter is required")
        
        self.season_id = season_id
        self.include = include
        self.max_time = max_time
        
        self.logger.info(f"League teams spider initialized - Season ID: {season_id}")
        if include:
            self.logger.info(f"Including detailed stats: {include}")
        if max_time:
            self.logger.info(f"Historical data requested up to timestamp: {max_time}")
    
    def get_request_params(self) -> Dict[str, Any]:
        """Build request parameters for league-teams endpoint"""
        params = {
            'season_id': self.season_id
        }
        
        if self.include:
            params['include'] = self.include
            
        if self.max_time:
            params['max_time'] = self.max_time
            
        return params
    
    def parse_data_item(self, item_data: Dict[str, Any]) -> Optional[LeagueTeamItem]:
        """
        Parse individual team from API response
        
        Args:
            item_data: Single team object from data[] array
            
        Returns:
            LeagueTeamItem or None if invalid
        """
        # Validate team data
        if not validate_league_team_item(item_data):
            team_name = item_data.get('name', 'Unknown')
            self.logger.warning(f"Invalid team data: {team_name}")
            return None
        
        try:
            # Create team item using helper function
            team_item = create_league_team_item(item_data)
            
            # Log progress
            team_name = team_item.get('name', 'Unknown')
            position = team_item.get('form_overall_position', 'Unknown')
            points = team_item.get('seasonPoints', 0)
            goals_for = team_item.get('seasonGoalsFor', 0)
            goals_against = team_item.get('seasonGoalsAgainst', 0)
            
            self.logger.debug(f"Processed team: {team_name} (Pos: {position}, Pts: {points}, GF: {goals_for}, GA: {goals_against})")
            
            return team_item
            
        except Exception as e:
            team_name = item_data.get('name', 'Unknown')
            self.logger.error(f"Error processing team {team_name}: {e}")
            return None