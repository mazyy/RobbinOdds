from scrapy import Item, Field
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst
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

class LeaguePlayerItem(Item):
    """Item for individual player from /league-players endpoint"""
    # Basic player information
    id = Field()                        # Player ID
    player_name = Field()               # Full player name
    team_name = Field()                 # Current team name
    team_id = Field()                   # Team ID
    position = Field()                  # Player position
    age = Field()                       # Player age
    
    # Performance statistics
    apps = Field()                      # Appearances count
    goals = Field()                     # Goals scored
    assists = Field()                   # Assists count
    mins_played = Field()               # Minutes played
    
    # Disciplinary records
    yellow_cards = Field()              # Yellow cards received
    red_cards = Field()                 # Red cards received
    
    # Shot statistics
    shots = Field()                     # Total shots
    shots_on_target = Field()           # Shots on target
    shot_accuracy = Field()             # Shot accuracy percentage
    
    # Passing statistics
    passes = Field()                    # Total passes
    passes_completed = Field()          # Completed passes
    pass_accuracy = Field()             # Pass accuracy percentage
    key_passes = Field()                # Key passes
    
    # Defensive statistics
    tackles = Field()                   # Tackles made
    interceptions = Field()             # Interceptions
    clearances = Field()                # Clearances
    blocks = Field()                    # Blocks
    
    # Advanced statistics
    dribbles = Field()                  # Dribbles attempted
    dribbles_successful = Field()       # Successful dribbles
    fouls_committed = Field()           # Fouls committed
    fouls_suffered = Field()            # Fouls suffered
    offsides = Field()                  # Offsides count
    
    # Goalkeeper specific (if applicable)
    saves = Field()                     # Saves made
    goals_conceded = Field()            # Goals conceded
    clean_sheets = Field()              # Clean sheets
    
    # Performance ratios
    goals_per_match = Field()           # Goals per match
    assists_per_match = Field()         # Assists per match
    mins_per_goal = Field()             # Minutes per goal
    mins_per_assist = Field()           # Minutes per assist
    
    # Season context
    season_id = Field()                 # Season ID
    competition_name = Field()          # Competition name
    
    # Physical attributes
    height = Field()                    # Player height
    weight = Field()                    # Player weight
    nationality = Field()               # Player nationality
    
    # Market value (if available)
    market_value = Field()              # Market value
    contract_expires = Field()          # Contract expiration date
    
    # Additional playing time stats
    substitute_in = Field()             # Times subbed in
    substitute_out = Field()            # Times subbed out
    captain = Field()                   # Times as captain
    penalties_taken = Field()           # Penalties taken
    penalties_scored = Field()          # Penalties scored
    
    # More detailed stats often in API
    crosses = Field()                   # Crosses attempted
    corners_taken = Field()             # Corner kicks taken
    through_balls = Field()             # Through balls played
    long_balls = Field()                # Long balls attempted
    
    # Defensive stats
    aerial_duels_won = Field()          # Aerial duels won
    aerial_duels_total = Field()        # Total aerial duels
    duels_won = Field()                 # Ground duels won
    duels_total = Field()               # Total ground duels
    
    # Additional goal stats
    goals_left_foot = Field()           # Goals with left foot
    goals_right_foot = Field()          # Goals with right foot
    goals_header = Field()              # Goals with header
    goals_inside_box = Field()          # Goals from inside penalty area
    goals_outside_box = Field()         # Goals from outside penalty area
    
    # Form and streaks
    current_goals_streak = Field()      # Current scoring streak
    longest_goals_streak = Field()      # Longest scoring streak
    
    # Metadata
    extracted_at = Field()              # When this was extracted

class LeaguePlayerLoader(ItemLoader):
    """Item loader for league player data"""
    
    default_item_class = LeaguePlayerItem
    default_input_processor = MapCompose(clean_string)
    default_output_processor = TakeFirst()
    
    # Integer fields
    id_in = MapCompose(safe_int)
    team_id_in = MapCompose(safe_int)
    age_in = MapCompose(safe_int)
    apps_in = MapCompose(safe_int)
    goals_in = MapCompose(safe_int)
    assists_in = MapCompose(safe_int)
    mins_played_in = MapCompose(safe_int)
    yellow_cards_in = MapCompose(safe_int)
    red_cards_in = MapCompose(safe_int)
    shots_in = MapCompose(safe_int)
    shots_on_target_in = MapCompose(safe_int)
    passes_in = MapCompose(safe_int)
    passes_completed_in = MapCompose(safe_int)
    key_passes_in = MapCompose(safe_int)
    tackles_in = MapCompose(safe_int)
    interceptions_in = MapCompose(safe_int)
    clearances_in = MapCompose(safe_int)
    blocks_in = MapCompose(safe_int)
    dribbles_in = MapCompose(safe_int)
    dribbles_successful_in = MapCompose(safe_int)
    fouls_committed_in = MapCompose(safe_int)
    fouls_suffered_in = MapCompose(safe_int)
    offsides_in = MapCompose(safe_int)
    saves_in = MapCompose(safe_int)
    goals_conceded_in = MapCompose(safe_int)
    clean_sheets_in = MapCompose(safe_int)
    season_id_in = MapCompose(safe_int)
    height_in = MapCompose(safe_int)
    weight_in = MapCompose(safe_int)
    
    # Float fields
    shot_accuracy_in = MapCompose(safe_float)
    pass_accuracy_in = MapCompose(safe_float)
    goals_per_match_in = MapCompose(safe_float)
    assists_per_match_in = MapCompose(safe_float)
    mins_per_goal_in = MapCompose(safe_float)
    mins_per_assist_in = MapCompose(safe_float)
    market_value_in = MapCompose(safe_float)
    
    # Additional integer fields
    substitute_in_in = MapCompose(safe_int)
    substitute_out_in = MapCompose(safe_int)
    captain_in = MapCompose(safe_int)
    penalties_taken_in = MapCompose(safe_int)
    penalties_scored_in = MapCompose(safe_int)
    crosses_in = MapCompose(safe_int)
    corners_taken_in = MapCompose(safe_int)
    through_balls_in = MapCompose(safe_int)
    long_balls_in = MapCompose(safe_int)
    aerial_duels_won_in = MapCompose(safe_int)
    aerial_duels_total_in = MapCompose(safe_int)
    duels_won_in = MapCompose(safe_int)
    duels_total_in = MapCompose(safe_int)
    goals_left_foot_in = MapCompose(safe_int)
    goals_right_foot_in = MapCompose(safe_int)
    goals_header_in = MapCompose(safe_int)
    goals_inside_box_in = MapCompose(safe_int)
    goals_outside_box_in = MapCompose(safe_int)
    current_goals_streak_in = MapCompose(safe_int)
    longest_goals_streak_in = MapCompose(safe_int)
    
    # Timestamp
    extracted_at_in = MapCompose(lambda x: datetime.now())

def validate_league_player_item(item_data: dict) -> bool:
    """Validate league player data structure before processing"""
    required_fields = ['id', 'player_name', 'team_name']
    
    if not isinstance(item_data, dict):
        return False
    
    for field in required_fields:
        if field not in item_data or not item_data[field]:
            return False
    
    return True

def create_league_player_item(item_data: dict) -> LeaguePlayerItem:
    """Create league player item from API data"""
    loader = LeaguePlayerLoader()
    
    # Basic player information
    loader.add_value('id', item_data.get('id'))
    loader.add_value('player_name', item_data.get('player_name'))
    loader.add_value('team_name', item_data.get('team_name'))
    loader.add_value('team_id', item_data.get('team_id'))
    loader.add_value('position', item_data.get('position'))
    loader.add_value('age', item_data.get('age'))
    
    # Performance statistics
    loader.add_value('apps', item_data.get('apps'))
    loader.add_value('goals', item_data.get('goals'))
    loader.add_value('assists', item_data.get('assists'))
    loader.add_value('mins_played', item_data.get('mins_played'))
    
    # Disciplinary records
    loader.add_value('yellow_cards', item_data.get('yellow_cards'))
    loader.add_value('red_cards', item_data.get('red_cards'))
    
    # Shot statistics
    loader.add_value('shots', item_data.get('shots'))
    loader.add_value('shots_on_target', item_data.get('shots_on_target'))
    loader.add_value('shot_accuracy', item_data.get('shot_accuracy'))
    
    # Passing statistics
    loader.add_value('passes', item_data.get('passes'))
    loader.add_value('passes_completed', item_data.get('passes_completed'))
    loader.add_value('pass_accuracy', item_data.get('pass_accuracy'))
    loader.add_value('key_passes', item_data.get('key_passes'))
    
    # Defensive statistics
    loader.add_value('tackles', item_data.get('tackles'))
    loader.add_value('interceptions', item_data.get('interceptions'))
    loader.add_value('clearances', item_data.get('clearances'))
    loader.add_value('blocks', item_data.get('blocks'))
    
    # Advanced statistics
    loader.add_value('dribbles', item_data.get('dribbles'))
    loader.add_value('dribbles_successful', item_data.get('dribbles_successful'))
    loader.add_value('fouls_committed', item_data.get('fouls_committed'))
    loader.add_value('fouls_suffered', item_data.get('fouls_suffered'))
    loader.add_value('offsides', item_data.get('offsides'))
    
    # Goalkeeper specific
    loader.add_value('saves', item_data.get('saves'))
    loader.add_value('goals_conceded', item_data.get('goals_conceded'))
    loader.add_value('clean_sheets', item_data.get('clean_sheets'))
    
    # Performance ratios
    loader.add_value('goals_per_match', item_data.get('goals_per_match'))
    loader.add_value('assists_per_match', item_data.get('assists_per_match'))
    loader.add_value('mins_per_goal', item_data.get('mins_per_goal'))
    loader.add_value('mins_per_assist', item_data.get('mins_per_assist'))
    
    # Season context
    loader.add_value('season_id', item_data.get('season_id'))
    loader.add_value('competition_name', item_data.get('competition_name'))
    
    # Physical attributes
    loader.add_value('height', item_data.get('height'))
    loader.add_value('weight', item_data.get('weight'))
    loader.add_value('nationality', item_data.get('nationality'))
    
    # Market value
    loader.add_value('market_value', item_data.get('market_value'))
    loader.add_value('contract_expires', item_data.get('contract_expires'))
    
    # Additional playing time stats
    loader.add_value('substitute_in', item_data.get('substitute_in'))
    loader.add_value('substitute_out', item_data.get('substitute_out'))
    loader.add_value('captain', item_data.get('captain'))
    loader.add_value('penalties_taken', item_data.get('penalties_taken'))
    loader.add_value('penalties_scored', item_data.get('penalties_scored'))
    
    # More detailed stats
    loader.add_value('crosses', item_data.get('crosses'))
    loader.add_value('corners_taken', item_data.get('corners_taken'))
    loader.add_value('through_balls', item_data.get('through_balls'))
    loader.add_value('long_balls', item_data.get('long_balls'))
    
    # Defensive stats
    loader.add_value('aerial_duels_won', item_data.get('aerial_duels_won'))
    loader.add_value('aerial_duels_total', item_data.get('aerial_duels_total'))
    loader.add_value('duels_won', item_data.get('duels_won'))
    loader.add_value('duels_total', item_data.get('duels_total'))
    
    # Additional goal stats
    loader.add_value('goals_left_foot', item_data.get('goals_left_foot'))
    loader.add_value('goals_right_foot', item_data.get('goals_right_foot'))
    loader.add_value('goals_header', item_data.get('goals_header'))
    loader.add_value('goals_inside_box', item_data.get('goals_inside_box'))
    loader.add_value('goals_outside_box', item_data.get('goals_outside_box'))
    
    # Form and streaks
    loader.add_value('current_goals_streak', item_data.get('current_goals_streak'))
    loader.add_value('longest_goals_streak', item_data.get('longest_goals_streak'))
    
    # Metadata
    loader.add_value('extracted_at', None)
    
    return loader.load_item()