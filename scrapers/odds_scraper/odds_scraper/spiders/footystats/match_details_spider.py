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
    - Lineups, substitutions, and player events
    - Weather conditions and venue details
    - Comprehensive odds data from 25+ bookmakers
    
    Usage:
    scrapy crawl footystats_match_details -a match_id=579101 -O match.json
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
        
        Note: FootyStats match endpoint returns the match data directly in the 'data' field,
        not as an array like other endpoints.
        
        Args:
            item_data: Match details object from API response (single object, not array)
            
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
            
            # Log comprehensive progress
            home_team = match_item.get('home_name', 'Unknown')
            away_team = match_item.get('away_name', 'Unknown')
            home_goals = match_item.get('home_goal_count', 0)
            away_goals = match_item.get('away_goal_count', 0)
            status = match_item.get('status', 'unknown')
            season = match_item.get('season', 'Unknown')
            
            # Count nested data elements
            h2h_matches = 0
            if match_item.get('h2h'):
                h2h_data = match_item.get('h2h')
                if isinstance(h2h_data, dict):
                    prev_matches = h2h_data.get('previous_matches_results', {})
                    h2h_matches = prev_matches.get('totalMatches', 0)
            
            odds_count = 0
            if match_item.get('odds_comparison'):
                odds_comp = match_item.get('odds_comparison')
                if isinstance(odds_comp, dict) and 'FT Result' in odds_comp:
                    ft_result = odds_comp['FT Result']
                    if '1' in ft_result:
                        odds_count = len(ft_result['1'])
            
            lineup_count = 0
            if match_item.get('lineups'):
                lineups = match_item.get('lineups')
                if isinstance(lineups, dict):
                    team_a_lineup = lineups.get('team_a', [])
                    team_b_lineup = lineups.get('team_b', [])
                    lineup_count = len(team_a_lineup) + len(team_b_lineup)
            
            weather_info = ""
            if match_item.get('weather'):
                weather = match_item.get('weather')
                if isinstance(weather, dict):
                    temp = weather.get('temperature_celcius', {}).get('temp', 'N/A')
                    weather_type = weather.get('type', 'N/A')
                    weather_info = f"{temp}°C, {weather_type}"
            
            self.logger.debug(
                f"Processed match: {home_team} {home_goals}-{away_goals} {away_team} "
                f"({status}, {season}) - H2H: {h2h_matches} matches, "
                f"Odds: {odds_count} bookmakers, Lineups: {lineup_count} players"
                f"{', Weather: ' + weather_info if weather_info else ''}"
            )
            
            return match_item
            
        except Exception as e:
            self.logger.error(f"Error processing match details for match ID {self.match_id}: {e}")
            self.logger.exception("Full traceback:")
            return None