from typing import Dict, Any, Optional
from .base_spider import FootyStatsBaseSpider
from ...items.footystats.league_list_items import (
    LeagueListItem,
    validate_league_list_item,
    create_league_list_item
)

class LeagueListSpider(FootyStatsBaseSpider):
    """Spider for FootyStats /league-list endpoint"""
    
    name = "footystats_league_list"
    endpoint_name = "league-list"
    allowed_domains = ["api.football-data-api.com"]
    
    def parse_data_item(self, item_data: Dict[str, Any]) -> Optional[LeagueListItem]:
        """Parse individual league from API response"""
        
        if not validate_league_list_item(item_data):
            league_name = item_data.get('name', 'Unknown')
            self.logger.warning(f"Invalid league data: {league_name}")
            return None
        
        try:
            league_item = create_league_list_item(item_data)
            
            league_name = league_item.get('name', 'Unknown')
            season_count = len(league_item.get('season', []))
            self.logger.debug(f"Processed league: {league_name} ({season_count} seasons)")
            
            return league_item
            
        except Exception as e:
            league_name = item_data.get('name', 'Unknown')
            self.logger.error(f"Error processing league {league_name}: {e}")
            return None