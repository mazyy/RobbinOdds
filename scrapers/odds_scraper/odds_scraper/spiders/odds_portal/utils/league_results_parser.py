from typing import Dict, List, Any, Optional
from scrapers.odds_scraper.odds_scraper.items.odds_portal.league_items import (
    MatchResultItem, OddsSummaryItem, LeagueResultsPageItem,
    MatchResultLoader, OddsSummaryLoader, LeagueResultsPageLoader
)

class LeagueResultsParser:
    """Parser for league results data from OddsPortal AJAX response"""
    
    def __init__(self, tournament_id: str = None, tournament_name: str = None, 
                 season: str = None):
        """
        Initialize parser with league info
        
        Args:
            tournament_id: Tournament ID
            tournament_name: Tournament name (e.g., "NBA")
            season: Season string (e.g., "2024-2025")
        """
        self.tournament_id = tournament_id
        self.tournament_name = tournament_name
        self.season = season
    
    def parse_results_page(self, response_data: Dict[str, Any]) -> LeagueResultsPageItem:
        """
        Parse a page of league results from AJAX response
        
        Args:
            response_data: Decrypted response with 's' and 'd' fields
            
        Returns:
            LeagueResultsPageItem with all matches
        """
        # Check response status
        if response_data.get('s') != 1:
            raise ValueError(f"Invalid response status: {response_data.get('s')}")
        
        data = response_data.get('d', {})
        
        # Create page loader
        page_loader = LeagueResultsPageLoader()
        
        # Basic page info
        page_loader.add_value('tournament_id', self.tournament_id)
        page_loader.add_value('tournament_name', self.tournament_name)
        page_loader.add_value('season', self.season)
        
        # Pagination info
        page_loader.add_value('page_number', data.get('page'))
        page_loader.add_value('total_matches', data.get('total'))
        page_loader.add_value('matches_per_page', data.get('onePage'))
        
        # Calculate total pages and has_next
        pagination = data.get('pagination', {})
        page_loader.add_value('total_pages', pagination.get('pageCount'))
        page_loader.add_value('has_next_page', pagination.get('hasPagination', False))
        
        # Parse all matches
        matches = []
        rows = data.get('rows', [])
        
        for row in rows:
            match_item = self._parse_match_result(row)
            if match_item:
                matches.append(match_item)
        
        page_loader.add_value('matches', matches)
        
        return page_loader.load_item()
    
    def _parse_match_result(self, match_data: Dict[str, Any]) -> Optional[MatchResultItem]:
        """
        Parse individual match result
        
        Args:
            match_data: Match data from rows array
            
        Returns:
            MatchResultItem or None if parsing fails
        """
        loader = MatchResultLoader()
        
        # Match identification
        loader.add_value('match_id', match_data.get('encodeEventId'))
        loader.add_value('encoded_event_id', match_data.get('encodeEventId'))
        loader.add_value('match_url', match_data.get('url'))
        
        # Teams
        loader.add_value('home_team_name', match_data.get('home-name'))
        loader.add_value('away_team_name', match_data.get('away-name'))
        loader.add_value('home_team_id', match_data.get('home'))
        loader.add_value('away_team_id', match_data.get('away'))
        loader.add_value('home_country', match_data.get('home-country-two-chart-name'))
        loader.add_value('away_country', match_data.get('away-country-two-chart-name'))
        
        # Match status
        loader.add_value('status_id', match_data.get('status-id'))
        loader.add_value('event_stage_id', match_data.get('event-stage-id'))
        loader.add_value('event_stage_name', match_data.get('event-stage-name'))
        loader.add_value('is_finished', match_data.get('status-id'))  # Will be converted to bool
        loader.add_value('is_after_extra_time', match_data.get('event-stage-id'))  # Will be converted to bool
        
        # Tournament info
        loader.add_value('tournament_id', match_data.get('tournament-id'))
        loader.add_value('tournament_name', match_data.get('tournament-name'))
        loader.add_value('tournament_stage_id', match_data.get('tournament-stage-id'))
        loader.add_value('tournament_stage_name', match_data.get('tournament-stage-name'))
        loader.add_value('sport_id', match_data.get('sport-id'))
        loader.add_value('sport_name', 'Basketball')  # You can map from sport-id if needed
        loader.add_value('country_name', match_data.get('country-name'))
        
        # Scores
        loader.add_value('final_score', match_data.get('result'))
        loader.add_value('home_score', match_data.get('homeResult'))
        loader.add_value('away_score', match_data.get('awayResult'))
        loader.add_value('partial_scores', match_data.get('partialresult'))
        
        # Winner
        loader.add_value('home_winner_status', match_data.get('home-winner'))
        loader.add_value('away_winner_status', match_data.get('away-winner'))
        
        # Match timing
        loader.add_value('match_timestamp', match_data.get('date-start-timestamp'))
        
        # Venue
        loader.add_value('venue', match_data.get('venue'))
        loader.add_value('venue_town', match_data.get('venueTown'))
        loader.add_value('venue_country', match_data.get('venueCountry'))
        
        # Bookmakers count
        loader.add_value('bookmakers_count', match_data.get('bookmakersCount'))
        
        # Parse odds summary
        odds_summary = self._parse_odds_summary(match_data.get('odds', []))
        loader.add_value('odds_summary', odds_summary)
        
        # Additional info
        match_info = match_data.get('info', [])
        if match_info and isinstance(match_info, list):
            # Extract just the name field from each info item
            info_texts = [info.get('name') for info in match_info if info.get('name')]
            loader.add_value('match_info', info_texts)
        
        return loader.load_item()
    
    def _parse_odds_summary(self, odds_data: List[Dict[str, Any]]) -> List[OddsSummaryItem]:
        """
        Parse odds summary data
        
        Args:
            odds_data: List of odds summary entries
            
        Returns:
            List of OddsSummaryItem objects
        """
        odds_items = []
        
        for odds_entry in odds_data:
            loader = OddsSummaryLoader()
            
            loader.add_value('event_id', odds_entry.get('eventId'))
            loader.add_value('outcome_id', odds_entry.get('outcomeId'))
            loader.add_value('outcome_result_id', odds_entry.get('outcomeResultId'))
            loader.add_value('betting_type_id', odds_entry.get('bettingTypeId'))
            loader.add_value('scope_id', odds_entry.get('scopeId'))
            loader.add_value('avg_odds', odds_entry.get('avgOdds'))
            loader.add_value('max_odds', odds_entry.get('maxOdds'))
            loader.add_value('max_odds_provider_id', odds_entry.get('maxOddsProviderId'))
            loader.add_value('is_active', odds_entry.get('active'))
            loader.add_value('active_bookmakers_count', odds_entry.get('cntActive'))
            
            odds_items.append(loader.load_item())
        
        return odds_items

# Helper function for use in spider
def parse_league_results_page(response_data: Dict[str, Any],
                             tournament_id: str = None,
                             tournament_name: str = None,
                             season: str = None) -> LeagueResultsPageItem:
    """
    Convenience function to parse league results page
    
    Args:
        response_data: Decrypted response with 's' and 'd' fields
        tournament_id: Tournament ID
        tournament_name: Tournament name
        season: Season string
        
    Returns:
        LeagueResultsPageItem with parsed data
    """
    parser = LeagueResultsParser(
        tournament_id=tournament_id,
        tournament_name=tournament_name,
        season=season
    )
    return parser.parse_results_page(response_data)