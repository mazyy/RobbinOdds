# scrapy/odds_scraper/odds_scraper/items/footystats/league_matches_items.py

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
    
    # ===== BASIC MATCH INFORMATION =====
    id = Field()                        # Match ID
    homeID = Field()                    # Home team ID  
    awayID = Field()                    # Away team ID
    home_name = Field()                 # Home team name
    away_name = Field()                 # Away team name
    season = Field()                    # Season string
    seasonID = Field()                  # Season ID
    status = Field()                    # Match status
    roundID = Field()                   # Round ID
    game_week = Field()                 # Game week
    revised_game_week = Field()         # Revised game week
    date_unix = Field()                 # Match timestamp
    
    # ===== GOALS AND SCORING =====
    homeGoalCount = Field()             # Home team goals
    awayGoalCount = Field()             # Away team goals
    totalGoalCount = Field()            # Total goals
    overallGoalCount = Field()          # Overall goal count
    homeGoals = Field()                 # Home goal timings (array)
    awayGoals = Field()                 # Away goal timings (array)
    home_team_goal_timings = Field()    # Home goal timing details
    away_team_goal_timings = Field()    # Away goal timing details
    
    # ===== HALF-TIME STATISTICS =====
    home_team_goal_count_half_time = Field()  # HT home goals
    away_team_goal_count_half_time = Field()  # HT away goals
    total_goal_count_half_time = Field()      # HT total goals
    ht_goals_team_a = Field()           # HT home goals
    ht_goals_team_b = Field()           # HT away goals
    HTGoalCount = Field()               # HT goal count
    
    # ===== SECOND HALF STATISTICS =====
    goals_2hg_team_a = Field()          # 2H home goals
    goals_2hg_team_b = Field()          # 2H away goals
    GoalCount_2hg = Field()             # 2H goal count
    
    # ===== MATCH STATISTICS =====
    team_a_corners = Field()            # Home team corners
    team_b_corners = Field()            # Away team corners
    team_a_fh_corners = Field()         # Home 1H corners
    team_b_fh_corners = Field()         # Away 1H corners
    team_a_2h_corners = Field()         # Home 2H corners
    team_b_2h_corners = Field()         # Away 2H corners
    corner_fh_count = Field()           # 1H corner count
    corner_2h_count = Field()           # 2H corner count
    
    team_a_offsides = Field()           # Home team offsides
    team_b_offsides = Field()           # Away team offsides
    
    # ===== CARDS STATISTICS =====
    team_a_yellow_cards = Field()       # Home yellow cards
    team_b_yellow_cards = Field()       # Away yellow cards
    team_a_red_cards = Field()          # Home red cards
    team_b_red_cards = Field()          # Away red cards
    team_a_fh_cards = Field()           # Home 1H cards
    team_b_fh_cards = Field()           # Away 1H cards
    team_a_2h_cards = Field()           # Home 2H cards
    team_b_2h_cards = Field()           # Away 2H cards
    total_fh_cards = Field()            # 1H total cards
    total_2h_cards = Field()            # 2H total cards
    team_a_cards_num = Field()          # Home cards number
    team_b_cards_num = Field()          # Away cards number
    
    # ===== SHOTS STATISTICS =====
    team_a_shots_on_target = Field()   # Home shots on target
    team_b_shots_on_target = Field()   # Away shots on target
    team_a_shots_off_target = Field()  # Home shots off target
    team_b_shots_off_target = Field()  # Away shots off target
    team_a_shots = Field()              # Home total shots
    team_b_shots = Field()              # Away total shots
    
    # ===== POSSESSION AND ATTACKS =====
    team_a_possession = Field()         # Home possession
    team_b_possession = Field()         # Away possession
    team_a_attacks = Field()            # Home attacks
    team_b_attacks = Field()            # Away attacks
    team_a_dangerous_attacks = Field()  # Home dangerous attacks
    team_b_dangerous_attacks = Field()  # Away dangerous attacks
    
    # ===== XG STATISTICS =====
    team_a_xg = Field()                 # Home xG
    team_b_xg = Field()                 # Away xG
    total_xg = Field()                  # Total xG
    team_a_xg_prematch = Field()        # Home pre-match xG
    team_b_xg_prematch = Field()        # Away pre-match xG
    total_xg_prematch = Field()         # Total pre-match xG
    
    # ===== PENALTIES =====
    team_a_penalties_won = Field()      # Home penalties won
    team_b_penalties_won = Field()      # Away penalties won
    team_a_penalty_goals = Field()      # Home penalty goals
    team_b_penalty_goals = Field()      # Away penalty goals
    team_a_penalty_missed = Field()     # Home penalties missed
    team_b_penalty_missed = Field()     # Away penalties missed
    
    # ===== SET PIECES =====
    team_a_throwins = Field()           # Home throw-ins
    team_b_throwins = Field()           # Away throw-ins
    team_a_freekicks = Field()          # Home free kicks
    team_b_freekicks = Field()          # Away free kicks
    team_a_goalkicks = Field()          # Home goal kicks
    team_b_goalkicks = Field()          # Away goal kicks
    
    # ===== EARLY MATCH STATISTICS =====
    team_a_0_10_min_goals = Field()     # Home 0-10 min goals
    team_b_0_10_min_goals = Field()     # Away 0-10 min goals
    team_a_corners_0_10_min = Field()   # Home 0-10 min corners
    team_b_corners_0_10_min = Field()   # Away 0-10 min corners
    team_a_cards_0_10_min = Field()     # Home 0-10 min cards
    team_b_cards_0_10_min = Field()     # Away 0-10 min cards
    
    # ===== PRE-MATCH STATISTICS =====
    pre_match_teamA_ppg = Field()       # Pre-match home PPG
    pre_match_teamB_ppg = Field()       # Pre-match away PPG
    pre_match_home_ppg = Field()        # Pre-match home PPG
    pre_match_away_ppg = Field()        # Pre-match away PPG
    pre_match_teamA_overall_ppg = Field() # Pre-match home overall PPG
    pre_match_teamB_overall_ppg = Field() # Pre-match away overall PPG
    pre_match_teamA_overall_avg_goals_per_match_pre_match = Field()
    pre_match_teamB_overall_avg_goals_per_match_pre_match = Field()
    home_ppg = Field()                  # Home PPG
    away_ppg = Field()                  # Away PPG
    
    # ===== MAIN ODDS INFORMATION =====
    odds_ft_1 = Field()                 # Home win odds
    odds_ft_x = Field()                 # Draw odds
    odds_ft_2 = Field()                 # Away win odds
    
    # ===== OVER/UNDER ODDS =====
    odds_ft_over05 = Field()            # Over 0.5 odds
    odds_ft_under05 = Field()           # Under 0.5 odds
    odds_ft_over15 = Field()            # Over 1.5 odds
    odds_ft_under15 = Field()           # Under 1.5 odds
    odds_ft_over25 = Field()            # Over 2.5 odds
    odds_ft_under25 = Field()           # Under 2.5 odds
    odds_ft_over35 = Field()            # Over 3.5 odds
    odds_ft_under35 = Field()           # Under 3.5 odds
    odds_ft_over45 = Field()            # Over 4.5 odds
    odds_ft_under45 = Field()           # Under 4.5 odds
    
    # ===== BTTS AND CLEAN SHEETS =====
    odds_btts_yes = Field()             # BTTS Yes odds
    odds_btts_no = Field()              # BTTS No odds
    odds_team_a_cs_yes = Field()        # Home clean sheet yes
    odds_team_a_cs_no = Field()         # Home clean sheet no
    odds_team_b_cs_yes = Field()        # Away clean sheet yes
    odds_team_b_cs_no = Field()         # Away clean sheet no
    
    # ===== DOUBLE CHANCE ODDS =====
    odds_doublechance_1x = Field()      # 1X double chance
    odds_doublechance_12 = Field()      # 12 double chance
    odds_doublechance_x2 = Field()      # X2 double chance
    
    # ===== HALF-TIME RESULT ODDS =====
    odds_1st_half_result_1 = Field()    # 1st half home win
    odds_1st_half_result_x = Field()    # 1st half draw
    odds_1st_half_result_2 = Field()    # 1st half away win
    odds_2nd_half_result_1 = Field()    # 2nd half home win
    odds_2nd_half_result_x = Field()    # 2nd half draw
    odds_2nd_half_result_2 = Field()    # 2nd half away win
    
    # ===== DRAW NO BET ODDS =====
    odds_dnb_1 = Field()                # Home draw no bet
    odds_dnb_2 = Field()                # Away draw no bet
    
    # ===== CORNERS ODDS =====
    odds_corners_over_75 = Field()      # Corners over 7.5
    odds_corners_over_85 = Field()      # Corners over 8.5
    odds_corners_over_95 = Field()      # Corners over 9.5
    odds_corners_over_105 = Field()     # Corners over 10.5
    odds_corners_over_115 = Field()     # Corners over 11.5
    odds_corners_under_75 = Field()     # Corners under 7.5
    odds_corners_under_85 = Field()     # Corners under 8.5
    odds_corners_under_95 = Field()     # Corners under 9.5
    odds_corners_under_105 = Field()    # Corners under 10.5
    odds_corners_under_115 = Field()    # Corners under 11.5
    odds_corners_1 = Field()            # Home more corners
    odds_corners_x = Field()            # Equal corners
    odds_corners_2 = Field()            # Away more corners
    
    # ===== FIRST GOAL AND WIN TO NIL ODDS =====
    odds_team_to_score_first_1 = Field() # Home to score first
    odds_team_to_score_first_x = Field() # No goal
    odds_team_to_score_first_2 = Field() # Away to score first
    odds_win_to_nil_1 = Field()         # Home win to nil
    odds_win_to_nil_2 = Field()         # Away win to nil
    
    # ===== HALF-TIME OVER/UNDER ODDS =====
    odds_1st_half_over05 = Field()      # 1H over 0.5
    odds_1st_half_over15 = Field()      # 1H over 1.5
    odds_1st_half_over25 = Field()      # 1H over 2.5
    odds_1st_half_over35 = Field()      # 1H over 3.5
    odds_1st_half_under05 = Field()     # 1H under 0.5
    odds_1st_half_under15 = Field()     # 1H under 1.5
    odds_1st_half_under25 = Field()     # 1H under 2.5
    odds_1st_half_under35 = Field()     # 1H under 3.5
    
    # ===== SECOND HALF OVER/UNDER ODDS =====
    odds_2nd_half_over05 = Field()      # 2H over 0.5
    odds_2nd_half_over15 = Field()      # 2H over 1.5
    odds_2nd_half_over25 = Field()      # 2H over 2.5
    odds_2nd_half_over35 = Field()      # 2H over 3.5
    odds_2nd_half_under05 = Field()     # 2H under 0.5
    odds_2nd_half_under15 = Field()     # 2H under 1.5
    odds_2nd_half_under25 = Field()     # 2H under 2.5
    odds_2nd_half_under35 = Field()     # 2H under 3.5
    
    # ===== HALF-TIME BTTS ODDS =====
    odds_btts_1st_half_yes = Field()    # 1H BTTS yes
    odds_btts_1st_half_no = Field()     # 1H BTTS no
    odds_btts_2nd_half_yes = Field()    # 2H BTTS yes
    odds_btts_2nd_half_no = Field()     # 2H BTTS no
    
    # ===== MATCH CONTEXT =====
    referee_id = Field()                # Referee ID
    coach_id_team_a = Field()           # Home coach ID
    coach_id_team_b = Field()           # Away coach ID
    stadium_name = Field()              # Stadium name
    stadium_location = Field()          # Stadium location
    attendance = Field()                # Attendance figure
    winningTeam = Field()               # Winning team ID
    winner_team_id = Field()            # Winner team ID (-1 for draw)
    no_home_away = Field()              # No home/away flag
    
    # ===== POTENTIAL AND STATISTICS FLAGS =====
    btts_potential = Field()            # BTTS potential
    btts_fhg_potential = Field()        # BTTS first half potential
    btts_2hg_potential = Field()        # BTTS second half potential
    o45_potential = Field()             # Over 4.5 potential
    o35_potential = Field()             # Over 3.5 potential
    o25_potential = Field()             # Over 2.5 potential
    o15_potential = Field()             # Over 1.5 potential
    o05_potential = Field()             # Over 0.5 potential
    u45_potential = Field()             # Under 4.5 potential
    u35_potential = Field()             # Under 3.5 potential
    u25_potential = Field()             # Under 2.5 potential
    u15_potential = Field()             # Under 1.5 potential
    u05_potential = Field()             # Under 0.5 potential
    o15HT_potential = Field()           # Over 1.5 HT potential
    o05HT_potential = Field()           # Over 0.5 HT potential
    o05_2H_potential = Field()          # Over 0.5 2H potential
    o15_2H_potential = Field()          # Over 1.5 2H potential
    corners_potential = Field()         # Corners potential
    corners_o85_potential = Field()     # Corners over 8.5 potential
    corners_o95_potential = Field()     # Corners over 9.5 potential
    corners_o105_potential = Field()    # Corners over 10.5 potential
    offsides_potential = Field()        # Offsides potential
    cards_potential = Field()           # Cards potential
    avg_potential = Field()             # Average potential
    
    # ===== RECORDING FLAGS =====
    goalTimingDisabled = Field()        # Goal timing disabled flag
    corner_timings_recorded = Field()   # Corner timings recorded flag
    card_timings_recorded = Field()     # Card timings recorded flag
    attacks_recorded = Field()          # Attacks recorded flag
    pens_recorded = Field()             # Penalties recorded flag
    goal_timings_recorded = Field()     # Goal timings recorded flag
    throwins_recorded = Field()         # Throw-ins recorded flag
    freekicks_recorded = Field()        # Free kicks recorded flag
    goalkicks_recorded = Field()        # Goal kicks recorded flag
    
    # ===== STATISTICAL FLAGS =====
    over_05 = Field()                   # Over 0.5 goals flag
    over_15 = Field()                   # Over 1.5 goals flag
    over_25 = Field()                   # Over 2.5 goals flag
    over_35 = Field()                   # Over 3.5 goals flag
    over_45 = Field()                   # Over 4.5 goals flag
    btts = Field()                      # BTTS flag
    
    # ===== TEAM INFO =====
    home_url = Field()                  # Home team URL
    home_image = Field()                # Home team image
    away_url = Field()                  # Away team URL
    away_image = Field()                # Away team image
    
    # ===== METADATA =====
    extracted_at = Field()              # When this was extracted

class LeagueMatchLoader(ItemLoader):
    """Item loader for league match data"""
    
    default_item_class = LeagueMatchItem
    default_input_processor = MapCompose(clean_string)
    default_output_processor = TakeFirst()
    
    # ===== INTEGER FIELDS =====
    id_in = MapCompose(safe_int)
    homeID_in = MapCompose(safe_int)
    awayID_in = MapCompose(safe_int)
    seasonID_in = MapCompose(safe_int)
    roundID_in = MapCompose(safe_int)
    game_week_in = MapCompose(safe_int)
    revised_game_week_in = MapCompose(safe_int)
    
    # Goals
    homeGoalCount_in = MapCompose(safe_int)
    awayGoalCount_in = MapCompose(safe_int)
    totalGoalCount_in = MapCompose(safe_int)
    overallGoalCount_in = MapCompose(safe_int)
    ht_goals_team_a_in = MapCompose(safe_int)
    ht_goals_team_b_in = MapCompose(safe_int)
    HTGoalCount_in = MapCompose(safe_int)
    goals_2hg_team_a_in = MapCompose(safe_int)
    goals_2hg_team_b_in = MapCompose(safe_int)
    GoalCount_2hg_in = MapCompose(safe_int)
    
    # Corners
    team_a_corners_in = MapCompose(safe_int)
    team_b_corners_in = MapCompose(safe_int)
    team_a_fh_corners_in = MapCompose(safe_int)
    team_b_fh_corners_in = MapCompose(safe_int)
    team_a_2h_corners_in = MapCompose(safe_int)
    team_b_2h_corners_in = MapCompose(safe_int)
    corner_fh_count_in = MapCompose(safe_int)
    corner_2h_count_in = MapCompose(safe_int)
    
    # Cards
    team_a_yellow_cards_in = MapCompose(safe_int)
    team_b_yellow_cards_in = MapCompose(safe_int)
    team_a_red_cards_in = MapCompose(safe_int)
    team_b_red_cards_in = MapCompose(safe_int)
    team_a_fh_cards_in = MapCompose(safe_int)
    team_b_fh_cards_in = MapCompose(safe_int)
    team_a_2h_cards_in = MapCompose(safe_int)
    team_b_2h_cards_in = MapCompose(safe_int)
    total_fh_cards_in = MapCompose(safe_int)
    total_2h_cards_in = MapCompose(safe_int)
    team_a_cards_num_in = MapCompose(safe_int)
    team_b_cards_num_in = MapCompose(safe_int)
    
    # Shots
    team_a_shots_on_target_in = MapCompose(safe_int)
    team_b_shots_on_target_in = MapCompose(safe_int)
    team_a_shots_off_target_in = MapCompose(safe_int)
    team_b_shots_off_target_in = MapCompose(safe_int)
    team_a_shots_in = MapCompose(safe_int)
    team_b_shots_in = MapCompose(safe_int)
    
    # Attacks
    team_a_attacks_in = MapCompose(safe_int)
    team_b_attacks_in = MapCompose(safe_int)
    team_a_dangerous_attacks_in = MapCompose(safe_int)
    team_b_dangerous_attacks_in = MapCompose(safe_int)
    
    # Penalties
    team_a_penalties_won_in = MapCompose(safe_int)
    team_b_penalties_won_in = MapCompose(safe_int)
    team_a_penalty_goals_in = MapCompose(safe_int)
    team_b_penalty_goals_in = MapCompose(safe_int)
    team_a_penalty_missed_in = MapCompose(safe_int)
    team_b_penalty_missed_in = MapCompose(safe_int)
    
    # Set pieces
    team_a_throwins_in = MapCompose(safe_int)
    team_b_throwins_in = MapCompose(safe_int)
    team_a_freekicks_in = MapCompose(safe_int)
    team_b_freekicks_in = MapCompose(safe_int)
    team_a_goalkicks_in = MapCompose(safe_int)
    team_b_goalkicks_in = MapCompose(safe_int)
    
    # Early match stats
    team_a_0_10_min_goals_in = MapCompose(safe_int)
    team_b_0_10_min_goals_in = MapCompose(safe_int)
    team_a_corners_0_10_min_in = MapCompose(safe_int)
    team_b_corners_0_10_min_in = MapCompose(safe_int)
    team_a_cards_0_10_min_in = MapCompose(safe_int)
    team_b_cards_0_10_min_in = MapCompose(safe_int)
    
    # Other integers
    attendance_in = MapCompose(safe_int)
    winningTeam_in = MapCompose(safe_int)
    winner_team_id_in = MapCompose(safe_int)
    no_home_away_in = MapCompose(safe_int)
    referee_id_in = MapCompose(safe_int)
    coach_id_team_a_in = MapCompose(safe_int)
    coach_id_team_b_in = MapCompose(safe_int)
    
    # Recording flags
    goalTimingDisabled_in = MapCompose(safe_int)
    corner_timings_recorded_in = MapCompose(safe_int)
    card_timings_recorded_in = MapCompose(safe_int)
    attacks_recorded_in = MapCompose(safe_int)
    pens_recorded_in = MapCompose(safe_int)
    goal_timings_recorded_in = MapCompose(safe_int)
    throwins_recorded_in = MapCompose(safe_int)
    freekicks_recorded_in = MapCompose(safe_int)
    goalkicks_recorded_in = MapCompose(safe_int)
    
    # ===== FLOAT FIELDS =====
    # Possession
    team_a_possession_in = MapCompose(safe_float)
    team_b_possession_in = MapCompose(safe_float)
    
    # xG stats
    team_a_xg_in = MapCompose(safe_float)
    team_b_xg_in = MapCompose(safe_float)
    total_xg_in = MapCompose(safe_float)
    team_a_xg_prematch_in = MapCompose(safe_float)
    team_b_xg_prematch_in = MapCompose(safe_float)
    total_xg_prematch_in = MapCompose(safe_float)
    
    # Pre-match stats
    pre_match_teamA_ppg_in = MapCompose(safe_float)
    pre_match_teamB_ppg_in = MapCompose(safe_float)
    pre_match_home_ppg_in = MapCompose(safe_float)
    pre_match_away_ppg_in = MapCompose(safe_float)
    pre_match_teamA_overall_ppg_in = MapCompose(safe_float)
    pre_match_teamB_overall_ppg_in = MapCompose(safe_float)
    home_ppg_in = MapCompose(safe_float)
    away_ppg_in = MapCompose(safe_float)
    
    # Odds fields - all as floats
    odds_ft_1_in = MapCompose(safe_float)
    odds_ft_x_in = MapCompose(safe_float)
    odds_ft_2_in = MapCompose(safe_float)
    odds_ft_over05_in = MapCompose(safe_float)
    odds_ft_under05_in = MapCompose(safe_float)
    odds_ft_over15_in = MapCompose(safe_float)
    odds_ft_under15_in = MapCompose(safe_float)
    odds_ft_over25_in = MapCompose(safe_float)
    odds_ft_under25_in = MapCompose(safe_float)
    odds_ft_over35_in = MapCompose(safe_float)
    odds_ft_under35_in = MapCompose(safe_float)
    odds_ft_over45_in = MapCompose(safe_float)
    odds_ft_under45_in = MapCompose(safe_float)
    odds_btts_yes_in = MapCompose(safe_float)
    odds_btts_no_in = MapCompose(safe_float)
    odds_team_a_cs_yes_in = MapCompose(safe_float)
    odds_team_a_cs_no_in = MapCompose(safe_float)
    odds_team_b_cs_yes_in = MapCompose(safe_float)
    odds_team_b_cs_no_in = MapCompose(safe_float)
    odds_doublechance_1x_in = MapCompose(safe_float)
    odds_doublechance_12_in = MapCompose(safe_float)
    odds_doublechance_x2_in = MapCompose(safe_float)
    odds_1st_half_result_1_in = MapCompose(safe_float)
    odds_1st_half_result_x_in = MapCompose(safe_float)
    odds_1st_half_result_2_in = MapCompose(safe_float)
    odds_2nd_half_result_1_in = MapCompose(safe_float)
    odds_2nd_half_result_x_in = MapCompose(safe_float)
    odds_2nd_half_result_2_in = MapCompose(safe_float)
    odds_dnb_1_in = MapCompose(safe_float)
    odds_dnb_2_in = MapCompose(safe_float)
    
    # Corners odds
    odds_corners_over_75_in = MapCompose(safe_float)
    odds_corners_over_85_in = MapCompose(safe_float)
    odds_corners_over_95_in = MapCompose(safe_float)
    odds_corners_over_105_in = MapCompose(safe_float)
    odds_corners_over_115_in = MapCompose(safe_float)
    odds_corners_under_75_in = MapCompose(safe_float)
    odds_corners_under_85_in = MapCompose(safe_float)
    odds_corners_under_95_in = MapCompose(safe_float)
    odds_corners_under_105_in = MapCompose(safe_float)
    odds_corners_under_115_in = MapCompose(safe_float)
    odds_corners_1_in = MapCompose(safe_float)
    odds_corners_x_in = MapCompose(safe_float)
    odds_corners_2_in = MapCompose(safe_float)
    
    # First goal and win to nil odds
    odds_team_to_score_first_1_in = MapCompose(safe_float)
    odds_team_to_score_first_x_in = MapCompose(safe_float)
    odds_team_to_score_first_2_in = MapCompose(safe_float)
    odds_win_to_nil_1_in = MapCompose(safe_float)
    odds_win_to_nil_2_in = MapCompose(safe_float)
    
    # Half-time over/under odds
    odds_1st_half_over05_in = MapCompose(safe_float)
    odds_1st_half_over15_in = MapCompose(safe_float)
    odds_1st_half_over25_in = MapCompose(safe_float)
    odds_1st_half_over35_in = MapCompose(safe_float)
    odds_1st_half_under05_in = MapCompose(safe_float)
    odds_1st_half_under15_in = MapCompose(safe_float)
    odds_1st_half_under25_in = MapCompose(safe_float)
    odds_1st_half_under35_in = MapCompose(safe_float)
    
    # Second half over/under odds
    odds_2nd_half_over05_in = MapCompose(safe_float)
    odds_2nd_half_over15_in = MapCompose(safe_float)
    odds_2nd_half_over25_in = MapCompose(safe_float)
    odds_2nd_half_over35_in = MapCompose(safe_float)
    odds_2nd_half_under05_in = MapCompose(safe_float)
    odds_2nd_half_under15_in = MapCompose(safe_float)
    odds_2nd_half_under25_in = MapCompose(safe_float)
    odds_2nd_half_under35_in = MapCompose(safe_float)
    
    # Half-time BTTS odds
    odds_btts_1st_half_yes_in = MapCompose(safe_float)
    odds_btts_1st_half_no_in = MapCompose(safe_float)
    odds_btts_2nd_half_yes_in = MapCompose(safe_float)
    odds_btts_2nd_half_no_in = MapCompose(safe_float)
    
    # Potential fields
    btts_potential_in = MapCompose(safe_float)
    btts_fhg_potential_in = MapCompose(safe_float)
    btts_2hg_potential_in = MapCompose(safe_float)
    o45_potential_in = MapCompose(safe_float)
    o35_potential_in = MapCompose(safe_float)
    o25_potential_in = MapCompose(safe_float)
    o15_potential_in = MapCompose(safe_float)
    o05_potential_in = MapCompose(safe_float)
    u45_potential_in = MapCompose(safe_float)
    u35_potential_in = MapCompose(safe_float)
    u25_potential_in = MapCompose(safe_float)
    u15_potential_in = MapCompose(safe_float)
    u05_potential_in = MapCompose(safe_float)
    o15HT_potential_in = MapCompose(safe_float)
    o05HT_potential_in = MapCompose(safe_float)
    o05_2H_potential_in = MapCompose(safe_float)
    o15_2H_potential_in = MapCompose(safe_float)
    corners_potential_in = MapCompose(safe_float)
    corners_o85_potential_in = MapCompose(safe_float)
    corners_o95_potential_in = MapCompose(safe_float)
    corners_o105_potential_in = MapCompose(safe_float)
    offsides_potential_in = MapCompose(safe_float)
    cards_potential_in = MapCompose(safe_float)
    avg_potential_in = MapCompose(safe_float)
    
    # ===== BOOLEAN FIELDS =====
    over_05_in = MapCompose(lambda x: bool(x) if x is not None else None)
    over_15_in = MapCompose(lambda x: bool(x) if x is not None else None)
    over_25_in = MapCompose(lambda x: bool(x) if x is not None else None)
    over_35_in = MapCompose(lambda x: bool(x) if x is not None else None)
    over_45_in = MapCompose(lambda x: bool(x) if x is not None else None)
    btts_in = MapCompose(lambda x: bool(x) if x is not None else None)
    
    # ===== TIMESTAMP =====
    date_unix_in = MapCompose(convert_unix_timestamp)
    extracted_at_in = MapCompose(lambda x: datetime.now())
    
    # ===== ARRAY FIELDS (keep as lists) =====
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
    
    # ===== BASIC MATCH INFORMATION =====
    loader.add_value('id', item_data.get('id'))
    loader.add_value('homeID', item_data.get('homeID'))
    loader.add_value('awayID', item_data.get('awayID'))
    loader.add_value('home_name', item_data.get('home_name'))
    loader.add_value('away_name', item_data.get('away_name'))
    loader.add_value('season', item_data.get('season'))
    loader.add_value('seasonID', item_data.get('seasonID'))
    loader.add_value('status', item_data.get('status'))
    loader.add_value('roundID', item_data.get('roundID'))
    loader.add_value('game_week', item_data.get('game_week'))
    loader.add_value('revised_game_week', item_data.get('revised_game_week'))
    loader.add_value('date_unix', item_data.get('date_unix'))
    
    # ===== GOALS AND SCORING =====
    loader.add_value('homeGoalCount', item_data.get('homeGoalCount'))
    loader.add_value('awayGoalCount', item_data.get('awayGoalCount'))
    loader.add_value('totalGoalCount', item_data.get('totalGoalCount'))
    loader.add_value('overallGoalCount', item_data.get('overallGoalCount'))
    loader.add_value('homeGoals', item_data.get('homeGoals', []))
    loader.add_value('awayGoals', item_data.get('awayGoals', []))
    loader.add_value('home_team_goal_timings', item_data.get('home_team_goal_timings', []))
    loader.add_value('away_team_goal_timings', item_data.get('away_team_goal_timings', []))
    
    # ===== HALF-TIME STATISTICS =====
    loader.add_value('home_team_goal_count_half_time', item_data.get('home_team_goal_count_half_time'))
    loader.add_value('away_team_goal_count_half_time', item_data.get('away_team_goal_count_half_time'))
    loader.add_value('total_goal_count_half_time', item_data.get('total_goal_count_half_time'))
    loader.add_value('ht_goals_team_a', item_data.get('ht_goals_team_a'))
    loader.add_value('ht_goals_team_b', item_data.get('ht_goals_team_b'))
    loader.add_value('HTGoalCount', item_data.get('HTGoalCount'))
    
    # ===== SECOND HALF STATISTICS =====
    loader.add_value('goals_2hg_team_a', item_data.get('goals_2hg_team_a'))
    loader.add_value('goals_2hg_team_b', item_data.get('goals_2hg_team_b'))
    loader.add_value('GoalCount_2hg', item_data.get('GoalCount_2hg'))
    
    # ===== MATCH STATISTICS =====
    loader.add_value('team_a_corners', item_data.get('team_a_corners'))
    loader.add_value('team_b_corners', item_data.get('team_b_corners'))
    loader.add_value('team_a_fh_corners', item_data.get('team_a_fh_corners'))
    loader.add_value('team_b_fh_corners', item_data.get('team_b_fh_corners'))
    loader.add_value('team_a_2h_corners', item_data.get('team_a_2h_corners'))
    loader.add_value('team_b_2h_corners', item_data.get('team_b_2h_corners'))
    loader.add_value('corner_fh_count', item_data.get('corner_fh_count'))
    loader.add_value('corner_2h_count', item_data.get('corner_2h_count'))
    loader.add_value('team_a_offsides', item_data.get('team_a_offsides'))
    loader.add_value('team_b_offsides', item_data.get('team_b_offsides'))
    
    # ===== CARDS STATISTICS =====
    loader.add_value('team_a_yellow_cards', item_data.get('team_a_yellow_cards'))
    loader.add_value('team_b_yellow_cards', item_data.get('team_b_yellow_cards'))
    loader.add_value('team_a_red_cards', item_data.get('team_a_red_cards'))
    loader.add_value('team_b_red_cards', item_data.get('team_b_red_cards'))
    loader.add_value('team_a_fh_cards', item_data.get('team_a_fh_cards'))
    loader.add_value('team_b_fh_cards', item_data.get('team_b_fh_cards'))
    loader.add_value('team_a_2h_cards', item_data.get('team_a_2h_cards'))
    loader.add_value('team_b_2h_cards', item_data.get('team_b_2h_cards'))
    loader.add_value('total_fh_cards', item_data.get('total_fh_cards'))
    loader.add_value('total_2h_cards', item_data.get('total_2h_cards'))
    loader.add_value('team_a_cards_num', item_data.get('team_a_cards_num'))
    loader.add_value('team_b_cards_num', item_data.get('team_b_cards_num'))
    
    # ===== SHOTS STATISTICS =====
    loader.add_value('team_a_shots_on_target', item_data.get('team_a_shots_on_target'))
    loader.add_value('team_b_shots_on_target', item_data.get('team_b_shots_on_target'))
    loader.add_value('team_a_shots_off_target', item_data.get('team_a_shots_off_target'))
    loader.add_value('team_b_shots_off_target', item_data.get('team_b_shots_off_target'))
    loader.add_value('team_a_shots', item_data.get('team_a_shots'))
    loader.add_value('team_b_shots', item_data.get('team_b_shots'))
    
    # ===== POSSESSION AND ATTACKS =====
    loader.add_value('team_a_possession', item_data.get('team_a_possession'))
    loader.add_value('team_b_possession', item_data.get('team_b_possession'))
    loader.add_value('team_a_attacks', item_data.get('team_a_attacks'))
    loader.add_value('team_b_attacks', item_data.get('team_b_attacks'))
    loader.add_value('team_a_dangerous_attacks', item_data.get('team_a_dangerous_attacks'))
    loader.add_value('team_b_dangerous_attacks', item_data.get('team_b_dangerous_attacks'))
    
    # ===== XG STATISTICS =====
    loader.add_value('team_a_xg', item_data.get('team_a_xg'))
    loader.add_value('team_b_xg', item_data.get('team_b_xg'))
    loader.add_value('total_xg', item_data.get('total_xg'))
    loader.add_value('team_a_xg_prematch', item_data.get('team_a_xg_prematch'))
    loader.add_value('team_b_xg_prematch', item_data.get('team_b_xg_prematch'))
    loader.add_value('total_xg_prematch', item_data.get('total_xg_prematch'))
    
    # ===== PENALTIES =====
    loader.add_value('team_a_penalties_won', item_data.get('team_a_penalties_won'))
    loader.add_value('team_b_penalties_won', item_data.get('team_b_penalties_won'))
    loader.add_value('team_a_penalty_goals', item_data.get('team_a_penalty_goals'))
    loader.add_value('team_b_penalty_goals', item_data.get('team_b_penalty_goals'))
    loader.add_value('team_a_penalty_missed', item_data.get('team_a_penalty_missed'))
    loader.add_value('team_b_penalty_missed', item_data.get('team_b_penalty_missed'))
    
    # ===== SET PIECES =====
    loader.add_value('team_a_throwins', item_data.get('team_a_throwins'))
    loader.add_value('team_b_throwins', item_data.get('team_b_throwins'))
    loader.add_value('team_a_freekicks', item_data.get('team_a_freekicks'))
    loader.add_value('team_b_freekicks', item_data.get('team_b_freekicks'))
    loader.add_value('team_a_goalkicks', item_data.get('team_a_goalkicks'))
    loader.add_value('team_b_goalkicks', item_data.get('team_b_goalkicks'))
    
    # ===== EARLY MATCH STATISTICS =====
    loader.add_value('team_a_0_10_min_goals', item_data.get('team_a_0_10_min_goals'))
    loader.add_value('team_b_0_10_min_goals', item_data.get('team_b_0_10_min_goals'))
    loader.add_value('team_a_corners_0_10_min', item_data.get('team_a_corners_0_10_min'))
    loader.add_value('team_b_corners_0_10_min', item_data.get('team_b_corners_0_10_min'))
    loader.add_value('team_a_cards_0_10_min', item_data.get('team_a_cards_0_10_min'))
    loader.add_value('team_b_cards_0_10_min', item_data.get('team_b_cards_0_10_min'))
    
    # ===== PRE-MATCH STATISTICS =====
    loader.add_value('pre_match_teamA_ppg', item_data.get('pre_match_teamA_ppg'))
    loader.add_value('pre_match_teamB_ppg', item_data.get('pre_match_teamB_ppg'))
    loader.add_value('pre_match_home_ppg', item_data.get('pre_match_home_ppg'))
    loader.add_value('pre_match_away_ppg', item_data.get('pre_match_away_ppg'))
    loader.add_value('pre_match_teamA_overall_ppg', item_data.get('pre_match_teamA_overall_ppg'))
    loader.add_value('pre_match_teamB_overall_ppg', item_data.get('pre_match_teamB_overall_ppg'))
    loader.add_value('home_ppg', item_data.get('home_ppg'))
    loader.add_value('away_ppg', item_data.get('away_ppg'))
    
    # ===== MAIN ODDS INFORMATION =====
    loader.add_value('odds_ft_1', item_data.get('odds_ft_1'))
    loader.add_value('odds_ft_x', item_data.get('odds_ft_x'))
    loader.add_value('odds_ft_2', item_data.get('odds_ft_2'))
    
    # ===== OVER/UNDER ODDS =====
    loader.add_value('odds_ft_over05', item_data.get('odds_ft_over05'))
    loader.add_value('odds_ft_under05', item_data.get('odds_ft_under05'))
    loader.add_value('odds_ft_over15', item_data.get('odds_ft_over15'))
    loader.add_value('odds_ft_under15', item_data.get('odds_ft_under15'))
    loader.add_value('odds_ft_over25', item_data.get('odds_ft_over25'))
    loader.add_value('odds_ft_under25', item_data.get('odds_ft_under25'))
    loader.add_value('odds_ft_over35', item_data.get('odds_ft_over35'))
    loader.add_value('odds_ft_under35', item_data.get('odds_ft_under35'))
    loader.add_value('odds_ft_over45', item_data.get('odds_ft_over45'))
    loader.add_value('odds_ft_under45', item_data.get('odds_ft_under45'))
    
    # ===== BTTS AND CLEAN SHEETS =====
    loader.add_value('odds_btts_yes', item_data.get('odds_btts_yes'))
    loader.add_value('odds_btts_no', item_data.get('odds_btts_no'))
    loader.add_value('odds_team_a_cs_yes', item_data.get('odds_team_a_cs_yes'))
    loader.add_value('odds_team_a_cs_no', item_data.get('odds_team_a_cs_no'))
    loader.add_value('odds_team_b_cs_yes', item_data.get('odds_team_b_cs_yes'))
    loader.add_value('odds_team_b_cs_no', item_data.get('odds_team_b_cs_no'))
    
    # ===== DOUBLE CHANCE ODDS =====
    loader.add_value('odds_doublechance_1x', item_data.get('odds_doublechance_1x'))
    loader.add_value('odds_doublechance_12', item_data.get('odds_doublechance_12'))
    loader.add_value('odds_doublechance_x2', item_data.get('odds_doublechance_x2'))
    
    # ===== HALF-TIME RESULT ODDS =====
    loader.add_value('odds_1st_half_result_1', item_data.get('odds_1st_half_result_1'))
    loader.add_value('odds_1st_half_result_x', item_data.get('odds_1st_half_result_x'))
    loader.add_value('odds_1st_half_result_2', item_data.get('odds_1st_half_result_2'))
    loader.add_value('odds_2nd_half_result_1', item_data.get('odds_2nd_half_result_1'))
    loader.add_value('odds_2nd_half_result_x', item_data.get('odds_2nd_half_result_x'))
    loader.add_value('odds_2nd_half_result_2', item_data.get('odds_2nd_half_result_2'))
    
    # ===== DRAW NO BET ODDS =====
    loader.add_value('odds_dnb_1', item_data.get('odds_dnb_1'))
    loader.add_value('odds_dnb_2', item_data.get('odds_dnb_2'))
    
    # ===== CORNERS ODDS =====
    loader.add_value('odds_corners_over_75', item_data.get('odds_corners_over_75'))
    loader.add_value('odds_corners_over_85', item_data.get('odds_corners_over_85'))
    loader.add_value('odds_corners_over_95', item_data.get('odds_corners_over_95'))
    loader.add_value('odds_corners_over_105', item_data.get('odds_corners_over_105'))
    loader.add_value('odds_corners_over_115', item_data.get('odds_corners_over_115'))
    loader.add_value('odds_corners_under_75', item_data.get('odds_corners_under_75'))
    loader.add_value('odds_corners_under_85', item_data.get('odds_corners_under_85'))
    loader.add_value('odds_corners_under_95', item_data.get('odds_corners_under_95'))
    loader.add_value('odds_corners_under_105', item_data.get('odds_corners_under_105'))
    loader.add_value('odds_corners_under_115', item_data.get('odds_corners_under_115'))
    loader.add_value('odds_corners_1', item_data.get('odds_corners_1'))
    loader.add_value('odds_corners_x', item_data.get('odds_corners_x'))
    loader.add_value('odds_corners_2', item_data.get('odds_corners_2'))
    
    # ===== FIRST GOAL AND WIN TO NIL ODDS =====
    loader.add_value('odds_team_to_score_first_1', item_data.get('odds_team_to_score_first_1'))
    loader.add_value('odds_team_to_score_first_x', item_data.get('odds_team_to_score_first_x'))
    loader.add_value('odds_team_to_score_first_2', item_data.get('odds_team_to_score_first_2'))
    loader.add_value('odds_win_to_nil_1', item_data.get('odds_win_to_nil_1'))
    loader.add_value('odds_win_to_nil_2', item_data.get('odds_win_to_nil_2'))
    
    # ===== HALF-TIME OVER/UNDER ODDS =====
    loader.add_value('odds_1st_half_over05', item_data.get('odds_1st_half_over05'))
    loader.add_value('odds_1st_half_over15', item_data.get('odds_1st_half_over15'))
    loader.add_value('odds_1st_half_over25', item_data.get('odds_1st_half_over25'))
    loader.add_value('odds_1st_half_over35', item_data.get('odds_1st_half_over35'))
    loader.add_value('odds_1st_half_under05', item_data.get('odds_1st_half_under05'))
    loader.add_value('odds_1st_half_under15', item_data.get('odds_1st_half_under15'))
    loader.add_value('odds_1st_half_under25', item_data.get('odds_1st_half_under25'))
    loader.add_value('odds_1st_half_under35', item_data.get('odds_1st_half_under35'))
    
    # ===== SECOND HALF OVER/UNDER ODDS =====
    loader.add_value('odds_2nd_half_over05', item_data.get('odds_2nd_half_over05'))
    loader.add_value('odds_2nd_half_over15', item_data.get('odds_2nd_half_over15'))
    loader.add_value('odds_2nd_half_over25', item_data.get('odds_2nd_half_over25'))
    loader.add_value('odds_2nd_half_over35', item_data.get('odds_2nd_half_over35'))
    loader.add_value('odds_2nd_half_under05', item_data.get('odds_2nd_half_under05'))
    loader.add_value('odds_2nd_half_under15', item_data.get('odds_2nd_half_under15'))
    loader.add_value('odds_2nd_half_under25', item_data.get('odds_2nd_half_under25'))
    loader.add_value('odds_2nd_half_under35', item_data.get('odds_2nd_half_under35'))
    
    # ===== HALF-TIME BTTS ODDS =====
    loader.add_value('odds_btts_1st_half_yes', item_data.get('odds_btts_1st_half_yes'))
    loader.add_value('odds_btts_1st_half_no', item_data.get('odds_btts_1st_half_no'))
    loader.add_value('odds_btts_2nd_half_yes', item_data.get('odds_btts_2nd_half_yes'))
    loader.add_value('odds_btts_2nd_half_no', item_data.get('odds_btts_2nd_half_no'))
    
    # ===== MATCH CONTEXT =====
    loader.add_value('referee_id', item_data.get('referee_id'))
    loader.add_value('coach_id_team_a', item_data.get('coach_id_team_a'))
    loader.add_value('coach_id_team_b', item_data.get('coach_id_team_b'))
    loader.add_value('stadium_name', item_data.get('stadium_name'))
    loader.add_value('stadium_location', item_data.get('stadium_location'))
    loader.add_value('attendance', item_data.get('attendance'))
    loader.add_value('winningTeam', item_data.get('winningTeam'))
    loader.add_value('winner_team_id', item_data.get('winner_team_id'))
    loader.add_value('no_home_away', item_data.get('no_home_away'))
    
    # ===== POTENTIAL AND STATISTICS FLAGS =====
    loader.add_value('btts_potential', item_data.get('btts_potential'))
    loader.add_value('btts_fhg_potential', item_data.get('btts_fhg_potential'))
    loader.add_value('btts_2hg_potential', item_data.get('btts_2hg_potential'))
    loader.add_value('o45_potential', item_data.get('o45_potential'))
    loader.add_value('o35_potential', item_data.get('o35_potential'))
    loader.add_value('o25_potential', item_data.get('o25_potential'))
    loader.add_value('o15_potential', item_data.get('o15_potential'))
    loader.add_value('o05_potential', item_data.get('o05_potential'))
    loader.add_value('u45_potential', item_data.get('u45_potential'))
    loader.add_value('u35_potential', item_data.get('u35_potential'))
    loader.add_value('u25_potential', item_data.get('u25_potential'))
    loader.add_value('u15_potential', item_data.get('u15_potential'))
    loader.add_value('u05_potential', item_data.get('u05_potential'))
    loader.add_value('o15HT_potential', item_data.get('o15HT_potential'))
    loader.add_value('o05HT_potential', item_data.get('o05HT_potential'))
    loader.add_value('o05_2H_potential', item_data.get('o05_2H_potential'))
    loader.add_value('o15_2H_potential', item_data.get('o15_2H_potential'))
    loader.add_value('corners_potential', item_data.get('corners_potential'))
    loader.add_value('corners_o85_potential', item_data.get('corners_o85_potential'))
    loader.add_value('corners_o95_potential', item_data.get('corners_o95_potential'))
    loader.add_value('corners_o105_potential', item_data.get('corners_o105_potential'))
    loader.add_value('offsides_potential', item_data.get('offsides_potential'))
    loader.add_value('cards_potential', item_data.get('cards_potential'))
    loader.add_value('avg_potential', item_data.get('avg_potential'))
    
    # ===== RECORDING FLAGS =====
    loader.add_value('goalTimingDisabled', item_data.get('goalTimingDisabled'))
    loader.add_value('corner_timings_recorded', item_data.get('corner_timings_recorded'))
    loader.add_value('card_timings_recorded', item_data.get('card_timings_recorded'))
    loader.add_value('attacks_recorded', item_data.get('attacks_recorded'))
    loader.add_value('pens_recorded', item_data.get('pens_recorded'))
    loader.add_value('goal_timings_recorded', item_data.get('goal_timings_recorded'))
    loader.add_value('throwins_recorded', item_data.get('throwins_recorded'))
    loader.add_value('freekicks_recorded', item_data.get('freekicks_recorded'))
    loader.add_value('goalkicks_recorded', item_data.get('goalkicks_recorded'))
    
    # ===== STATISTICAL FLAGS =====
    loader.add_value('over_05', item_data.get('over_05'))
    loader.add_value('over_15', item_data.get('over_15'))
    loader.add_value('over_25', item_data.get('over_25'))
    loader.add_value('over_35', item_data.get('over_35'))
    loader.add_value('over_45', item_data.get('over_45'))
    loader.add_value('btts', item_data.get('btts'))
    
    # ===== TEAM INFO =====
    loader.add_value('home_url', item_data.get('home_url'))
    loader.add_value('home_image', item_data.get('home_image'))
    loader.add_value('away_url', item_data.get('away_url'))
    loader.add_value('away_image', item_data.get('away_image'))
    
    # ===== METADATA =====
    loader.add_value('extracted_at', datetime.now())
    
    return loader.load_item()