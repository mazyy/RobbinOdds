# odds_scraper/odds_scraper/spiders/odds_portal/utils/match_event_parser.py

from datetime import datetime
from typing import Dict, List, Any, Optional

from odds_scraper.items.odds_portal.items import (
    OddsItem, OutcomeItem, MarketItem, MatchEventOddsItem,
    OddsLoader, OutcomeLoader, MarketLoader, MatchEventOddsLoader,
    OUTCOME_TYPE_MAP
)

class MatchEventOddsParser:
    """Parser for match event odds data from OddsPortal API"""
    
    def __init__(self, 
                 bookmaker_names: Dict[str, str] = None,
                 betting_type_names: Dict[str, Dict] = None,
                 scope_names: Dict[str, str] = None,
                 handicap_names: Dict[str, Dict] = None,
                 is_started: bool = False):
        """
        Initialize parser with mappings
        
        Args:
            bookmaker_names: Dict mapping bookmaker IDs to names
            betting_type_names: Dict with betting type info
            scope_names: Dict mapping scope IDs to names
            handicap_names: Dict with handicap info
            is_started: Whether the match has started
        """
        self.bookmaker_names = bookmaker_names or {}
        self.betting_type_names = betting_type_names or {}
        self.scope_names = scope_names or {}
        self.handicap_names = handicap_names or {}
        self.is_started = is_started
        
    def parse_match_event_odds(self, odds_response: Dict[str, Any], 
                             match_id: str = None) -> MatchEventOddsItem:
        """
        Parse complete match event odds data from decrypted API response
        
        Args:
            odds_response: Decrypted response with 's' and 'd' fields
            match_id: Match ID from event header
            
        Returns:
            MatchEventOddsItem with all parsed data
        """
        # Check response status
        if odds_response.get('s') != 1:
            raise ValueError(f"Invalid response status: {odds_response.get('s')}")
            
        # Extract the data object
        odds_data = odds_response.get('d', {})
        
        loader = MatchEventOddsLoader()
        
        # Basic event info
        if match_id:
            loader.add_value('match_id', match_id)
        loader.add_value('encoded_event_id', odds_data.get('encodeventId'))
        
        # Add match state information - only is_started matters for pre-match
        loader.add_value('is_started', self.is_started)
        
        # Current context
        loader.add_value('current_betting_type', odds_data.get('bt'))
        loader.add_value('current_scope', odds_data.get('sc'))
        
        # Timestamp info
        time_base = odds_data.get('time-base')
        if time_base:
            loader.add_value('time_base', time_base)
            
        loader.add_value('refresh_interval', odds_data.get('refresh'))
        
        # Broken parsers
        loader.add_value('broken_parsers', odds_data.get('brokenParser', []))
        
        # Parse markets
        oddsdata = odds_data.get('oddsdata', {})
        
        back_markets = []
        lay_markets = []
        
        # Parse back markets
        back_data = oddsdata.get('back', {})
        for market_key, market_data in back_data.items():
            market_item = self._parse_market(market_data, is_back=True)
            if market_item:
                back_markets.append(market_item)
        
        # Parse lay markets  
        lay_data = oddsdata.get('lay', {})
        for market_key, market_data in lay_data.items():
            market_item = self._parse_market(market_data, is_back=False)
            if market_item:
                lay_markets.append(market_item)
        
        loader.add_value('back_markets', back_markets)
        loader.add_value('lay_markets', lay_markets)
        
        return loader.load_item()
    
    def _parse_market(self, market_data: Dict[str, Any], is_back: bool) -> Optional[MarketItem]:
        """
        Parse individual market data
        
        Args:
            market_data: Market data from API containing all the parsed values
            is_back: True for back odds, False for lay odds
            
        Returns:
            MarketItem or None if parsing fails
        """
        loader = MarketLoader()
        
        # Market identification - directly from the data
        betting_type_id = market_data.get('bettingTypeId')
        scope_id = market_data.get('scopeId')
        handicap_type_id = market_data.get('handicapTypeId')
        
        loader.add_value('betting_type_id', betting_type_id)
        
        # Get betting type name from provided mapping
        betting_type_info = self.betting_type_names.get(str(betting_type_id), {})
        betting_type_name = betting_type_info.get('name', f"Unknown_{betting_type_id}")
        loader.add_value('betting_type_name', betting_type_name)
        
        loader.add_value('scope_id', scope_id)
        loader.add_value('scope_name', self.scope_names.get(str(scope_id), f"Unknown_{scope_id}"))
        
        loader.add_value('handicap_type_id', handicap_type_id)
        
        # Get handicap type name
        if handicap_type_id == 0 or str(handicap_type_id) == "0":
            handicap_type_name = "No Handicap"
        else:
            handicap_info = self.handicap_names.get(str(handicap_type_id), {})
            handicap_type_name = handicap_info.get('Name', f"Unknown_{handicap_type_id}")
        loader.add_value('handicap_type_name', handicap_type_name)
        
        loader.add_value('handicap_value', market_data.get('handicapValue'))
        loader.add_value('mixed_parameter_id', market_data.get('mixedParameterId'))
        loader.add_value('mixed_parameter_name', market_data.get('mixedParameterName'))
        
        # Market type
        loader.add_value('is_back', is_back)
        
        # Outcome IDs
        outcome_ids = market_data.get('outcomeId', [])
        if isinstance(outcome_ids, dict):
            # Convert from dict format {"0": "id1", "1": "id2"} to list
            outcome_ids = [outcome_ids.get(str(i)) for i in sorted(map(int, outcome_ids.keys()))]
        loader.add_value('outcome_ids', outcome_ids)
        
        # Parse outcomes from history
        outcomes = self._parse_outcomes(market_data, betting_type_id, outcome_ids)
        loader.add_value('outcomes', outcomes)
        
        return loader.load_item()
    
    def _parse_outcomes(self, market_data: Dict[str, Any], 
                       betting_type_id: int, 
                       outcome_ids: List[str]) -> List[OutcomeItem]:
        """
        Parse outcomes from market history data and current odds
        
        Args:
            market_data: Market data containing history, odds, volume, and changeTime
            betting_type_id: Betting type ID for outcome type mapping
            outcome_ids: List of outcome IDs
            
        Returns:
            List of OutcomeItem objects
        """
        outcomes = []
        history_data = market_data.get('history', {})
        current_odds = market_data.get('odds', {})
        current_volume = market_data.get('volume', {})
        change_times = market_data.get('changeTime', {})
        
        # For lay odds, the structure is different - handle it separately
        if not current_odds and history_data:
            # Handle lay odds structure where we only have history data
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
        
        # For back odds with current odds data
        # Get all bookmaker IDs from both current odds and history
        all_bookmaker_ids = set()
        if current_odds:
            all_bookmaker_ids.update(current_odds.keys())
        for outcome_history in history_data.values():
            all_bookmaker_ids.update(outcome_history.keys())
        
        for bookmaker_id in all_bookmaker_ids:
            bookmaker_current_odds = current_odds.get(bookmaker_id, {})
            bookmaker_current_volume = current_volume.get(bookmaker_id, {})
            bookmaker_change_times = change_times.get(bookmaker_id, {})
            
            for position, outcome_id in enumerate(outcome_ids):
                if not outcome_id:
                    continue
                
                # Build odds history list
                combined_odds_history = []
                
                # First add historical odds (opening odds)
                if outcome_id in history_data:
                    historical_odds = history_data[outcome_id].get(bookmaker_id, [])
                    combined_odds_history.extend(historical_odds)
                
                # Then add current odds as last item if available
                position_str = str(position)
                current_odds_value = None
                current_volume_value = 0
                current_timestamp = 0
                
                # Check if bookmaker has current odds
                if bookmaker_current_odds:
                    # Handle dict format: {"0": 1.33, "1": 3.4}
                    if isinstance(bookmaker_current_odds, dict) and position_str in bookmaker_current_odds:
                        current_odds_value = bookmaker_current_odds[position_str]
                        if isinstance(bookmaker_current_volume, dict):
                            current_volume_value = bookmaker_current_volume.get(position_str, 0)
                        if isinstance(bookmaker_change_times, dict):
                            current_timestamp = bookmaker_change_times.get(position_str, 0)
                    # Handle array format: [1.33, 3.4]
                    elif isinstance(bookmaker_current_odds, list) and position < len(bookmaker_current_odds):
                        current_odds_value = bookmaker_current_odds[position]
                        if isinstance(bookmaker_current_volume, list) and position < len(bookmaker_current_volume):
                            current_volume_value = bookmaker_current_volume[position]
                        if isinstance(bookmaker_change_times, list) and position < len(bookmaker_change_times):
                            current_timestamp = bookmaker_change_times[position]
                    
                    # Add current odds entry if we have the odds value
                    if current_odds_value is not None:
                        current_entry = [current_odds_value, current_volume_value, current_timestamp]
                        combined_odds_history.append(current_entry)
                
                # Only create outcome if we have any odds data
                if combined_odds_history:
                    outcome_item = self._parse_outcome(
                        bookmaker_id=bookmaker_id,
                        outcome_id=outcome_id,
                        position=position,
                        betting_type_id=betting_type_id,
                        odds_history=combined_odds_history
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
def parse_match_event_odds(odds_response: Dict[str, Any], 
                          match_id: str = None,
                          bookmaker_names: Dict[str, str] = None,
                          betting_type_names: Dict[str, Dict] = None,
                          scope_names: Dict[str, str] = None,
                          handicap_names: Dict[str, Dict] = None,
                          is_started: bool = False) -> MatchEventOddsItem:
    """
    Convenience function to parse match event odds data
    
    Args:
        odds_response: Decrypted response with 's' and 'd' fields
        match_id: Match ID from event header
        bookmaker_names: Bookmaker ID to name mapping
        betting_type_names: Betting type info
        scope_names: Scope ID to name mapping
        handicap_names: Handicap info
        is_started: Whether the match has started
        
    Returns:
        MatchEventOddsItem with parsed data
    """
    parser = MatchEventOddsParser(
        bookmaker_names=bookmaker_names,
        betting_type_names=betting_type_names,
        scope_names=scope_names,
        handicap_names=handicap_names,
        is_started=is_started
    )
    return parser.parse_match_event_odds(odds_response, match_id)