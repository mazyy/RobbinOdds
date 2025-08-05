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

# Nested items for complex data structures
class PlayerEventItem(Item):
    """Individual player event (goal, card, etc.)"""
    event_type = Field()    # "Goal", "Yellow", "Red", etc.
    event_time = Field()    # Minute of the event

class LineupPlayerItem(Item):
    """Player in starting lineup"""
    player_id = Field()
    shirt_number = Field()
    player_events = Field()  # List of PlayerEventItem

class SubstitutionItem(Item):
    """Substitution details"""
    player_in_id = Field()
    player_in_shirt_number = Field()
    player_out_id = Field()
    player_out_time = Field()
    player_in_events = Field()  # List of PlayerEventItem

class GoalDetailItem(Item):
    """Goal details"""
    player_id = Field()
    time = Field()
    extra = Field()         # Extra time, penalty, etc.
    assist_player_id = Field()

class CardDetailItem(Item):
    """Card details"""
    player_id = Field()
    card_type = Field()     # "Yellow" or "Red"
    time = Field()

class H2HStatsItem(Item):
    """Head-to-head statistics"""
    team_a_id = Field()
    team_b_id = Field()
    total_matches = Field()
    team_a_wins = Field()
    team_b_wins = Field()
    draws = Field()
    team_a_win_percent = Field()
    team_b_win_percent = Field()
    avg_goals = Field()
    total_goals = Field()
    over05_percentage = Field()
    over15_percentage = Field()
    over25_percentage = Field()
    btts_percentage = Field()
    previous_matches_ids = Field()  # List of previous match data

class WeatherItem(Item):
    """Weather conditions"""
    temperature_celsius = Field()
    temperature_fahrenheit = Field()
    humidity = Field()
    wind_speed = Field()
    wind_degree = Field()
    weather_type = Field()
    clouds = Field()
    pressure = Field()

class MatchDetailsItem(Item):
    """Complete match details from FootyStats /match endpoint"""
    
    # Basic match information
    id = Field()                        # Match ID
    home_id = Field()                   # Home team ID
    away_id = Field()                   # Away team ID
    home_name = Field()                 # Home team name
    away_name = Field()                 # Away team name
    season = Field()                    # Season string
    status = Field()                    # Match status
    round_id = Field()                  # Round ID
    game_week = Field()                 # Game week
    revised_game_week = Field()         # Revised game week
    date_unix = Field()                 # Match timestamp as datetime
    competition_id = Field()            # Competition ID
    
    # Goals and scoring
    home_goal_count = Field()           # Home team goals
    away_goal_count = Field()           # Away team goals
    total_goal_count = Field()          # Total goals
    home_goals = Field()                # Home goal timings (list)
    away_goals = Field()                # Away goal timings (list)
    home_goals_timings = Field()        # Home goal timing details
    away_goals_timings = Field()        # Away goal timing details
    winning_team = Field()              # Winning team ID
    
    # Half-time statistics
    ht_goals_team_a = Field()           # HT home goals
    ht_goals_team_b = Field()           # HT away goals
    ht_goal_count = Field()             # HT total goals
    goals_2hg_team_a = Field()          # 2nd half home goals
    goals_2hg_team_b = Field()          # 2nd half away goals
    goal_count_2hg = Field()            # 2nd half total goals
    
    # Match statistics
    team_a_corners = Field()            # Home team corners
    team_b_corners = Field()            # Away team corners
    total_corner_count = Field()        # Total corners
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
    team_a_fouls = Field()              # Home team fouls
    team_b_fouls = Field()              # Away team fouls
    team_a_possession = Field()         # Home possession percentage
    team_b_possession = Field()         # Away possession percentage
    
    # Advanced statistics
    team_a_xg = Field()                 # Home expected goals
    team_b_xg = Field()                 # Away expected goals
    total_xg = Field()                  # Total expected goals
    team_a_xg_prematch = Field()        # Pre-match home xG
    team_b_xg_prematch = Field()        # Pre-match away xG
    total_xg_prematch = Field()         # Pre-match total xG
    team_a_dangerous_attacks = Field()  # Home dangerous attacks
    team_b_dangerous_attacks = Field()  # Away dangerous attacks
    team_a_attacks = Field()            # Home total attacks
    team_b_attacks = Field()            # Away total attacks
    
    # Penalties
    team_a_penalties_won = Field()      # Home penalties won
    team_b_penalties_won = Field()      # Away penalties won
    team_a_penalty_goals = Field()      # Home penalty goals
    team_b_penalty_goals = Field()      # Away penalty goals
    team_a_penalty_missed = Field()     # Home penalties missed
    team_b_penalty_missed = Field()     # Away penalties missed
    
    # Corner and card timing details
    team_a_fh_corners = Field()         # Home first half corners
    team_b_fh_corners = Field()         # Away first half corners
    team_a_2h_corners = Field()         # Home second half corners
    team_b_2h_corners = Field()         # Away second half corners
    corner_fh_count = Field()           # First half corner count
    corner_2h_count = Field()           # Second half corner count
    team_a_fh_cards = Field()           # Home first half cards
    team_b_fh_cards = Field()           # Away first half cards
    team_a_2h_cards = Field()           # Home second half cards
    team_b_2h_cards = Field()           # Away second half cards
    total_fh_cards = Field()            # Total first half cards
    total_2h_cards = Field()            # Total second half cards
    
    # Pre-match team statistics
    home_ppg = Field()                  # Home team PPG
    away_ppg = Field()                  # Away team PPG
    pre_match_home_ppg = Field()        # Pre-match home PPG
    pre_match_away_ppg = Field()        # Pre-match away PPG
    pre_match_team_a_overall_ppg = Field()  # Pre-match home overall PPG
    pre_match_team_b_overall_ppg = Field()  # Pre-match away overall PPG
    
    # Comprehensive odds data (1X2)
    odds_ft_1 = Field()                 # Home win odds
    odds_ft_x = Field()                 # Draw odds
    odds_ft_2 = Field()                 # Away win odds
    
    # Over/Under odds
    odds_ft_over05 = Field()            # Over 0.5 odds
    odds_ft_over15 = Field()            # Over 1.5 odds
    odds_ft_over25 = Field()            # Over 2.5 odds
    odds_ft_over35 = Field()            # Over 3.5 odds
    odds_ft_over45 = Field()            # Over 4.5 odds
    odds_ft_under05 = Field()           # Under 0.5 odds
    odds_ft_under15 = Field()           # Under 1.5 odds
    odds_ft_under25 = Field()           # Under 2.5 odds
    odds_ft_under35 = Field()           # Under 3.5 odds
    odds_ft_under45 = Field()           # Under 4.5 odds
    
    # BTTS and Clean Sheet odds
    odds_btts_yes = Field()             # BTTS Yes odds
    odds_btts_no = Field()              # BTTS No odds
    odds_team_a_cs_yes = Field()        # Home clean sheet yes
    odds_team_a_cs_no = Field()         # Home clean sheet no
    odds_team_b_cs_yes = Field()        # Away clean sheet yes
    odds_team_b_cs_no = Field()         # Away clean sheet no
    
    # Double Chance odds
    odds_doublechance_1x = Field()      # 1X double chance
    odds_doublechance_12 = Field()      # 12 double chance
    odds_doublechance_x2 = Field()      # X2 double chance
    
    # Half-time odds
    odds_1st_half_result_1 = Field()    # 1st half home win
    odds_1st_half_result_x = Field()    # 1st half draw
    odds_1st_half_result_2 = Field()    # 1st half away win
    odds_2nd_half_result_1 = Field()    # 2nd half home win
    odds_2nd_half_result_x = Field()    # 2nd half draw
    odds_2nd_half_result_2 = Field()    # 2nd half away win
    
    # Other specialized odds
    odds_corners_over_105 = Field()     # Corners over 10.5
    odds_corners_under_105 = Field()    # Corners under 10.5
    odds_team_to_score_first_1 = Field() # Home to score first
    odds_team_to_score_first_2 = Field() # Away to score first
    odds_win_to_nil_1 = Field()         # Home win to nil
    odds_win_to_nil_2 = Field()         # Away win to nil
    
    # Match context
    referee_id = Field()                # Referee ID
    coach_a_id = Field()                # Home coach ID
    coach_b_id = Field()                # Away coach ID
    stadium_name = Field()              # Stadium name
    stadium_location = Field()          # Stadium location
    attendance = Field()                # Attendance figure
    
    # Complex nested data
    lineups = Field()                   # Starting lineups (nested structure)
    bench = Field()                     # Substitute players (nested structure)
    team_a_goal_details = Field()       # List of GoalDetailItem
    team_b_goal_details = Field()       # List of GoalDetailItem
    team_a_card_details = Field()       # List of CardDetailItem
    team_b_card_details = Field()       # List of CardDetailItem
    h2h = Field()                       # H2HStatsItem
    weather = Field()                   # WeatherItem
    
    # Additional data
    trends = Field()                    # Team trends data
    tv_stations = Field()               # TV broadcast info
    odds_comparison = Field()           # Detailed odds comparison
    
    # Flags and indicators
    goal_timing_disabled = Field()      # Goal timing disabled flag
    corner_timings_recorded = Field()   # Corner timings recorded flag
    card_timings_recorded = Field()     # Card timings recorded flag
    attacks_recorded = Field()          # Attacks recorded flag
    pens_recorded = Field()             # Penalties recorded flag
    goal_timings_recorded_flag = Field() # Goal timings recorded flag
    throwins_recorded = Field()         # Throw-ins recorded flag
    freekicks_recorded = Field()        # Free kicks recorded flag
    goalkicks_recorded = Field()        # Goal kicks recorded flag
    
    # Statistical potentials
    btts_potential = Field()            # BTTS potential percentage
    o05_potential = Field()             # Over 0.5 potential
    o15_potential = Field()             # Over 1.5 potential
    o25_potential = Field()             # Over 2.5 potential
    o35_potential = Field()             # Over 3.5 potential
    o45_potential = Field()             # Over 4.5 potential
    corners_potential = Field()         # Corners potential
    cards_potential = Field()           # Cards potential
    avg_potential = Field()             # Average potential
    
    # URLs and images
    home_url = Field()                  # Home team URL
    home_image = Field()                # Home team image
    away_url = Field()                  # Away team URL
    away_image = Field()                # Away team image
    match_url = Field()                 # Match details URL
    
    # Metadata
    extracted_at = Field()              # When this was extracted

class MatchDetailsLoader(ItemLoader):
    """Item loader for match details data"""
    
    default_item_class = MatchDetailsItem
    default_input_processor = MapCompose(clean_string)
    default_output_processor = TakeFirst()
    
    # Integer fields
    id_in = MapCompose(safe_int)
    home_id_in = MapCompose(safe_int)
    away_id_in = MapCompose(safe_int)
    round_id_in = MapCompose(safe_int)
    game_week_in = MapCompose(safe_int)
    revised_game_week_in = MapCompose(safe_int)
    competition_id_in = MapCompose(safe_int)
    home_goal_count_in = MapCompose(safe_int)
    away_goal_count_in = MapCompose(safe_int)
    total_goal_count_in = MapCompose(safe_int)
    winning_team_in = MapCompose(safe_int)
    ht_goals_team_a_in = MapCompose(safe_int)
    ht_goals_team_b_in = MapCompose(safe_int)
    ht_goal_count_in = MapCompose(safe_int)
    goals_2hg_team_a_in = MapCompose(safe_int)
    goals_2hg_team_b_in = MapCompose(safe_int)
    goal_count_2hg_in = MapCompose(safe_int)
    team_a_corners_in = MapCompose(safe_int)
    team_b_corners_in = MapCompose(safe_int)
    total_corner_count_in = MapCompose(safe_int)
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
    team_a_fouls_in = MapCompose(safe_int)
    team_b_fouls_in = MapCompose(safe_int)
    team_a_dangerous_attacks_in = MapCompose(safe_int)
    team_b_dangerous_attacks_in = MapCompose(safe_int)
    team_a_attacks_in = MapCompose(safe_int)
    team_b_attacks_in = MapCompose(safe_int)
    team_a_penalties_won_in = MapCompose(safe_int)
    team_b_penalties_won_in = MapCompose(safe_int)
    team_a_penalty_goals_in = MapCompose(safe_int)
    team_b_penalty_goals_in = MapCompose(safe_int)
    team_a_penalty_missed_in = MapCompose(safe_int)
    team_b_penalty_missed_in = MapCompose(safe_int)
    referee_id_in = MapCompose(safe_int)
    coach_a_id_in = MapCompose(safe_int)
    coach_b_id_in = MapCompose(safe_int)
    attendance_in = MapCompose(safe_int)
    
    # Float fields
    team_a_possession_in = MapCompose(safe_float)
    team_b_possession_in = MapCompose(safe_float)
    team_a_xg_in = MapCompose(safe_float)
    team_b_xg_in = MapCompose(safe_float)
    total_xg_in = MapCompose(safe_float)
    team_a_xg_prematch_in = MapCompose(safe_float)
    team_b_xg_prematch_in = MapCompose(safe_float)
    total_xg_prematch_in = MapCompose(safe_float)
    home_ppg_in = MapCompose(safe_float)
    away_ppg_in = MapCompose(safe_float)
    pre_match_home_ppg_in = MapCompose(safe_float)
    pre_match_away_ppg_in = MapCompose(safe_float)
    pre_match_team_a_overall_ppg_in = MapCompose(safe_float)
    pre_match_team_b_overall_ppg_in = MapCompose(safe_float)
    
    # All odds fields as floats
    odds_ft_1_in = MapCompose(safe_float)
    odds_ft_x_in = MapCompose(safe_float)
    odds_ft_2_in = MapCompose(safe_float)
    odds_ft_over05_in = MapCompose(safe_float)
    odds_ft_over15_in = MapCompose(safe_float)
    odds_ft_over25_in = MapCompose(safe_float)
    odds_ft_over35_in = MapCompose(safe_float)
    odds_ft_over45_in = MapCompose(safe_float)
    odds_ft_under05_in = MapCompose(safe_float)
    odds_ft_under15_in = MapCompose(safe_float)
    odds_ft_under25_in = MapCompose(safe_float)
    odds_ft_under35_in = MapCompose(safe_float)
    odds_ft_under45_in = MapCompose(safe_float)
    odds_btts_yes_in = MapCompose(safe_float)
    odds_btts_no_in = MapCompose(safe_float)
    
    # Timestamp
    date_unix_in = MapCompose(convert_unix_timestamp)
    extracted_at_in = MapCompose(lambda x: datetime.now())
    
    # Keep complex structures as-is
    lineups_out = Identity()
    bench_out = Identity()
    team_a_goal_details_out = Identity()
    team_b_goal_details_out = Identity()
    team_a_card_details_out = Identity()
    team_b_card_details_out = Identity()
    h2h_out = Identity()
    weather_out = Identity()
    trends_out = Identity()
    odds_comparison_out = Identity()
    home_goals_out = Identity()
    away_goals_out = Identity()

def validate_match_details_item(item_data: dict) -> bool:
    """Validate match details data structure before processing"""
    if not isinstance(item_data, dict):
        return False
    
    # Check for required basic fields
    required_fields = ['id', 'home_name', 'away_name']
    for field in required_fields:
        if field not in item_data or not item_data[field]:
            return False
    
    return True

def create_match_details_item(item_data: dict) -> MatchDetailsItem:
    """Create match details item from API data"""
    loader = MatchDetailsLoader()
    
    # Basic match information - map from actual JSON keys
    loader.add_value('id', item_data.get('id'))
    loader.add_value('home_id', item_data.get('homeID'))
    loader.add_value('away_id', item_data.get('awayID'))
    loader.add_value('home_name', item_data.get('home_name'))
    loader.add_value('away_name', item_data.get('away_name'))
    loader.add_value('season', item_data.get('season'))
    loader.add_value('status', item_data.get('status'))
    loader.add_value('round_id', item_data.get('roundID'))
    loader.add_value('game_week', item_data.get('game_week'))
    loader.add_value('revised_game_week', item_data.get('revised_game_week'))
    loader.add_value('date_unix', item_data.get('date_unix'))
    loader.add_value('competition_id', item_data.get('competition_id'))
    
    # Goals and scoring
    loader.add_value('home_goal_count', item_data.get('homeGoalCount'))
    loader.add_value('away_goal_count', item_data.get('awayGoalCount'))
    loader.add_value('total_goal_count', item_data.get('totalGoalCount'))
    loader.add_value('home_goals', item_data.get('homeGoals', []))
    loader.add_value('away_goals', item_data.get('awayGoals', []))
    loader.add_value('home_goals_timings', item_data.get('homeGoals_timings', []))
    loader.add_value('away_goals_timings', item_data.get('awayGoals_timings', []))
    loader.add_value('winning_team', item_data.get('winningTeam'))
    
    # Half-time statistics
    loader.add_value('ht_goals_team_a', item_data.get('ht_goals_team_a'))
    loader.add_value('ht_goals_team_b', item_data.get('ht_goals_team_b'))
    loader.add_value('ht_goal_count', item_data.get('HTGoalCount'))
    loader.add_value('goals_2hg_team_a', item_data.get('goals_2hg_team_a'))
    loader.add_value('goals_2hg_team_b', item_data.get('goals_2hg_team_b'))
    loader.add_value('goal_count_2hg', item_data.get('GoalCount_2hg'))
    
    # Match statistics
    loader.add_value('team_a_corners', item_data.get('team_a_corners'))
    loader.add_value('team_b_corners', item_data.get('team_b_corners'))
    loader.add_value('total_corner_count', item_data.get('totalCornerCount'))
    loader.add_value('team_a_offsides', item_data.get('team_a_offsides'))
    loader.add_value('team_b_offsides', item_data.get('team_b_offsides'))
    loader.add_value('team_a_yellow_cards', item_data.get('team_a_yellow_cards'))
    loader.add_value('team_b_yellow_cards', item_data.get('team_b_yellow_cards'))
    loader.add_value('team_a_red_cards', item_data.get('team_a_red_cards'))
    loader.add_value('team_b_red_cards', item_data.get('team_b_red_cards'))
    loader.add_value('team_a_shots_on_target', item_data.get('team_a_shotsOnTarget'))
    loader.add_value('team_b_shots_on_target', item_data.get('team_b_shotsOnTarget'))
    loader.add_value('team_a_shots_off_target', item_data.get('team_a_shotsOffTarget'))
    loader.add_value('team_b_shots_off_target', item_data.get('team_b_shotsOffTarget'))
    loader.add_value('team_a_shots', item_data.get('team_a_shots'))
    loader.add_value('team_b_shots', item_data.get('team_b_shots'))
    loader.add_value('team_a_fouls', item_data.get('team_a_fouls'))
    loader.add_value('team_b_fouls', item_data.get('team_b_fouls'))
    loader.add_value('team_a_possession', item_data.get('team_a_possession'))
    loader.add_value('team_b_possession', item_data.get('team_b_possession'))
    
    # Advanced statistics
    loader.add_value('team_a_xg', item_data.get('team_a_xg'))
    loader.add_value('team_b_xg', item_data.get('team_b_xg'))
    loader.add_value('total_xg', item_data.get('total_xg'))
    loader.add_value('team_a_xg_prematch', item_data.get('team_a_xg_prematch'))
    loader.add_value('team_b_xg_prematch', item_data.get('team_b_xg_prematch'))
    loader.add_value('total_xg_prematch', item_data.get('total_xg_prematch'))
    loader.add_value('team_a_dangerous_attacks', item_data.get('team_a_dangerous_attacks'))
    loader.add_value('team_b_dangerous_attacks', item_data.get('team_b_dangerous_attacks'))
    loader.add_value('team_a_attacks', item_data.get('team_a_attacks'))
    loader.add_value('team_b_attacks', item_data.get('team_b_attacks'))
    
    # Penalties
    loader.add_value('team_a_penalties_won', item_data.get('team_a_penalties_won'))
    loader.add_value('team_b_penalties_won', item_data.get('team_b_penalties_won'))
    loader.add_value('team_a_penalty_goals', item_data.get('team_a_penalty_goals'))
    loader.add_value('team_b_penalty_goals', item_data.get('team_b_penalty_goals'))
    loader.add_value('team_a_penalty_missed', item_data.get('team_a_penalty_missed'))
    loader.add_value('team_b_penalty_missed', item_data.get('team_b_penalty_missed'))
    
    # Pre-match team statistics
    loader.add_value('home_ppg', item_data.get('home_ppg'))
    loader.add_value('away_ppg', item_data.get('away_ppg'))
    loader.add_value('pre_match_home_ppg', item_data.get('pre_match_home_ppg'))
    loader.add_value('pre_match_away_ppg', item_data.get('pre_match_away_ppg'))
    loader.add_value('pre_match_team_a_overall_ppg', item_data.get('pre_match_teamA_overall_ppg'))
    loader.add_value('pre_match_team_b_overall_ppg', item_data.get('pre_match_teamB_overall_ppg'))
    
    # Odds data - map from actual JSON keys
    loader.add_value('odds_ft_1', item_data.get('odds_ft_1'))
    loader.add_value('odds_ft_x', item_data.get('odds_ft_x'))
    loader.add_value('odds_ft_2', item_data.get('odds_ft_2'))
    loader.add_value('odds_ft_over05', item_data.get('odds_ft_over05'))
    loader.add_value('odds_ft_over15', item_data.get('odds_ft_over15'))
    loader.add_value('odds_ft_over25', item_data.get('odds_ft_over25'))
    loader.add_value('odds_ft_over35', item_data.get('odds_ft_over35'))
    loader.add_value('odds_ft_over45', item_data.get('odds_ft_over45'))
    loader.add_value('odds_ft_under05', item_data.get('odds_ft_under05'))
    loader.add_value('odds_ft_under15', item_data.get('odds_ft_under15'))
    loader.add_value('odds_ft_under25', item_data.get('odds_ft_under25'))
    loader.add_value('odds_ft_under35', item_data.get('odds_ft_under35'))
    loader.add_value('odds_ft_under45', item_data.get('odds_ft_under45'))
    loader.add_value('odds_btts_yes', item_data.get('odds_btts_yes'))
    loader.add_value('odds_btts_no', item_data.get('odds_btts_no'))
    
    # Match context
    loader.add_value('referee_id', item_data.get('refereeID'))
    loader.add_value('coach_a_id', item_data.get('coach_a_ID'))
    loader.add_value('coach_b_id', item_data.get('coach_b_ID'))
    loader.add_value('stadium_name', item_data.get('stadium_name'))
    loader.add_value('stadium_location', item_data.get('stadium_location'))
    loader.add_value('attendance', item_data.get('attendance'))
    
    # Complex nested data
    loader.add_value('lineups', item_data.get('lineups'))
    loader.add_value('bench', item_data.get('bench'))
    loader.add_value('team_a_goal_details', item_data.get('team_a_goal_details', []))
    loader.add_value('team_b_goal_details', item_data.get('team_b_goal_details', []))
    loader.add_value('team_a_card_details', item_data.get('team_a_card_details', []))
    loader.add_value('team_b_card_details', item_data.get('team_b_card_details', []))
    loader.add_value('h2h', item_data.get('h2h'))
    loader.add_value('weather', item_data.get('weather'))
    
    # Additional data
    loader.add_value('trends', item_data.get('trends'))
    loader.add_value('tv_stations', item_data.get('tv_stations'))
    loader.add_value('odds_comparison', item_data.get('odds_comparison'))
    
    # URLs and images
    loader.add_value('home_url', item_data.get('home_url'))
    loader.add_value('home_image', item_data.get('home_image'))
    loader.add_value('away_url', item_data.get('away_url'))
    loader.add_value('away_image', item_data.get('away_image'))
    loader.add_value('match_url', item_data.get('match_url'))
    
    # Metadata
    loader.add_value('extracted_at', None)
    
    return loader.load_item()