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

class MatchDetailsItem(Item):
    """Item for match details from /match endpoint"""
    # Match information (from match object)
    id = Field()                        # Match ID
    home_name = Field()                 # Home team name
    away_name = Field()                 # Away team name
    homeID = Field()                    # Home team ID
    awayID = Field()                    # Away team ID
    homeGoalCount = Field()             # Home team goals
    awayGoalCount = Field()             # Away team goals
    totalGoalCount = Field()            # Total goals in match
    status = Field()                    # Match status
    date_unix = Field()                 # Match timestamp as datetime
    season = Field()                    # Season string
    competition_name = Field()          # Competition/league name
    
    # Match statistics
    team_a_corners = Field()            # Home team corners
    team_b_corners = Field()            # Away team corners
    team_a_yellow_cards = Field()       # Home team yellow cards
    team_b_yellow_cards = Field()       # Away team yellow cards
    team_a_red_cards = Field()          # Home team red cards
    team_b_red_cards = Field()          # Away team red cards
    team_a_shots_on_target = Field()    # Home shots on target
    team_b_shots_on_target = Field()    # Away shots on target
    team_a_possession = Field()         # Home possession percentage
    team_b_possession = Field()         # Away possession percentage
    
    # Head-to-head data (from h2h object)
    h2h_matches_count = Field()         # Total H2H matches between teams
    h2h_home_wins = Field()             # Home team H2H wins
    h2h_away_wins = Field()             # Away team H2H wins
    h2h_draws = Field()                 # H2H draws
    h2h_avg_goals = Field()             # H2H average goals per match
    h2h_btts_percentage = Field()       # H2H BTTS percentage
    h2h_over_25_percentage = Field()    # H2H Over 2.5 goals percentage
    
    # Odds data (from odds object)
    odds_count = Field()                # Number of bookmakers with odds
    best_home_odds = Field()            # Best available home win odds
    best_draw_odds = Field()            # Best available draw odds
    best_away_odds = Field()            # Best available away win odds
    avg_home_odds = Field()             # Average home win odds
    avg_draw_odds = Field()             # Average draw odds
    avg_away_odds = Field()             # Average away win odds
    best_over_25_odds = Field()         # Best Over 2.5 odds
    best_under_25_odds = Field()        # Best Under 2.5 odds
    best_btts_yes_odds = Field()        # Best BTTS Yes odds
    best_btts_no_odds = Field()         # Best BTTS No odds
    
    # Pre-match team statistics
    pre_match_home_ppg = Field()        # Home team pre-match PPG
    pre_match_away_ppg = Field()        # Away team pre-match PPG
    pre_match_home_form = Field()       # Home team form rating
    pre_match_away_form = Field()       # Away team form rating
    pre_match_home_avg_goals = Field()  # Home team average goals
    pre_match_away_avg_goals = Field()  # Away team average goals
    pre_match_home_avg_conceded = Field() # Home team average goals conceded
    pre_match_away_avg_conceded = Field() # Away team average goals conceded
    pre_match_home_position = Field()   # Home team league position
    pre_match_away_position = Field()   # Away team league position
    
    # Match context
    referee_id = Field()                # Referee ID
    stadium_name = Field()              # Stadium name
    stadium_location = Field()          # Stadium location
    
    # Metadata
    extracted_at = Field()              # When this was extracted

class MatchDetailsLoader(ItemLoader):
    """Item loader for match details data"""
    
    default_item_class = MatchDetailsItem
    default_input_processor = MapCompose(clean_string)
    default_output_processor = TakeFirst()
    
    # Integer fields
    id_in = MapCompose(safe_int)
    homeID_in = MapCompose(safe_int)
    awayID_in = MapCompose(safe_int)
    homeGoalCount_in = MapCompose(safe_int)
    awayGoalCount_in = MapCompose(safe_int)
    totalGoalCount_in = MapCompose(safe_int)
    team_a_corners_in = MapCompose(safe_int)
    team_b_corners_in = MapCompose(safe_int)
    team_a_yellow_cards_in = MapCompose(safe_int)
    team_b_yellow_cards_in = MapCompose(safe_int)
    team_a_red_cards_in = MapCompose(safe_int)
    team_b_red_cards_in = MapCompose(safe_int)
    team_a_shots_on_target_in = MapCompose(safe_int)
    team_b_shots_on_target_in = MapCompose(safe_int)
    h2h_matches_count_in = MapCompose(safe_int)
    h2h_home_wins_in = MapCompose(safe_int)
    h2h_away_wins_in = MapCompose(safe_int)
    h2h_draws_in = MapCompose(safe_int)
    odds_count_in = MapCompose(safe_int)
    pre_match_home_position_in = MapCompose(safe_int)
    pre_match_away_position_in = MapCompose(safe_int)
    referee_id_in = MapCompose(safe_int)
    
    # Float fields
    team_a_possession_in = MapCompose(safe_float)
    team_b_possession_in = MapCompose(safe_float)
    h2h_avg_goals_in = MapCompose(safe_float)
    h2h_btts_percentage_in = MapCompose(safe_float)
    h2h_over_25_percentage_in = MapCompose(safe_float)
    best_home_odds_in = MapCompose(safe_float)
    best_draw_odds_in = MapCompose(safe_float)
    best_away_odds_in = MapCompose(safe_float)
    avg_home_odds_in = MapCompose(safe_float)
    avg_draw_odds_in = MapCompose(safe_float)
    avg_away_odds_in = MapCompose(safe_float)
    best_over_25_odds_in = MapCompose(safe_float)
    best_under_25_odds_in = MapCompose(safe_float)
    best_btts_yes_odds_in = MapCompose(safe_float)
    best_btts_no_odds_in = MapCompose(safe_float)
    pre_match_home_ppg_in = MapCompose(safe_float)
    pre_match_away_ppg_in = MapCompose(safe_float)
    pre_match_home_form_in = MapCompose(safe_float)
    pre_match_away_form_in = MapCompose(safe_float)
    pre_match_home_avg_goals_in = MapCompose(safe_float)
    pre_match_away_avg_goals_in = MapCompose(safe_float)
    pre_match_home_avg_conceded_in = MapCompose(safe_float)
    pre_match_away_avg_conceded_in = MapCompose(safe_float)
    
    # Timestamp
    date_unix_in = MapCompose(convert_unix_timestamp)
    extracted_at_in = MapCompose(lambda x: datetime.now())

def validate_match_details_item(item_data: dict) -> bool:
    """Validate match details data structure before processing"""
    if not isinstance(item_data, dict):
        return False
    
    # Check if we have at least match data
    match_data = item_data.get('match', {})
    if not isinstance(match_data, dict) or not match_data.get('id'):
        return False
    
    return True

def create_match_details_item(item_data: dict) -> MatchDetailsItem:
    """Create match details item from API data"""
    loader = MatchDetailsLoader()
    
    # Extract from match object
    match_data = item_data.get('match', {})
    loader.add_value('id', match_data.get('id'))
    loader.add_value('home_name', match_data.get('home_name'))
    loader.add_value('away_name', match_data.get('away_name'))
    loader.add_value('homeID', match_data.get('homeID'))
    loader.add_value('awayID', match_data.get('awayID'))
    loader.add_value('homeGoalCount', match_data.get('homeGoalCount'))
    loader.add_value('awayGoalCount', match_data.get('awayGoalCount'))
    loader.add_value('totalGoalCount', match_data.get('totalGoalCount'))
    loader.add_value('status', match_data.get('status'))
    loader.add_value('date_unix', match_data.get('date_unix'))
    loader.add_value('season', match_data.get('season'))
    loader.add_value('competition_name', match_data.get('competition_name'))
    
    # Match statistics
    loader.add_value('team_a_corners', match_data.get('team_a_corners'))
    loader.add_value('team_b_corners', match_data.get('team_b_corners'))
    loader.add_value('team_a_yellow_cards', match_data.get('team_a_yellow_cards'))
    loader.add_value('team_b_yellow_cards', match_data.get('team_b_yellow_cards'))
    loader.add_value('team_a_red_cards', match_data.get('team_a_red_cards'))
    loader.add_value('team_b_red_cards', match_data.get('team_b_red_cards'))
    loader.add_value('team_a_shots_on_target', match_data.get('team_a_shots_on_target'))
    loader.add_value('team_b_shots_on_target', match_data.get('team_b_shots_on_target'))
    loader.add_value('team_a_possession', match_data.get('team_a_possession'))
    loader.add_value('team_b_possession', match_data.get('team_b_possession'))
    
    # Extract from h2h object
    h2h_data = item_data.get('h2h', {})
    loader.add_value('h2h_matches_count', h2h_data.get('matches_count'))
    loader.add_value('h2h_home_wins', h2h_data.get('home_wins'))
    loader.add_value('h2h_away_wins', h2h_data.get('away_wins'))
    loader.add_value('h2h_draws', h2h_data.get('draws'))
    loader.add_value('h2h_avg_goals', h2h_data.get('avg_goals'))
    loader.add_value('h2h_btts_percentage', h2h_data.get('btts_percentage'))
    loader.add_value('h2h_over_25_percentage', h2h_data.get('over_25_percentage'))
    
    # Extract from odds object
    odds_data = item_data.get('odds', {})
    bookmakers = odds_data.get('bookmakers', [])
    loader.add_value('odds_count', len(bookmakers))
    loader.add_value('best_home_odds', odds_data.get('best_home_odds'))
    loader.add_value('best_draw_odds', odds_data.get('best_draw_odds'))
    loader.add_value('best_away_odds', odds_data.get('best_away_odds'))
    loader.add_value('avg_home_odds', odds_data.get('avg_home_odds'))
    loader.add_value('avg_draw_odds', odds_data.get('avg_draw_odds'))
    loader.add_value('avg_away_odds', odds_data.get('avg_away_odds'))
    loader.add_value('best_over_25_odds', odds_data.get('best_over_25_odds'))
    loader.add_value('best_under_25_odds', odds_data.get('best_under_25_odds'))
    loader.add_value('best_btts_yes_odds', odds_data.get('best_btts_yes_odds'))
    loader.add_value('best_btts_no_odds', odds_data.get('best_btts_no_odds'))
    
    # Pre-match team statistics
    loader.add_value('pre_match_home_ppg', match_data.get('pre_match_teamA_ppg'))
    loader.add_value('pre_match_away_ppg', match_data.get('pre_match_teamB_ppg'))
    loader.add_value('pre_match_home_form', match_data.get('pre_match_teamA_form'))
    loader.add_value('pre_match_away_form', match_data.get('pre_match_teamB_form'))
    loader.add_value('pre_match_home_avg_goals', match_data.get('pre_match_teamA_avg_goals'))
    loader.add_value('pre_match_away_avg_goals', match_data.get('pre_match_teamB_avg_goals'))
    loader.add_value('pre_match_home_avg_conceded', match_data.get('pre_match_teamA_avg_conceded'))
    loader.add_value('pre_match_away_avg_conceded', match_data.get('pre_match_teamB_avg_conceded'))
    loader.add_value('pre_match_home_position', match_data.get('pre_match_teamA_position'))
    loader.add_value('pre_match_away_position', match_data.get('pre_match_teamB_position'))
    
    # Match context
    loader.add_value('referee_id', match_data.get('referee_id'))
    loader.add_value('stadium_name', match_data.get('stadium_name'))
    loader.add_value('stadium_location', match_data.get('stadium_location'))
    
    # Metadata
    loader.add_value('extracted_at', None)
    
    return loader.load_item()