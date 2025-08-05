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

class LeagueMatchItem(Item):
    """Item for individual match from /league-matches endpoint"""
    # Basic match information
    id = Field()                        # Match ID
    homeID = Field()                    # Home team ID
    awayID = Field()                    # Away team ID
    home_name = Field()                 # Home team name
    away_name = Field()                 # Away team name
    season = Field()                    # Season string
    status = Field()                    # Match status
    roundID = Field()                   # Round ID
    game_week = Field()                 # Game week
    revised_game_week = Field()         # Revised game week
    date_unix = Field()                 # Match timestamp
    
    # Goals and scoring
    homeGoalCount = Field()             # Home team goals
    awayGoalCount = Field()             # Away team goals
    totalGoalCount = Field()            # Total goals
    homeGoals = Field()                 # Home goal timings (array)
    awayGoals = Field()                 # Away goal timings (array)
    home_team_goal_timings = Field()    # Home goal timing details
    away_team_goal_timings = Field()    # Away goal timing details
    
    # Match statistics
    team_a_corners = Field()            # Home team corners
    team_b_corners = Field()            # Away team corners
    team_a_offsides = Field()           # Home team offsides
    team_b_offsides = Field()           # Away team offsides
    team_a_yellow_cards = Field()       # Home team yellow cards
    team_b_yellow_cards = Field()       # Away team yellow cards
    team_a_red_cards = Field()          # Home team red cards
    team_b_red_cards = Field()          # Away team red cards
    team_a_shots_on_target = Field()    # Home shots on target
    team_b_shots_on_target = Field()    # Away shots on target
    team_a_shots_off_target = Field()   # Home shots off target
    team_b_shots_off_target = Field()   # Away shots off target
    team_a_shots = Field()              # Home total shots
    team_b_shots = Field()              # Away total shots
    team_a_possession = Field()         # Home possession
    team_b_possession = Field()         # Away possession
    
    # Half-time statistics
    home_team_goal_count_half_time = Field()  # HT home goals
    away_team_goal_count_half_time = Field()  # HT away goals
    total_goal_count_half_time = Field()      # HT total goals
    
    # Pre-match statistics
    pre_match_teamA_ppg = Field()       # Pre-match home PPG
    pre_match_teamB_ppg = Field()       # Pre-match away PPG
    pre_match_teamA_overall_avg_goals_per_match_pre_match = Field()
    pre_match_teamB_overall_avg_goals_per_match_pre_match = Field()
    
    # Odds information
    odds_ft_1 = Field()                 # Home win odds
    odds_ft_x = Field()                 # Draw odds
    odds_ft_2 = Field()                 # Away win odds
    odds_btts_yes = Field()             # BTTS Yes odds
    odds_btts_no = Field()              # BTTS No odds
    odds_over_05 = Field()              # Over 0.5 odds
    odds_under_05 = Field()             # Under 0.5 odds
    odds_over_15 = Field()              # Over 1.5 odds
    odds_under_15 = Field()             # Under 1.5 odds
    odds_over_25 = Field()              # Over 2.5 odds
    odds_under_25 = Field()             # Under 2.5 odds
    odds_over_35 = Field()              # Over 3.5 odds
    odds_under_35 = Field()             # Under 3.5 odds
    odds_over_45 = Field()              # Over 4.5 odds
    odds_under_45 = Field()             # Under 4.5 odds
    
    # Additional match details
    referee_id = Field()                # Referee ID
    coach_id_team_a = Field()           # Home coach ID
    coach_id_team_b = Field()           # Away coach ID
    stadium_name = Field()              # Stadium name
    stadium_location = Field()          # Stadium location
    winner_team_id = Field()            # Winning team ID (-1 for draw)
    
    # Statistical flags
    over_05 = Field()                   # Over 0.5 goals flag
    over_15 = Field()                   # Over 1.5 goals flag
    over_25 = Field()                   # Over 2.5 goals flag
    over_35 = Field()                   # Over 3.5 goals flag
    over_45 = Field()                   # Over 4.5 goals flag
    btts = Field()                      # BTTS flag
    
    # Season context
    seasonID = Field()                  # Season ID
    
    # Metadata
    extracted_at = Field()              # When this was extracted

class LeagueMatchLoader(ItemLoader):
    """Item loader for league match data"""
    
    default_item_class = LeagueMatchItem
    default_input_processor = MapCompose(clean_string)
    default_output_processor = TakeFirst()
    
    # Integer fields
    id_in = MapCompose(safe_int)
    homeID_in = MapCompose(safe_int)
    awayID_in = MapCompose(safe_int)
    roundID_in = MapCompose(safe_int)
    game_week_in = MapCompose(safe_int)
    revised_game_week_in = MapCompose(safe_int)
    homeGoalCount_in = MapCompose(safe_int)
    awayGoalCount_in = MapCompose(safe_int)
    totalGoalCount_in = MapCompose(safe_int)
    team_a_corners_in = MapCompose(safe_int)
    team_b_corners_in = MapCompose(safe_int)
    team_a_offsides_in = MapCompose(safe_int)
    team_b_offsides_in = MapCompose(safe_int)
    team_a_yellow_cards_in = MapCompose(safe_int)
    team_b_yellow_cards_in = MapCompose(safe_int)
    team_a_red_cards_in = MapCompose(safe_int)
    team_b_red_cards_in = MapCompose(safe_int)
    team_a_shots_on_target_in = MapCompose(safe_int)
    team_b_shots_on_target_in = MapCompose(safe_int)
    team_a_shots_off_target_in = MapCompose(safe_int)
    team_b_shots_off_target_in = MapCompose(safe_int)
    team_a_shots_in = MapCompose(safe_int)
    team_b_shots_in = MapCompose(safe_int)
    home_team_goal_count_half_time_in = MapCompose(safe_int)
    away_team_goal_count_half_time_in = MapCompose(safe_int)
    total_goal_count_half_time_in = MapCompose(safe_int)
    referee_id_in = MapCompose(safe_int)
    coach_id_team_a_in = MapCompose(safe_int)
    coach_id_team_b_in = MapCompose(safe_int)
    winner_team_id_in = MapCompose(safe_int)
    seasonID_in = MapCompose(safe_int)
    
    # Float fields
    team_a_possession_in = MapCompose(safe_float)
    team_b_possession_in = MapCompose(safe_float)
    pre_match_teamA_ppg_in = MapCompose(safe_float)
    pre_match_teamB_ppg_in = MapCompose(safe_float)
    pre_match_teamA_overall_avg_goals_per_match_pre_match_in = MapCompose(safe_float)
    pre_match_teamB_overall_avg_goals_per_match_pre_match_in = MapCompose(safe_float)
    odds_ft_1_in = MapCompose(safe_float)
    odds_ft_x_in = MapCompose(safe_float)
    odds_ft_2_in = MapCompose(safe_float)
    odds_btts_yes_in = MapCompose(safe_float)
    odds_btts_no_in = MapCompose(safe_float)
    odds_over_05_in = MapCompose(safe_float)
    odds_under_05_in = MapCompose(safe_float)
    odds_over_15_in = MapCompose(safe_float)
    odds_under_15_in = MapCompose(safe_float)
    odds_over_25_in = MapCompose(safe_float)
    odds_under_25_in = MapCompose(safe_float)
    odds_over_35_in = MapCompose(safe_float)
    odds_under_35_in = MapCompose(safe_float)
    odds_over_45_in = MapCompose(safe_float)
    odds_under_45_in = MapCompose(safe_float)
    
    # Boolean fields
    over_05_in = MapCompose(lambda x: bool(x) if x is not None else None)
    over_15_in = MapCompose(lambda x: bool(x) if x is not None else None)
    over_25_in = MapCompose(lambda x: bool(x) if x is not None else None)
    over_35_in = MapCompose(lambda x: bool(x) if x is not None else None)
    over_45_in = MapCompose(lambda x: bool(x) if x is not None else None)
    btts_in = MapCompose(lambda x: bool(x) if x is not None else None)
    
    # Timestamp
    date_unix_in = MapCompose(convert_unix_timestamp)
    extracted_at_in = MapCompose(lambda x: datetime.now())
    
    # Array fields (keep as lists)
    homeGoals_out = Identity()
    awayGoals_out = Identity()
    home_team_goal_timings_out = Identity()
    away_team_goal_timings_out = Identity()

def validate_league_match_item(item_data: dict) -> bool:
    """Validate league match data structure before processing"""
    required_fields = ['id', 'home_name', 'away_name', 'season']
    
    if not isinstance(item_data, dict):
        return False
    
    for field in required_fields:
        if field not in item_data or not item_data[field]:
            return False
    
    return True

def create_league_match_item(item_data: dict) -> LeagueMatchItem:
    """Create league match item from API data"""
    loader = LeagueMatchLoader()
    
    # Basic match information
    loader.add_value('id', item_data.get('id'))
    loader.add_value('homeID', item_data.get('homeID'))
    loader.add_value('awayID', item_data.get('awayID'))
    loader.add_value('home_name', item_data.get('home_name'))
    loader.add_value('away_name', item_data.get('away_name'))
    loader.add_value('season', item_data.get('season'))
    loader.add_value('status', item_data.get('status'))
    loader.add_value('roundID', item_data.get('roundID'))
    loader.add_value('game_week', item_data.get('game_week'))
    loader.add_value('revised_game_week', item_data.get('revised_game_week'))
    loader.add_value('date_unix', item_data.get('date_unix'))
    
    # Goals and scoring
    loader.add_value('homeGoalCount', item_data.get('homeGoalCount'))
    loader.add_value('awayGoalCount', item_data.get('awayGoalCount'))
    loader.add_value('totalGoalCount', item_data.get('totalGoalCount'))
    loader.add_value('homeGoals', item_data.get('homeGoals', []))
    loader.add_value('awayGoals', item_data.get('awayGoals', []))
    loader.add_value('home_team_goal_timings', item_data.get('home_team_goal_timings', []))
    loader.add_value('away_team_goal_timings', item_data.get('away_team_goal_timings', []))
    
    # Match statistics
    loader.add_value('team_a_corners', item_data.get('team_a_corners'))
    loader.add_value('team_b_corners', item_data.get('team_b_corners'))
    loader.add_value('team_a_offsides', item_data.get('team_a_offsides'))
    loader.add_value('team_b_offsides', item_data.get('team_b_offsides'))
    loader.add_value('team_a_yellow_cards', item_data.get('team_a_yellow_cards'))
    loader.add_value('team_b_yellow_cards', item_data.get('team_b_yellow_cards'))
    loader.add_value('team_a_red_cards', item_data.get('team_a_red_cards'))
    loader.add_value('team_b_red_cards', item_data.get('team_b_red_cards'))
    loader.add_value('team_a_shots_on_target', item_data.get('team_a_shots_on_target'))
    loader.add_value('team_b_shots_on_target', item_data.get('team_b_shots_on_target'))
    loader.add_value('team_a_shots_off_target', item_data.get('team_a_shots_off_target'))
    loader.add_value('team_b_shots_off_target', item_data.get('team_b_shots_off_target'))
    loader.add_value('team_a_shots', item_data.get('team_a_shots'))
    loader.add_value('team_b_shots', item_data.get('team_b_shots'))
    loader.add_value('team_a_possession', item_data.get('team_a_possession'))
    loader.add_value('team_b_possession', item_data.get('team_b_possession'))
    
    # Half-time statistics
    loader.add_value('home_team_goal_count_half_time', item_data.get('home_team_goal_count_half_time'))
    loader.add_value('away_team_goal_count_half_time', item_data.get('away_team_goal_count_half_time'))
    loader.add_value('total_goal_count_half_time', item_data.get('total_goal_count_half_time'))
    
    # Pre-match statistics
    loader.add_value('pre_match_teamA_ppg', item_data.get('pre_match_teamA_ppg'))
    loader.add_value('pre_match_teamB_ppg', item_data.get('pre_match_teamB_ppg'))
    loader.add_value('pre_match_teamA_overall_avg_goals_per_match_pre_match', 
                    item_data.get('pre_match_teamA_overall_avg_goals_per_match_pre_match'))
    loader.add_value('pre_match_teamB_overall_avg_goals_per_match_pre_match', 
                    item_data.get('pre_match_teamB_overall_avg_goals_per_match_pre_match'))
    
    # Odds information
    loader.add_value('odds_ft_1', item_data.get('odds_ft_1'))
    loader.add_value('odds_ft_x', item_data.get('odds_ft_x'))
    loader.add_value('odds_ft_2', item_data.get('odds_ft_2'))
    loader.add_value('odds_btts_yes', item_data.get('odds_btts_yes'))
    loader.add_value('odds_btts_no', item_data.get('odds_btts_no'))
    loader.add_value('odds_over_05', item_data.get('odds_over_05'))
    loader.add_value('odds_under_05', item_data.get('odds_under_05'))
    loader.add_value('odds_over_15', item_data.get('odds_over_15'))
    loader.add_value('odds_under_15', item_data.get('odds_under_15'))
    loader.add_value('odds_over_25', item_data.get('odds_over_25'))
    loader.add_value('odds_under_25', item_data.get('odds_under_25'))
    loader.add_value('odds_over_35', item_data.get('odds_over_35'))
    loader.add_value('odds_under_35', item_data.get('odds_under_35'))
    loader.add_value('odds_over_45', item_data.get('odds_over_45'))
    loader.add_value('odds_under_45', item_data.get('odds_under_45'))
    
    # Additional match details
    loader.add_value('referee_id', item_data.get('referee_id'))
    loader.add_value('coach_id_team_a', item_data.get('coach_id_team_a'))
    loader.add_value('coach_id_team_b', item_data.get('coach_id_team_b'))
    loader.add_value('stadium_name', item_data.get('stadium_name'))
    loader.add_value('stadium_location', item_data.get('stadium_location'))
    loader.add_value('winner_team_id', item_data.get('winner_team_id'))
    
    # Statistical flags
    loader.add_value('over_05', item_data.get('over_05'))
    loader.add_value('over_15', item_data.get('over_15'))
    loader.add_value('over_25', item_data.get('over_25'))
    loader.add_value('over_35', item_data.get('over_35'))
    loader.add_value('over_45', item_data.get('over_45'))
    loader.add_value('btts', item_data.get('btts'))
    
    # Season context
    loader.add_value('seasonID', item_data.get('seasonID'))
    
    # Metadata
    loader.add_value('extracted_at', None)
    
    return loader.load_item()