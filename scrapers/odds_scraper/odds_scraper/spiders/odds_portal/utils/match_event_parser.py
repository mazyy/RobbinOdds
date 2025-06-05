# odds_scraper/odds_scraper/spiders/odds_portal/match_event_parser.py

import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

from odds_scraper.items.odds_portal.items import (
    OddsItem, OutcomeItem, MarketItem, MatchEventOddsItem,
    OddsLoader, OutcomeLoader, MarketLoader, MatchEventOddsLoader,
    BETTING_TYPE_NAMES, SCOPE_NAMES, OUTCOME_TYPE_MAP
)

class MatchEventOddsParser:
    """Parser for match event odds data from OddsPortal API"""
    
    def __init__(self, bookmaker_names: Dict[str, str] = None):
        """
        Initialize parser with optional bookmaker names mapping
        
        Args:
            bookmaker_names: Dict mapping bookmaker IDs to names
        """
        self.bookmaker_names = bookmaker_names
        
    def parse_match_event_odds(self, odds_data: Dict[str, Any], 
                             match_id: str = None, 
                             time_base: int = None) -> MatchEventOddsItem:
        """
        Parse complete match event odds data
        
        Args:
            odds_data: Raw odds data from API (the 'd' object)
            match_id: Match ID from event header
            time_base: Base timestamp for calculations
            
        Returns:
            MatchEventOddsItem with all parsed data
        """
        loader = MatchEventOddsLoader()
        
        # Basic event info
        if match_id:
            loader.add_value('match_id', match_id)
        loader.add_value('encoded_event_id', odds_data.get('encodeventId'))
        
        # Current context
        loader.add_value('current_betting_type', odds_data.get('bt'))
        loader.add_value('current_scope', odds_data.get('sc'))
        
        # Timestamp info
        api_time_base = odds_data.get('time-base')
        if api_time_base:
            loader.add_value('time_base', api_time_base)
        elif time_base:
            loader.add_value('time_base', time_base)
            
        loader.add_value('refresh_interval', odds_data.get('refresh'))
        
        # Navigation and broken parsers
        loader.add_value('available_markets', odds_data.get('nav', {}))
        loader.add_value('broken_parsers', odds_data.get('brokenParser', []))
        
        # Parse markets
        oddsdata = odds_data.get('oddsdata', {})
        
        back_markets = []
        lay_markets = []
        
        # Parse back markets
        back_data = oddsdata.get('back', {})
        for market_key, market_data in back_data.items():
            market_item = self._parse_market(market_key, market_data, is_back=True)
            if market_item:
                back_markets.append(market_item)
        
        # Parse lay markets  
        lay_data = oddsdata.get('lay', {})
        for market_key, market_data in lay_data.items():
            market_item = self._parse_market(market_key, market_data, is_back=False)
            if market_item:
                lay_markets.append(market_item)
        
        loader.add_value('back_markets', back_markets)
        loader.add_value('lay_markets', lay_markets)
        
        return loader.load_item()
    
    def _parse_market_key(self, market_key: str) -> Optional[Tuple[int, int, int, float, int]]:
        """
        Parse market key pattern: E-[bt]-[sc]-[ht]-[hv]-[mp]
        
        Returns:
            Tuple of (betting_type_id, scope_id, handicap_type_id, handicap_value, mixed_parameter_id)
        """
        pattern = r'E-(\d+)-(\d+)-(\d+)-([\d.]+)-(\d+)'
        match = re.match(pattern, market_key)
        
        if not match:
            return None
            
        try:
            return (
                int(match.group(1)),    # betting_type_id
                int(match.group(2)),    # scope_id
                int(match.group(3)),    # handicap_type_id
                float(match.group(4)),  # handicap_value
                int(match.group(5))     # mixed_parameter_id
            )
        except (ValueError, TypeError):
            return None
    
    def _parse_market(self, market_key: str, market_data: Dict[str, Any], 
                     is_back: bool) -> Optional[MarketItem]:
        """
        Parse individual market data
        
        Args:
            market_key: Market identifier (e.g., "E-1-2-0-0-0")
            market_data: Market data from API
            is_back: True for back odds, False for lay odds
            
        Returns:
            MarketItem or None if parsing fails
        """
        # Parse market key
        parsed_key = self._parse_market_key(market_key)
        if not parsed_key:
            return None
            
        betting_type_id, scope_id, handicap_type_id, handicap_value, mixed_parameter_id = parsed_key
        
        loader = MarketLoader()
        
        # Market identification
        loader.add_value('betting_type_id', betting_type_id)
        loader.add_value('betting_type_name', BETTING_TYPE_NAMES.get(betting_type_id, f"Unknown_{betting_type_id}"))
        loader.add_value('scope_id', scope_id)
        loader.add_value('scope_name', SCOPE_NAMES.get(scope_id, f"Unknown_{scope_id}"))
        loader.add_value('handicap_type_id', handicap_type_id)
        loader.add_value('handicap_value', handicap_value)
        loader.add_value('mixed_parameter_id', mixed_parameter_id)
        loader.add_value('mixed_parameter_name', market_data.get('mixedParameterName'))
        
        # Market type
        loader.add_value('is_back', is_back)
        
        # Outcome IDs
        outcome_ids = market_data.get('outcomeId', [])
        if isinstance(outcome_ids, dict):
            # Convert from dict format {"0": "id1", "1": "id2"} to list
            outcome_ids = [outcome_ids.get(str(i)) for i in sorted(map(int, outcome_ids.keys()))]
        loader.add_value('outcome_ids', outcome_ids)
        
        # Parse outcomes
        outcomes = self._parse_outcomes(market_data, betting_type_id, outcome_ids)
        loader.add_value('outcomes', outcomes)
        
        return loader.load_item()
    
    def _parse_outcomes(self, market_data: Dict[str, Any], 
                       betting_type_id: int, 
                       outcome_ids: List[str]) -> List[OutcomeItem]:
        """
        Parse outcomes from market history data
        
        Args:
            market_data: Market data containing history
            betting_type_id: Betting type ID for outcome type mapping
            outcome_ids: List of outcome IDs
            
        Returns:
            List of OutcomeItem objects
        """
        outcomes = []
        history_data = market_data.get('history', {})
        
        for position, outcome_id in enumerate(outcome_ids):
            if not outcome_id or outcome_id not in history_data:
                continue
                
            outcome_history = history_data[outcome_id]
            
            for bookmaker_id, odds_history in outcome_history.items():
                if not odds_history:
                    continue
                    
                outcome_item = self._parse_outcome(
                    bookmaker_id=bookmaker_id,
                    outcome_id=outcome_id,
                    position=position,
                    betting_type_id=betting_type_id,
                    odds_history=odds_history
                )
                
                if outcome_item:
                    outcomes.append(outcome_item)
        
        return outcomes
    
    def _parse_outcome(self, bookmaker_id: str, outcome_id: str, 
                      position: int, betting_type_id: int, 
                      odds_history: List[List]) -> Optional[OutcomeItem]:
        """
        Parse single outcome data
        
        Args:
            bookmaker_id: Bookmaker ID
            outcome_id: Outcome ID from API
            position: Position in outcome array
            betting_type_id: Betting type for outcome type mapping
            odds_history: List of [odds, volume, timestamp] entries
            
        Returns:
            OutcomeItem or None if parsing fails
        """
        if not odds_history:
            return None
            
        loader = OutcomeLoader()
        
        # Basic info
        loader.add_value('bookmaker_id', bookmaker_id)
        loader.add_value('bookmaker_name', self.bookmaker_names.get(bookmaker_id, f"Bookmaker_{bookmaker_id}"))
        loader.add_value('outcome_id', outcome_id)
        loader.add_value('outcome_position', position)
        
        # Determine outcome type
        outcome_type_map = OUTCOME_TYPE_MAP.get(betting_type_id, {})
        outcome_type = outcome_type_map.get(position, f"outcome_{position}")
        loader.add_value('outcome_type', outcome_type)
        
        # Parse odds history
        parsed_odds = []
        for entry in odds_history:
            if len(entry) >= 3:
                odds_item = self._parse_odds_entry(entry)
                if odds_item:
                    parsed_odds.append(odds_item)
        
        loader.add_value('odds_history', parsed_odds)
        
        return loader.load_item()
    
    def _parse_odds_entry(self, entry: List) -> Optional[OddsItem]:
        """
        Parse single odds entry: [odds_value, volume, timestamp]
        
        Args:
            entry: List containing [odds_value, volume, timestamp]
            
        Returns:
            OddsItem or None if parsing fails
        """
        if len(entry) < 3:
            return None
            
        try:
            loader = OddsLoader()
            loader.add_value('odds_value', entry[0])
            loader.add_value('volume', entry[1])
            loader.add_value('timestamp', entry[2])
            
            return loader.load_item()
        except (ValueError, TypeError, IndexError):
            return None

# Helper function for use in spider
def parse_match_event_odds(odds_data: Dict[str, Any], 
                          match_id: str = None,
                          time_base: int = None,
                          bookmaker_names: Dict[str, str] = None) -> MatchEventOddsItem:
    """
    Convenience function to parse match event odds data
    
    Args:
        odds_data: Raw odds data from API
        match_id: Match ID from event header
        time_base: Base timestamp
        bookmaker_names: Bookmaker ID to name mapping
        
    Returns:
        MatchEventOddsItem with parsed data
    """
    parser = MatchEventOddsParser(bookmaker_names=bookmaker_names)
    return parser.parse_match_event_odds(odds_data, match_id, time_base)