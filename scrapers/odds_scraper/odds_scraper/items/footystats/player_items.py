from scrapy import Item, Field
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst, Identity
from datetime import datetime

def clean_string(value):
    """Clean and strip string values"""
    if isinstance(value, str):
        return value.strip()
    return value

def safe_int(value):
    """Safely convert to integer"""
    try:
        return int(value) if value is not None else None
    except (ValueError, TypeError):
        return None

def safe_float(value):
    """Safely convert to float"""
    try:
        return float(value) if value is not None else None
    except (ValueError, TypeError):
        return None

def convert_unix_timestamp(timestamp):
    """Convert UNIX timestamp to datetime object"""
    try:
        if isinstance(timestamp, (int, float)):
            return datetime.fromtimestamp(timestamp)
        return None
    except (ValueError, TypeError):
        return None

class PlayerSeasonItem(Item):
    """Individual season statistics for player"""
    season = Field()                    # Season string (e.g., "2023/2024")
    competition_name = Field()          # Competition name
    team_name = Field()                 # Team name for this season
    team_id = Field()                   # Team ID
    appearances = Field()               # Appearances count
    goals = Field()                     # Goals scored
    assists = Field()                   # Assists count
    yellow_cards = Field()              # Yellow cards received
    red_cards = Field()                 # Red cards received
    mins_played = Field()               # Minutes played
    starting_eleven = Field()           # Times in starting XI
    substitute_appearances = Field()    # Substitute appearances

class PlayerItem(Item):
    """Item for player from /player endpoint"""
    # Basic information
    id = Field()                        # Player ID
    player_name = Field()               # Full player name
    first_name = Field()                # First name
    last_name = Field()                 # Last name
    age = Field()                       # Current age
    position = Field()                  # Playing position
    nationality = Field()               # Player nationality
    height = Field()                    # Height in cm
    weight = Field()                    # Weight in kg
    birthday = Field()                  # Birthday timestamp
    
    # Current team information
    current_team = Field()              # Current team name
    current_team_id = Field()           # Current team ID
    jersey_number = Field()             # Jersey number
    
    # Career totals across all competitions
    career_appearances = Field()        # Total career appearances
    career_goals = Field()              # Total career goals
    career_assists = Field()            # Total career assists
    career_yellow_cards = Field()       # Total yellow cards
    career_red_cards = Field()          # Total red cards
    career_mins_played = Field()        # Total minutes played
    career_starting_eleven = Field()    # Total starts
    career_substitute_apps = Field()    # Total substitute appearances
    
    # Career averages and ratios
    goals_per_match = Field()           # Goals per match average
    assists_per_match = Field()         # Assists per match average
    mins_per_goal = Field()             # Minutes per goal
    mins_per_assist = Field()           # Minutes per assist
    goals_per_90_mins = Field()         # Goals per 90 minutes
    assists_per_90_mins = Field()       # Assists per 90 minutes
    
    # Season breakdown
    seasons = Field()                   # List of PlayerSeasonItem
    total_seasons = Field()             # Total number of seasons
    
    # Market and contract information
    market_value = Field()              # Current market value
    market_value_currency = Field()     # Currency of market value
    contract_expires = Field()          # Contract expiry date
    contract_expires_timestamp = Field() # Contract expiry as timestamp
    
    # Physical and personal details
    preferred_foot = Field()            # Preferred foot (left/right)
    international_caps = Field()        # International appearances
    international_goals = Field()       # International goals
    
    # Performance indicators
    disciplinary_points = Field()       # Total disciplinary points
    injury_prone_rating = Field()       # Injury proneness rating
    
    # Metadata
    last_updated = Field()              # When player data was last updated
    extracted_at = Field()              # When this was extracted

class PlayerSeasonLoader(ItemLoader):
    """Item loader for player season data"""
    
    default_item_class = PlayerSeasonItem
    default_input_processor = MapCompose(clean_string)
    default_output_processor = TakeFirst()
    
    # Integer fields
    team_id_in = MapCompose(safe_int)
    appearances_in = MapCompose(safe_int)
    goals_in = MapCompose(safe_int)
    assists_in = MapCompose(safe_int)
    yellow_cards_in = MapCompose(safe_int)
    red_cards_in = MapCompose(safe_int)
    mins_played_in = MapCompose(safe_int)
    starting_eleven_in = MapCompose(safe_int)
    substitute_appearances_in = MapCompose(safe_int)

class PlayerLoader(ItemLoader):
    """Item loader for player data"""
    
    default_item_class = PlayerItem
    default_input_processor = MapCompose(clean_string)
    default_output_processor = TakeFirst()
    
    # Integer fields
    id_in = MapCompose(safe_int)
    age_in = MapCompose(safe_int)
    height_in = MapCompose(safe_int)
    weight_in = MapCompose(safe_int)
    birthday_in = MapCompose(safe_int)
    current_team_id_in = MapCompose(safe_int)
    jersey_number_in = MapCompose(safe_int)
    career_appearances_in = MapCompose(safe_int)
    career_goals_in = MapCompose(safe_int)
    career_assists_in = MapCompose(safe_int)
    career_yellow_cards_in = MapCompose(safe_int)
    career_red_cards_in = MapCompose(safe_int)
    career_mins_played_in = MapCompose(safe_int)
    career_starting_eleven_in = MapCompose(safe_int)
    career_substitute_apps_in = MapCompose(safe_int)
    total_seasons_in = MapCompose(safe_int)
    international_caps_in = MapCompose(safe_int)
    international_goals_in = MapCompose(safe_int)
    disciplinary_points_in = MapCompose(safe_int)
    last_updated_in = MapCompose(safe_int)
    
    # Float fields
    goals_per_match_in = MapCompose(safe_float)
    assists_per_match_in = MapCompose(safe_float)
    mins_per_goal_in = MapCompose(safe_float)
    mins_per_assist_in = MapCompose(safe_float)
    goals_per_90_mins_in = MapCompose(safe_float)
    assists_per_90_mins_in = MapCompose(safe_float)
    market_value_in = MapCompose(safe_float)
    injury_prone_rating_in = MapCompose(safe_float)
    
    # Timestamp fields
    contract_expires_timestamp_in = MapCompose(convert_unix_timestamp)
    extracted_at_in = MapCompose(lambda x: datetime.now())
    
    # Keep seasons as list
    seasons_out = Identity()

def create_player_season(season_data: dict) -> PlayerSeasonItem:
    """Create player season item from season data"""
    loader = PlayerSeasonLoader()
    
    loader.add_value('season', season_data.get('season'))
    loader.add_value('competition_name', season_data.get('competition_name'))
    loader.add_value('team_name', season_data.get('team_name'))
    loader.add_value('team_id', season_data.get('team_id'))
    loader.add_value('appearances', season_data.get('appearances'))
    loader.add_value('goals', season_data.get('goals'))
    loader.add_value('assists', season_data.get('assists'))
    loader.add_value('yellow_cards', season_data.get('yellow_cards'))
    loader.add_value('red_cards', season_data.get('red_cards'))
    loader.add_value('mins_played', season_data.get('mins_played'))
    loader.add_value('starting_eleven', season_data.get('starting_eleven'))
    loader.add_value('substitute_appearances', season_data.get('substitute_appearances'))
    
    return loader.load_item()

def validate_player_item(item_data: dict) -> bool:
    """Validate player data structure before processing"""
    required_fields = ['id', 'player_name']
    
    if not isinstance(item_data, dict):
        return False
    
    for field in required_fields:
        if field not in item_data or not item_data[field]:
            return False
    
    return True

def create_player_item(item_data: dict) -> PlayerItem:
    """Create player item from API data"""
    loader = PlayerLoader()
    
    # Basic information
    loader.add_value('id', item_data.get('id'))
    loader.add_value('player_name', item_data.get('player_name'))
    loader.add_value('first_name', item_data.get('first_name'))
    loader.add_value('last_name', item_data.get('last_name'))
    loader.add_value('age', item_data.get('age'))
    loader.add_value('position', item_data.get('position'))
    loader.add_value('nationality', item_data.get('nationality'))
    loader.add_value('height', item_data.get('height'))
    loader.add_value('weight', item_data.get('weight'))
    loader.add_value('birthday', item_data.get('birthday'))
    
    # Current team information
    loader.add_value('current_team', item_data.get('current_team'))
    loader.add_value('current_team_id', item_data.get('current_team_id'))
    loader.add_value('jersey_number', item_data.get('jersey_number'))
    
    # Career totals
    loader.add_value('career_appearances', item_data.get('career_appearances'))
    loader.add_value('career_goals', item_data.get('career_goals'))
    loader.add_value('career_assists', item_data.get('career_assists'))
    loader.add_value('career_yellow_cards', item_data.get('career_yellow_cards'))
    loader.add_value('career_red_cards', item_data.get('career_red_cards'))
    loader.add_value('career_mins_played', item_data.get('career_mins_played'))
    loader.add_value('career_starting_eleven', item_data.get('career_starting_eleven'))
    loader.add_value('career_substitute_apps', item_data.get('career_substitute_apps'))
    
    # Career averages and ratios
    loader.add_value('goals_per_match', item_data.get('goals_per_match'))
    loader.add_value('assists_per_match', item_data.get('assists_per_match'))
    loader.add_value('mins_per_goal', item_data.get('mins_per_goal'))
    loader.add_value('mins_per_assist', item_data.get('mins_per_assist'))
    loader.add_value('goals_per_90_mins', item_data.get('goals_per_90_mins'))
    loader.add_value('assists_per_90_mins', item_data.get('assists_per_90_mins'))
    
    # Process seasons
    seasons_data = item_data.get('seasons', [])
    if isinstance(seasons_data, list):
        seasons = [create_player_season(season) for season in seasons_data]
        loader.add_value('seasons', seasons)
        loader.add_value('total_seasons', len(seasons))
    else:
        loader.add_value('seasons', [])
        loader.add_value('total_seasons', 0)
    
    # Market and contract information
    loader.add_value('market_value', item_data.get('market_value'))
    loader.add_value('market_value_currency', item_data.get('market_value_currency'))
    loader.add_value('contract_expires', item_data.get('contract_expires'))
    loader.add_value('contract_expires_timestamp', item_data.get('contract_expires_timestamp'))
    
    # Physical and personal details
    loader.add_value('preferred_foot', item_data.get('preferred_foot'))
    loader.add_value('international_caps', item_data.get('international_caps'))
    loader.add_value('international_goals', item_data.get('international_goals'))
    
    # Performance indicators
    loader.add_value('disciplinary_points', item_data.get('disciplinary_points'))
    loader.add_value('injury_prone_rating', item_data.get('injury_prone_rating'))
    
    # Metadata
    loader.add_value('last_updated', item_data.get('last_updated'))
    loader.add_value('extracted_at', None)
    
    return loader.load_item()