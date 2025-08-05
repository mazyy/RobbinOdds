from typing import Dict, Any, Optional
from .base_spider import FootyStatsBaseSpider
from ...items.footystats.match_details_items import (
    MatchDetailsItem,
    validate_match_details_item,
    create_match_details_item
)

class MatchDetailsSpider(FootyStatsBaseSpider):
    """
    Spider for FootyStats /match endpoint
    
    Extracts detailed match information including:
    - Complete match statistics
    - Head-to-head data between teams
    - Pre-match odds comparison from multiple bookmakers
    - Pre-match team statistics and form
    
    Usage:
    scrapy crawl footystats_match_details -a match_id=617749 -O match.json
    scrapy crawl footystats_match_details -a api_key=your_key -a match_id=453873
    """
    
    name = "footystats_match_details"
    endpoint_name = "match"
    allowed_domains = ["api.football-data-api.com"]
    
    def __init__(self, api_key: str = "example", match_id: str = None, **kwargs):
        """
        Initialize match details spider
        
        Args:
            api_key: FootyStats API key
            match_id: Match ID to retrieve detailed information for (required)
        """
        super().__init__(api_key=api_key, **kwargs)
        
        if not match_id:
            raise ValueError("match_id parameter is required")
        
        self.match_id = match_id
        
        self.logger.info(f"Match details spider initialized - Match ID: {match_id}")
    
    def get_request_params(self) -> Dict[str, Any]:
        """Build request parameters for match endpoint"""
        return {
            'match_id': self.match_id
        }
    
    def parse_data_item(self, item_data: Dict[str, Any]) -> Optional[MatchDetailsItem]:
        """
        Parse match details from API response
        
        Args:
            item_data: Match details object from API response
            
        Returns:
            MatchDetailsItem or None if invalid
        """
        # Validate match details data
        if not validate_match_details_item(item_data):
            self.logger.warning(f"Invalid match details data for match ID: {self.match_id}")
            return None
        
        try:
            # Create match details item using helper function
            match_item = create_match_details_item(item_data)
            
            # Log progress
            home_team = match_item.get('home_name', 'Unknown')
            away_team = match_item.get('away_name', 'Unknown')
            home_goals = match_item.get('homeGoalCount', 0)
            away_goals = match_item.get('awayGoalCount', 0)
            status = match_item.get('status', 'unknown')
            h2h_count = match_item.get('h2h_matches_count', 0)
            odds_count = match_item.get('odds_count', 0)
            
            self.logger.debug(f"Processed match: {home_team} {home_goals}-{away_goals} {away_team} ({status}) - H2H: {h2h_count} matches, Odds: {odds_count} bookmakers")
            
            return match_item
            
        except Exception as e:
            self.logger.error(f"Error processing match details for match ID {self.match_id}: {e}")
            return None