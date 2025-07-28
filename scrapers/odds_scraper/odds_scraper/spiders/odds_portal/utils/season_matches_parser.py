from typing import Dict, List, Any, Optional
from odds_scraper.items.odds_portal.league_items import (
    MatchInfoItem, SeasonMatchesItem,
    MatchInfoLoader, SeasonMatchesLoader
)
from datetime import datetime

class SeasonMatchesParser:
    """Parser for season match data from OddsPortal AJAX responses"""
    
    def __init__(self, league_id: str, league_name: str, season_id: str,
                 sport_id: str, sport_name: str, country_name: str):
        """
        Initialize parser with season context
        
        Args:
            league_id: League identifier
            league_name: League display name
            season_id: Season identifier (e.g., "2023-2024" or "current")
            sport_id: Sport ID
            sport_name: Sport name
            country_name: Country name
        """
        self.league_id = league_id
        self.league_name = league_name
        self.season_id = season_id
        self.sport_id = sport_id
        self.sport_name = sport_name
        self.country_name = country_name
    
    def parse_matches_page(self, response_data: Dict[str, Any], 
                          extraction_type: str = "results",
                          source_url: str = None) -> SeasonMatchesItem:
        """
        Parse a page of matches from AJAX response
        
        Args:
            response_data: Decrypted response with 's' and 'd' fields
            extraction_type: "results" for past matches, "fixtures" for upcoming
            source_url: URL that generated this response
            
        Returns:
            SeasonMatchesItem with all matches
        """
        # Check response status
        if response_data.get('s') != 1:
            raise ValueError(f"Invalid response status: {response_data.get('s')}")
        
        data = response_data.get('d', {})
        
        # Create page loader
        loader = SeasonMatchesLoader()
        
        # Season identification
        loader.add_value('league_id', self.league_id)
        loader.add_value('league_name', self.league_name)
        loader.add_value('season_id', self.season_id)
        loader.add_value('sport_id', self.sport_id)
        loader.add_value('sport_name', self.sport_name)
        loader.add_value('country_name', self.country_name)
        
        # Extraction info
        loader.add_value('extraction_type', extraction_type)
        loader.add_value('page_number', data.get('page'))
        loader.add_value('source_url', source_url)
        loader.add_value('extraction_timestamp', None)  # Will use current time
        
        # Pagination info
        pagination = data.get('pagination', {})
        loader.add_value('total_pages', pagination.get('pageCount'))
        loader.add_value('has_next_page', pagination.get('hasPagination', False))
        
        # Parse matches
        matches = []
        rows = data.get('rows', [])
        
        for row in rows:
            match_item = self._parse_match_info(row)
            if match_item:
                matches.append(match_item)
        
        loader.add_value('matches', matches)
        loader.add_value('total_matches', len(matches))
        
        return loader.load_item()
    
    def _parse_match_info(self, match_data: Dict[str, Any]) -> Optional[MatchInfoItem]:
        """
        Parse minimal match information
        
        Args:
            match_data: Match data from rows array
            
        Returns:
            MatchInfoItem or None if parsing fails
        """
        # Skip if no match ID
        match_id = match_data.get('encodeEventId')
        if not match_id:
            return None
        
        loader = MatchInfoLoader()
        
        # Essential identifiers
        loader.add_value('match_id', match_id)
        
        # Build full match URL
        match_url = match_data.get('url', '')
        if match_url and not match_url.startswith('http'):
            match_url = f"https://www.oddsportal.com{match_url}"
        loader.add_value('match_url', match_url)
        
        # Timing
        timestamp = match_data.get('date-start-timestamp')
        loader.add_value('match_timestamp', timestamp)
        
        # Status - will be converted by processor
        status_id = match_data.get('status-id')
        loader.add_value('status', status_id)
        
        # Teams
        loader.add_value('home_team', match_data.get('home-name'))
        loader.add_value('away_team', match_data.get('away-name'))
        
        # Context
        loader.add_value('league_id', self.league_id)
        loader.add_value('league_name', self.league_name)
        loader.add_value('season_id', self.season_id)
        loader.add_value('sport_id', self.sport_id)
        loader.add_value('tournament_stage', match_data.get('tournament-stage-name'))
        
        # Metadata
        loader.add_value('extracted_at', None)  # Will use current time
        
        return loader.load_item()

# Helper function for use in season spider
def parse_season_matches(response_data: Dict[str, Any],
                        league_id: str,
                        league_name: str,
                        season_id: str,
                        sport_id: str,
                        sport_name: str,
                        country_name: str,
                        extraction_type: str = "results",
                        source_url: str = None) -> SeasonMatchesItem:
    """
    Convenience function to parse season matches
    
    Args:
        response_data: Decrypted response
        league_id: League identifier
        league_name: League name
        season_id: Season ID
        sport_id: Sport ID
        sport_name: Sport name
        country_name: Country name
        extraction_type: "results" or "fixtures"
        source_url: Source URL
        
    Returns:
        SeasonMatchesItem with parsed data
    """
    parser = SeasonMatchesParser(
        league_id=league_id,
        league_name=league_name,
        season_id=season_id,
        sport_id=sport_id,
        sport_name=sport_name,
        country_name=country_name
    )
    return parser.parse_matches_page(response_data, extraction_type, source_url)