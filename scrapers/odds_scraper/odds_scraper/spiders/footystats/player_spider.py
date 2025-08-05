from typing import Dict, Any, Optional
from .base_spider import FootyStatsBaseSpider
from ...items.footystats.player_items import (
    PlayerItem,
    validate_player_item,
    create_player_item
)

class PlayerSpider(FootyStatsBaseSpider):
    """
    Spider for FootyStats /player endpoint
    
    Extracts detailed statistics for a specific player across all competitions:
    - Basic player information (name, position, age, physical attributes)
    - Career statistics across all competitions and seasons
    - Season-by-season breakdown
    - Performance metrics and averages
    - Current team information
    - Market value and contract details
    
    Usage:
    scrapy crawl footystats_player -a player_id=12345 -O player.json
    scrapy crawl footystats_player -a api_key=your_key -a player_id=67890
    """
    
    name = "footystats_player"
    endpoint_name = "player"
    allowed_domains = ["api.football-data-api.com"]
    
    def __init__(self, api_key: str = "example", player_id: str = None, **kwargs):
        """
        Initialize player spider
        
        Args:
            api_key: FootyStats API key
            player_id: Player ID to retrieve detailed statistics for (required)
        """
        super().__init__(api_key=api_key, **kwargs)
        
        if not player_id:
            raise ValueError("player_id parameter is required")
        
        self.player_id = player_id
        
        self.logger.info(f"Player spider initialized - Player ID: {player_id}")
    
    def get_request_params(self) -> Dict[str, Any]:
        """Build request parameters for player endpoint"""
        return {
            'player_id': self.player_id
        }
    
    def parse_data_item(self, item_data: Dict[str, Any]) -> Optional[PlayerItem]:
        """
        Parse player data from API response
        
        Args:
            item_data: Single player object from data[] array
            
        Returns:
            PlayerItem or None if invalid
        """
        # Validate player data
        if not validate_player_item(item_data):
            player_name = item_data.get('player_name', 'Unknown')
            self.logger.warning(f"Invalid player data: {player_name}")
            return None
        
        try:
            # Create player item using helper function
            player_item = create_player_item(item_data)
            
            # Log progress
            player_name = player_item.get('player_name', 'Unknown')
            current_team = player_item.get('current_team', 'Unknown')
            position = player_item.get('position', 'Unknown')
            age = player_item.get('age', 'Unknown')
            career_goals = player_item.get('career_goals', 0)
            career_apps = player_item.get('career_appearances', 0)
            seasons_count = len(player_item.get('seasons', []))
            
            self.logger.debug(f"Processed player: {player_name} ({position}, {age}y) - {current_team} - {career_goals} goals in {career_apps} apps across {seasons_count} seasons")
            
            return player_item
            
        except Exception as e:
            player_name = item_data.get('player_name', 'Unknown')
            self.logger.error(f"Error processing player {player_name}: {e}")
            return None