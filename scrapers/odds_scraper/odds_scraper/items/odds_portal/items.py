from scrapy import Item, Field
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst
from datetime import datetime

def convert_unix_timestamp(timestamp, time_base=None):
    """Convert UNIX timestamp to datetime object"""
    try:
        if isinstance(timestamp, (int, float)):
            return datetime.fromtimestamp(timestamp)
        return None
    except (ValueError, TypeError):
        return None

def convert_odds_value(value):
    """Convert odds value to float"""
    try:
        return float(value) if value is not None else None
    except (ValueError, TypeError):
        return None

def convert_volume(value):
    """Convert volume to integer"""
    try:
        return int(value) if value is not None else None
    except (ValueError, TypeError):
        return None
    
# -------------------- Items --------------------
class PageVarItem(Item):
    default_betting_type = Field()
    default_scope = Field()
    nav = Field()
    nav_filtered = Field()

class EventHeaderItem(Item):
    match_id = Field()
    xhash = Field()
    xhashf = Field()
    is_live = Field()
    real_live = Field()
    is_postponed = Field()
    is_started = Field()
    is_finished = Field()
    is_finished_grace_period = Field()
    sport_id = Field()
    sport_name = Field()
    sport_url = Field()
    home = Field()
    away = Field()
    tournament_id = Field()
    tournament_name = Field()
    tournament_url = Field()
    country_name = Field()
    default_bet_id = Field()
    user_bett_id = Field()
    user_id = Field()
    default_scope_id = Field()
    version_id = Field()

class EventBodyItem(Item):
    start_date = Field()
    end_date = Field()
    home_result = Field()
    away_result = Field()
    partial_result = Field()
    event_stage_name = Field()
    event_stage_id = Field()
    ft_only = Field()
    ft_only_text = Field()
    ft_only_text_short = Field()
    venue = Field()
    venue_town = Field()
    venue_country = Field()
    additional_odds_info = Field()
    providers_names = Field()
    providers_is_betting_exchange = Field()
    request_pre_match = Field()
    request_base_pre_match = Field()
    update_score_request = Field()
    updatescore_request_base = Field()
    request_match_facts = Field()
    request_event_data = Field()
    request_last_results = Field()
    request_betting_exchanges = Field()

class OddsItem(Item):
    """Single odds entry: [odds_value, volume, timestamp]"""
    odds_value = Field()  # float
    volume = Field()      # int 
    timestamp = Field()   # datetime object

class OutcomeItem(Item):
    """Odds for one outcome from one bookmaker"""
    bookmaker_id = Field()
    bookmaker_name = Field()
    outcome_id = Field()        # Original outcome ID from API (e.g., "8c1rjxv464x0xn0qq1")
    outcome_position = Field()  # Position in the outcomeId array (0, 1, 2, etc.)
    outcome_type = Field()      # "home", "draw", "away", etc. (derived from position + betting_type)
    odds_history = Field()      # List of OddsItem

class MarketItem(Item):
    """Market odds following the E-[bt]-[sc]-[ht]-[hv]-[mp] pattern"""
    # Market identification (from the key pattern)
    betting_type_id = Field()
    betting_type_name = Field()
    scope_id = Field() 
    scope_name = Field()
    handicap_type_id = Field()
    handicap_value = Field()
    mixed_parameter_id = Field()
    mixed_parameter_name = Field()
    
    # Market type
    is_back = Field()  # True for back odds, False for lay odds
    
    # Outcome mappings (from outcomeId array)
    outcome_ids = Field()       # List of outcome IDs from the API
    
    # All outcomes data
    outcomes = Field()  # List of OutcomeItem

class MatchEventOddsItem(Item):
    """Top-level match event odds data"""
    # Event identification
    match_id = Field()
    encoded_event_id = Field()
    
    # Current context
    current_betting_type = Field()
    current_scope = Field()
    
    # Timestamp info
    time_base = Field()
    refresh_interval = Field()
    
    # Navigation structure
    available_markets = Field()  # nav object
    
    # Broken parsers
    broken_parsers = Field()
    
    # Markets data
    back_markets = Field()  # List of MarketItem
    lay_markets = Field()   # List of MarketItem
    
# -------------------- Loaders --------------------
class PageVarLoader(ItemLoader):
    default_item_class = PageVarItem
    default_input_processor = MapCompose()
    default_output_processor = TakeFirst()

class HeaderLoader(ItemLoader):
    default_item_class = EventHeaderItem
    default_input_processor = MapCompose()
    default_output_processor = TakeFirst()

class BodyLoader(ItemLoader):
    default_item_class = EventBodyItem
    default_input_processor = MapCompose()
    default_output_processor = TakeFirst()

class OddsLoader(ItemLoader):
    default_item_class = OddsItem
    default_input_processor = MapCompose()
    # No default output processor - let fields be lists if needed
    
    # Only apply TakeFirst to specific scalar fields
    odds_value_in = MapCompose(convert_odds_value)
    odds_value_out = TakeFirst()
    
    volume_in = MapCompose(convert_volume)
    volume_out = TakeFirst()
    
    timestamp_in = MapCompose(convert_unix_timestamp)
    timestamp_out = TakeFirst()

class OutcomeLoader(ItemLoader):
    default_item_class = OutcomeItem
    default_input_processor = MapCompose()
    # No default output processor
    
    # Scalar fields get TakeFirst
    bookmaker_id_out = TakeFirst()
    bookmaker_name_out = TakeFirst()
    outcome_id_out = TakeFirst()
    outcome_position_out = TakeFirst()
    outcome_type_out = TakeFirst()
    
    # odds_history stays as list (no output processor)

class MarketLoader(ItemLoader):
    default_item_class = MarketItem
    default_input_processor = MapCompose()
    # No default output processor
    
    # Convert and take first for scalar fields
    betting_type_id_in = MapCompose(int)
    betting_type_id_out = TakeFirst()
    
    betting_type_name_out = TakeFirst()
    
    scope_id_in = MapCompose(int)
    scope_id_out = TakeFirst()
    
    scope_name_out = TakeFirst()
    
    handicap_type_id_in = MapCompose(int)
    handicap_type_id_out = TakeFirst()
    
    handicap_value_in = MapCompose(float)
    handicap_value_out = TakeFirst()
    
    mixed_parameter_id_in = MapCompose(int)
    mixed_parameter_id_out = TakeFirst()
    
    mixed_parameter_name_out = TakeFirst()
    is_back_out = TakeFirst()
    
    # List fields stay as lists (no output processor)
    # outcome_ids, outcomes

class MatchEventOddsLoader(ItemLoader):
    default_item_class = MatchEventOddsItem
    default_input_processor = MapCompose()
    # No default output processor
    
    # Scalar fields get TakeFirst
    match_id_out = TakeFirst()
    encoded_event_id_out = TakeFirst()
    current_betting_type_out = TakeFirst()
    current_scope_out = TakeFirst()
    
    time_base_in = MapCompose(convert_unix_timestamp)
    time_base_out = TakeFirst()
    
    refresh_interval_in = MapCompose(int)
    refresh_interval_out = TakeFirst()
    
    # List/dict fields stay as they are (no output processor)
    # available_markets, broken_parsers, back_markets, lay_markets


# -------------------- Mapping Dictionaries --------------------

BETTING_TYPE_NAMES = {
    1: "1X2",
    2: "Over/Under",
    3: "Home/Away", 
    4: "Double Chance",
    5: "Asian Handicap",
    6: "Draw No Bet",
    7: "To Qualify",
    8: "Correct Score",
    9: "Half Time / Full Time",
    10: "Odd or Even",
    11: "Winner",
    12: "European Handicap",
    13: "Both Teams to Score"
}

SCOPE_NAMES = {
    2: "Full Time",
    3: "First Half",
    4: "Second Half"
}

# Position to outcome type mapping based on betting type
OUTCOME_TYPE_MAP = {
    1: {0: "home", 1: "draw", 2: "away"},           # 1X2
    2: {0: "under", 1: "over"},                     # Over/Under
    3: {0: "home", 1: "away"},                      # Home/Away  
    4: {0: "1x", 1: "12", 2: "x2"},                 # Double Chance
    5: {0: "home", 1: "away"},                      # Asian Handicap
    6: {0: "home", 1: "away"},                      # Draw No Bet
    7: {0: "home", 1: "away"},                      # To Qualify
    8: {},                                          # Correct Score (dynamic outcomes)
    9: {},                                          # Half Time / Full Time (dynamic outcomes)
    10: {0: "odd", 1: "even"},                      # Odd or Even
    11: {},                                         # Winner (outright - dynamic outcomes)
    12: {0: "home", 1: "draw", 2: "away"},          # European Handicap
    13: {0: "no", 1: "yes"}                         # Both Teams to Score
}