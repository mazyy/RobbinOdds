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

class LeagueTeamItem(Item):
    """Item for individual team from /league-teams endpoint"""
    # Basic team information
    id = Field()                        # Team ID
    name = Field()                      # Team name
    shortName = Field()                 # Short team name
    
    # Season record
    seasonGoalsFor = Field()            # Goals scored this season
    seasonGoalsAgainst = Field()        # Goals conceded this season
    seasonCleanSheets = Field()         # Clean sheets this season
    seasonWins = Field()                # Wins this season
    seasonDraws = Field()               # Draws this season
    seasonLoses = Field()               # Losses this season
    seasonPoints = Field()              # Points this season
    seasonMatchesPlayed = Field()       # Matches played this season
    
    # Form and positioning
    form_overall_position = Field()     # Current league position
    ppg_overall = Field()               # Points per game overall
    ppg_home = Field()                  # Points per game at home
    ppg_away = Field()                  # Points per game away
    
    # Goal statistics
    avg_goals_per_match_overall = Field()           # Average goals per match
    avg_goals_per_match_home = Field()              # Average goals at home
    avg_goals_per_match_away = Field()              # Average goals away
    avg_goals_conceded_per_match_overall = Field()  # Average goals conceded
    avg_goals_conceded_per_match_home = Field()     # Average goals conceded at home
    avg_goals_conceded_per_match_away = Field()     # Average goals conceded away
    
    # Performance percentages
    seasonBTTSPercentage = Field()      # Both teams to score percentage
    seasonCSPercentage = Field()        # Clean sheet percentage
    seasonFTSPercentage = Field()       # Failed to score percentage
    
    # Over/Under statistics
    over_05_percentage = Field()        # Over 0.5 goals percentage
    over_15_percentage = Field()        # Over 1.5 goals percentage
    over_25_percentage = Field()        # Over 2.5 goals percentage
    over_35_percentage = Field()        # Over 3.5 goals percentage
    over_45_percentage = Field()        # Over 4.5 goals percentage
    
    # Card statistics
    seasonCards = Field()               # Total cards this season
    avg_cards_per_match = Field()       # Average cards per match
    
    # Corner statistics
    seasonCorners = Field()             # Total corners this season
    avg_corners_per_match = Field()     # Average corners per match
    
    # Home/Away splits
    home_wins = Field()                 # Home wins
    home_draws = Field()                # Home draws
    home_losses = Field()               # Home losses
    away_wins = Field()                 # Away wins
    away_draws = Field()                # Away draws
    away_losses = Field()               # Away losses
    
    # Recent form (when include=stats)
    last_5_matches_ppg = Field()        # Last 5 matches PPG
    last_10_matches_ppg = Field()       # Last 10 matches PPG
    
    # Advanced statistics (when include=stats)
    xG_overall = Field()                # Expected goals overall
    xGA_overall = Field()               # Expected goals against overall
    shots_per_match = Field()           # Shots per match
    shots_on_target_per_match = Field() # Shots on target per match
    possession_percentage = Field()     # Average possession percentage
    
    # Streak information
    current_win_streak = Field()        # Current winning streak
    current_loss_streak = Field()       # Current losing streak
    current_draw_streak = Field()       # Current drawing streak
    
    # Metadata
    extracted_at = Field()              # When this was extracted

class LeagueTeamLoader(ItemLoader):
    """Item loader for league team data"""
    
    default_item_class = LeagueTeamItem
    default_input_processor = MapCompose(clean_string)
    default_output_processor = TakeFirst()
    
    # Integer fields
    id_in = MapCompose(safe_int)
    seasonGoalsFor_in = MapCompose(safe_int)
    seasonGoalsAgainst_in = MapCompose(safe_int)
    seasonCleanSheets_in = MapCompose(safe_int)
    seasonWins_in = MapCompose(safe_int)
    seasonDraws_in = MapCompose(safe_int)
    seasonLoses_in = MapCompose(safe_int)
    seasonPoints_in = MapCompose(safe_int)
    seasonMatchesPlayed_in = MapCompose(safe_int)
    form_overall_position_in = MapCompose(safe_int)
    seasonCards_in = MapCompose(safe_int)
    seasonCorners_in = MapCompose(safe_int)
    home_wins_in = MapCompose(safe_int)
    home_draws_in = MapCompose(safe_int)
    home_losses_in = MapCompose(safe_int)
    away_wins_in = MapCompose(safe_int)
    away_draws_in = MapCompose(safe_int)
    away_losses_in = MapCompose(safe_int)
    current_win_streak_in = MapCompose(safe_int)
    current_loss_streak_in = MapCompose(safe_int)
    current_draw_streak_in = MapCompose(safe_int)
    
    # Float fields
    ppg_overall_in = MapCompose(safe_float)
    ppg_home_in = MapCompose(safe_float)
    ppg_away_in = MapCompose(safe_float)
    avg_goals_per_match_overall_in = MapCompose(safe_float)
    avg_goals_per_match_home_in = MapCompose(safe_float)
    avg_goals_per_match_away_in = MapCompose(safe_float)
    avg_goals_conceded_per_match_overall_in = MapCompose(safe_float)
    avg_goals_conceded_per_match_home_in = MapCompose(safe_float)
    avg_goals_conceded_per_match_away_in = MapCompose(safe_float)
    seasonBTTSPercentage_in = MapCompose(safe_float)
    seasonCSPercentage_in = MapCompose(safe_float)
    seasonFTSPercentage_in = MapCompose(safe_float)
    over_05_percentage_in = MapCompose(safe_float)
    over_15_percentage_in = MapCompose(safe_float)
    over_25_percentage_in = MapCompose(safe_float)
    over_35_percentage_in = MapCompose(safe_float)
    over_45_percentage_in = MapCompose(safe_float)
    avg_cards_per_match_in = MapCompose(safe_float)
    avg_corners_per_match_in = MapCompose(safe_float)
    last_5_matches_ppg_in = MapCompose(safe_float)
    last_10_matches_ppg_in = MapCompose(safe_float)
    xG_overall_in = MapCompose(safe_float)
    xGA_overall_in = MapCompose(safe_float)
    shots_per_match_in = MapCompose(safe_float)
    shots_on_target_per_match_in = MapCompose(safe_float)
    possession_percentage_in = MapCompose(safe_float)
    
    # Timestamp
    extracted_at_in = MapCompose(lambda x: datetime.now())

def validate_league_team_item(item_data: dict) -> bool:
    """Validate league team data structure before processing"""
    required_fields = ['id', 'name']
    
    if not isinstance(item_data, dict):
        return False
    
    for field in required_fields:
        if field not in item_data or not item_data[field]:
            return False
    
    return True

def create_league_team_item(item_data: dict) -> LeagueTeamItem:
    """Create league team item from API data"""
    loader = LeagueTeamLoader()
    
    # Basic team information
    loader.add_value('id', item_data.get('id'))
    loader.add_value('name', item_data.get('name'))
    loader.add_value('shortName', item_data.get('shortName'))
    
    # Season record
    loader.add_value('seasonGoalsFor', item_data.get('seasonGoalsFor'))
    loader.add_value('seasonGoalsAgainst', item_data.get('seasonGoalsAgainst'))
    loader.add_value('seasonCleanSheets', item_data.get('seasonCleanSheets'))
    loader.add_value('seasonWins', item_data.get('seasonWins'))
    loader.add_value('seasonDraws', item_data.get('seasonDraws'))
    loader.add_value('seasonLoses', item_data.get('seasonLoses'))
    loader.add_value('seasonPoints', item_data.get('seasonPoints'))
    loader.add_value('seasonMatchesPlayed', item_data.get('seasonMatchesPlayed'))
    
    # Form and positioning
    loader.add_value('form_overall_position', item_data.get('form_overall_position'))
    loader.add_value('ppg_overall', item_data.get('ppg_overall'))
    loader.add_value('ppg_home', item_data.get('ppg_home'))
    loader.add_value('ppg_away', item_data.get('ppg_away'))
    
    # Goal statistics
    loader.add_value('avg_goals_per_match_overall', item_data.get('avg_goals_per_match_overall'))
    loader.add_value('avg_goals_per_match_home', item_data.get('avg_goals_per_match_home'))
    loader.add_value('avg_goals_per_match_away', item_data.get('avg_goals_per_match_away'))
    loader.add_value('avg_goals_conceded_per_match_overall', item_data.get('avg_goals_conceded_per_match_overall'))
    loader.add_value('avg_goals_conceded_per_match_home', item_data.get('avg_goals_conceded_per_match_home'))
    loader.add_value('avg_goals_conceded_per_match_away', item_data.get('avg_goals_conceded_per_match_away'))
    
    # Performance percentages
    loader.add_value('seasonBTTSPercentage', item_data.get('seasonBTTSPercentage'))
    loader.add_value('seasonCSPercentage', item_data.get('seasonCSPercentage'))
    loader.add_value('seasonFTSPercentage', item_data.get('seasonFTSPercentage'))
    
    # Over/Under statistics
    loader.add_value('over_05_percentage', item_data.get('over_05_percentage'))
    loader.add_value('over_15_percentage', item_data.get('over_15_percentage'))
    loader.add_value('over_25_percentage', item_data.get('over_25_percentage'))
    loader.add_value('over_35_percentage', item_data.get('over_35_percentage'))
    loader.add_value('over_45_percentage', item_data.get('over_45_percentage'))
    
    # Card statistics
    loader.add_value('seasonCards', item_data.get('seasonCards'))
    loader.add_value('avg_cards_per_match', item_data.get('avg_cards_per_match'))
    
    # Corner statistics
    loader.add_value('seasonCorners', item_data.get('seasonCorners'))
    loader.add_value('avg_corners_per_match', item_data.get('avg_corners_per_match'))
    
    # Home/Away splits
    loader.add_value('home_wins', item_data.get('home_wins'))
    loader.add_value('home_draws', item_data.get('home_draws'))
    loader.add_value('home_losses', item_data.get('home_losses'))
    loader.add_value('away_wins', item_data.get('away_wins'))
    loader.add_value('away_draws', item_data.get('away_draws'))
    loader.add_value('away_losses', item_data.get('away_losses'))
    
    # Recent form (when include=stats)
    loader.add_value('last_5_matches_ppg', item_data.get('last_5_matches_ppg'))
    loader.add_value('last_10_matches_ppg', item_data.get('last_10_matches_ppg'))
    
    # Advanced statistics (when include=stats)
    loader.add_value('xG_overall', item_data.get('xG_overall'))
    loader.add_value('xGA_overall', item_data.get('xGA_overall'))
    loader.add_value('shots_per_match', item_data.get('shots_per_match'))
    loader.add_value('shots_on_target_per_match', item_data.get('shots_on_target_per_match'))
    loader.add_value('possession_percentage', item_data.get('possession_percentage'))
    
    # Streak information
    loader.add_value('current_win_streak', item_data.get('current_win_streak'))
    loader.add_value('current_loss_streak', item_data.get('current_loss_streak'))
    loader.add_value('current_draw_streak', item_data.get('current_draw_streak'))
    
    # Metadata
    loader.add_value('extracted_at', None)
    
    return loader.load_item()