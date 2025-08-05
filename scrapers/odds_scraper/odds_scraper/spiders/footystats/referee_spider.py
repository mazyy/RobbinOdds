from typing import Dict, Any, Optional
from .base_spider import FootyStatsBaseSpider
from ...items.footystats.referee_items import (
    RefereeItem,
    validate_referee_item,
    create_referee_item
)

class RefereeSpider(FootyStatsBaseSpider):
    """
    Spider for FootyStats /referee endpoint
    
    Extracts detailed statistics for a specific referee across all competitions:
    - Basic referee information (name, age, nationality)
    - Career statistics across all competitions and seasons
    - Season-by-season breakdown
    - Match statistics (goals, cards, penalties)
    - Performance indicators (BTTS, win percentages)
    
    Usage:
    scrapy crawl footystats_referee -a referee_id=393 -O referee.json
    scrapy crawl footystats_referee -a api_key=your_key -a referee_id=125
    """
    
    name = "footystats_referee"
    endpoint_name = "referee"
    allowed_domains = ["api.football-data-api.com"]
    
    def __init__(self, api_key: str = "example", referee_id: str = None, **kwargs):
        """
        Initialize referee spider
        
        Args:
            api_key: FootyStats API key
            referee_id: Referee ID to retrieve detailed statistics for (required)
        """
        super().__init__(api_key=api_key, **kwargs)
        
        if not referee_id:
            raise ValueError("referee_id parameter is required")
        
        self.referee_id = referee_id
        
        self.logger.info(f"Referee spider initialized - Referee ID: {referee_id}")
    
    def get_request_params(self) -> Dict[str, Any]:
        """Build request parameters for referee endpoint"""
        return {
            'referee_id': self.referee_id
        }
    
    def parse_data_item(self, item_data: Dict[str, Any]) -> Optional[RefereeItem]:
        """
        Parse referee data from API response
        
        Args:
            item_data: Single referee object from data[] array
            
        Returns:
            RefereeItem or None if invalid
        """
        # Validate referee data
        if not validate_referee_item(item_data):
            referee_name = item_data.get('full_name', 'Unknown')
            self.logger.warning(f"Invalid referee data: {referee_name}")
            return None
        
        try:
            # Create referee item using helper function
            referee_item = create_referee_item(item_data)
            
            # Log progress
            referee_name = referee_item.get('full_name', 'Unknown')
            nationality = referee_item.get('nationality', 'Unknown')
            age = referee_item.get('age', 'Unknown')
            career_appearances = referee_item.get('career_appearances', 0)
            career_goals_per_match = referee_item.get('career_goals_per_match', 0)
            seasons_count = len(referee_item.get('seasons', []))
            
            self.logger.debug(f"Processed referee: {referee_name} ({nationality}, {age}y) - {career_appearances} career apps, {career_goals_per_match:.2f} goals/match across {seasons_count} seasons")
            
            return referee_item
            
        except Exception as e:
            referee_name = item_data.get('full_name', 'Unknown')
            self.logger.error(f"Error processing referee {referee_name}: {e}")
            return None