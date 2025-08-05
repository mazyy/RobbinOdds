from typing import Dict, Any, Optional
from .base_spider import FootyStatsBaseSpider
from ...items.footystats.league_players_items import (
    LeaguePlayerItem,
    validate_league_player_item,
    create_league_player_item
)

class LeaguePlayersSpider(FootyStatsBaseSpider):
    """
    Spider for FootyStats /league-players endpoint
    
    Extracts all players in a league season with statistics:
    - Basic player information (name, position, age)
    - Team affiliation
    - Performance statistics (goals, assists, appearances)
    - Disciplinary records (cards)
    - 60+ statistical data points per player
    
    Usage:
    scrapy crawl footystats_league_players -a season_id=2012 -O players.json
    scrapy crawl footystats_league_players -a api_key=your_key -a season_id=1625
    scrapy crawl footystats_league_players -a season_id=2012 -a page=2
    """
    
    name = "footystats_league_players"
    endpoint_name = "league-players"
    allowed_domains = ["api.football-data-api.com"]
    
    def __init__(self, api_key: str = "example", season_id: str = None,
                 page: str = None, **kwargs):
        """
        Initialize league players spider
        
        Args:
            api_key: FootyStats API key
            season_id: Season ID to retrieve players for (required)
            page: Page number for pagination (optional)
        """
        super().__init__(api_key=api_key, **kwargs)
        
        if not season_id:
            raise ValueError("season_id parameter is required")
        
        self.season_id = season_id
        self.page = page
        
        self.logger.info(f"League players spider initialized - Season ID: {season_id}")
        if page:
            self.logger.info(f"Requesting page: {page}")
    
    def get_request_params(self) -> Dict[str, Any]:
        """Build request parameters for league-players endpoint"""
        params = {
            'season_id': self.season_id
        }
        
        if self.page:
            params['page'] = self.page
            
        return params
    
    def parse_data_item(self, item_data: Dict[str, Any]) -> Optional[LeaguePlayerItem]:
        """
        Parse individual player from API response
        
        Args:
            item_data: Single player object from data[] array
            
        Returns:
            LeaguePlayerItem or None if invalid
        """
        # Validate player data
        if not validate_league_player_item(item_data):
            player_name = item_data.get('player_name', 'Unknown')
            self.logger.warning(f"Invalid player data: {player_name}")
            return None
        
        try:
            # Create player item using helper function
            player_item = create_league_player_item(item_data)
            
            # Log progress
            player_name = player_item.get('player_name', 'Unknown')
            team_name = player_item.get('team_name', 'Unknown')
            position = player_item.get('position', 'Unknown')
            goals = player_item.get('goals', 0)
            apps = player_item.get('apps', 0)
            
            self.logger.debug(f"Processed player: {player_name} ({team_name}, {position}) - {goals} goals in {apps} apps")
            
            return player_item
            
        except Exception as e:
            player_name = item_data.get('player_name', 'Unknown')
            self.logger.error(f"Error processing player {player_name}: {e}")
            return None