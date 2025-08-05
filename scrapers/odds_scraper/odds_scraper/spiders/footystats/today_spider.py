from typing import Dict, Any, Optional
from .base_spider import FootyStatsBaseSpider
from ...items.footystats.today_items import (
    TodayMatchItem,
    validate_today_match_item,
    create_today_match_item
)

class TodaySpider(FootyStatsBaseSpider):
    """
    Spider for FootyStats /today endpoint
    
    Extracts matches scheduled for today or a specific date with:
    - Match ID and basic details
    - Team names and IDs
    - Competition information
    - Match timing and status
    
    Usage:
    scrapy crawl footystats_today -O today_matches.json
    scrapy crawl footystats_today -a api_key=your_key
    scrapy crawl footystats_today -a date=2024-08-03
    scrapy crawl footystats_today -a timezone=1
    """
    
    name = "footystats_today"
    endpoint_name = "today"
    allowed_domains = ["api.football-data-api.com"]
    
    def __init__(self, api_key: str = "example", date: str = None, 
                 timezone: str = "0", **kwargs):
        """
        Initialize today spider with optional parameters
        
        Args:
            api_key: FootyStats API key
            date: Date in YYYY-MM-DD format (optional, defaults to today)
            timezone: Timezone offset (optional, default: "0")
        """
        super().__init__(api_key=api_key, **kwargs)
        
        self.date = date
        self.timezone = timezone
        
        self.logger.info(f"Today spider initialized - Date: {date or 'today'}, Timezone: {timezone}")
    
    def get_request_params(self) -> Dict[str, Any]:
        """Build request parameters for today endpoint"""
        params = {}
        
        if self.date:
            params['date'] = self.date
            
        if self.timezone != "0":
            params['timezone'] = self.timezone
            
        return params
    
    def parse_data_item(self, item_data: Dict[str, Any]) -> Optional[TodayMatchItem]:
        """
        Parse individual match from API response
        
        Args:
            item_data: Single match object from data[] array
            
        Returns:
            TodayMatchItem or None if invalid
        """
        # Validate match data
        if not validate_today_match_item(item_data):
            match_info = f"{item_data.get('home_name', 'Unknown')} vs {item_data.get('away_name', 'Unknown')}"
            self.logger.warning(f"Invalid match data: {match_info}")
            return None
        
        try:
            # Create match item using helper function
            match_item = create_today_match_item(item_data)
            
            # Log progress
            match_info = f"{match_item.get('home_name')} vs {match_item.get('away_name')}"
            competition = match_item.get('competition_name', 'Unknown')
            self.logger.debug(f"Processed match: {match_info} ({competition})")
            
            return match_item
            
        except Exception as e:
            match_info = f"{item_data.get('home_name', 'Unknown')} vs {item_data.get('away_name', 'Unknown')}"
            self.logger.error(f"Error processing match {match_info}: {e}")
            return None