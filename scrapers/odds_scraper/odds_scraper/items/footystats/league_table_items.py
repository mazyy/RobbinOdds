from scrapy import Item, Field
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst, Identity
from datetime import datetime
from . import FootyStatsBaseItem, FootyStatsBaseItemLoader, safe_int, safe_float, clean_string

class LeagueTableItem(FootyStatsBaseItem):
    """
    Item for FootyStats /league-table endpoint
    
    League standings with position, points, goal difference and team statistics.
    Captures comprehensive table position data for league analysis.
    """
    
    # Basic team information
    id = Field()                          # Team ID
    name = Field()                        # Team name
    cleanName = Field()                   # Clean team name for matching
    shortName = Field()                   # Short team name
    image = Field()                       # Team logo URL
    
    # League position data
    position = Field()                    # League position
    played = Field()                      # Games played
    wins = Field()                        # Wins
    draws = Field()                       # Draws
    losses = Field()                      # Losses
    goals_for = Field()                   # Goals scored
    goals_against = Field()               # Goals conceded
    goal_difference = Field()             # Goal difference
    points = Field()                      # Total points
    
    # Form and performance
    form = Field()                        # Recent form (W-D-L string)
    home_wins = Field()                   # Home wins
    home_draws = Field()                  # Home draws
    home_losses = Field()                 # Home losses
    away_wins = Field()                   # Away wins
    away_draws = Field()                  # Away draws
    away_losses = Field()                 # Away losses
    
    # Goal statistics by venue
    home_goals_for = Field()              # Goals scored at home
    home_goals_against = Field()          # Goals conceded at home
    away_goals_for = Field()              # Goals scored away
    away_goals_against = Field()          # Goals conceded away
    
    # Additional metrics
    points_per_game = Field()             # Points per game average
    goal_average = Field()                # Goal average per game
    clean_sheets = Field()                # Clean sheets count
    failed_to_score = Field()             # Failed to score count
    
    # Extended metrics often in API
    home_played = Field()                 # Home games played
    away_played = Field()                 # Away games played
    home_goal_difference = Field()        # Home goal difference
    away_goal_difference = Field()        # Away goal difference
    home_points = Field()                 # Home points total
    away_points = Field()                 # Away points total
    home_points_per_game = Field()        # Home PPG
    away_points_per_game = Field()        # Away PPG
    
    # Attacking/defensive stats
    goals_per_game_overall = Field()      # Goals per game overall
    goals_conceded_per_game = Field()     # Goals conceded per game
    goal_difference_per_game = Field()    # Goal difference per game
    
    # Performance indicators
    current_form = Field()                # Current form string
    last_5_results = Field()              # Last 5 results
    last_10_results = Field()             # Last 10 results
    win_percentage = Field()              # Win percentage
    home_win_percentage = Field()         # Home win percentage
    away_win_percentage = Field()         # Away win percentage
    
    # Additional API fields
    country = Field()                     # Country name
    shortHand = Field()                   # Short hand name
    url = Field()                         # Team URL
    seasonURL_overall = Field()           # Season URL overall
    seasonURL_home = Field()              # Season URL home
    seasonURL_away = Field()              # Season URL away
    zone = Field()                        # Zone information (dict with name, number)
    corrections = Field()                 # Corrections field
    
    # Season context
    season_id = Field()                   # Season identifier
    league_name = Field()                 # League name
    competition_id = Field()              # Competition identifier
    
    # Metadata
    extracted_at = Field()                # Extraction timestamp

class LeagueTableLoader(FootyStatsBaseItemLoader):
    """Item loader for league table data"""
    
    default_item_class = LeagueTableItem
    default_input_processor = MapCompose(clean_string)
    default_output_processor = TakeFirst()
    
    # Integer fields
    id_in = MapCompose(safe_int)
    position_in = MapCompose(safe_int)
    played_in = MapCompose(safe_int)
    wins_in = MapCompose(safe_int)
    draws_in = MapCompose(safe_int)
    losses_in = MapCompose(safe_int)
    goals_for_in = MapCompose(safe_int)
    goals_against_in = MapCompose(safe_int)
    goal_difference_in = MapCompose(safe_int)
    points_in = MapCompose(safe_int)
    home_wins_in = MapCompose(safe_int)
    home_draws_in = MapCompose(safe_int)
    home_losses_in = MapCompose(safe_int)
    away_wins_in = MapCompose(safe_int)
    away_draws_in = MapCompose(safe_int)
    away_losses_in = MapCompose(safe_int)
    home_goals_for_in = MapCompose(safe_int)
    home_goals_against_in = MapCompose(safe_int)
    away_goals_for_in = MapCompose(safe_int)
    away_goals_against_in = MapCompose(safe_int)
    clean_sheets_in = MapCompose(safe_int)
    failed_to_score_in = MapCompose(safe_int)
    season_id_in = MapCompose(safe_int)
    competition_id_in = MapCompose(safe_int)
    
    # Extended metrics
    home_played_in = MapCompose(safe_int)
    away_played_in = MapCompose(safe_int)
    home_goal_difference_in = MapCompose(safe_int)
    away_goal_difference_in = MapCompose(safe_int)
    home_points_in = MapCompose(safe_int)
    away_points_in = MapCompose(safe_int)
    
    # Float fields
    points_per_game_in = MapCompose(safe_float)
    goal_average_in = MapCompose(safe_float)
    home_points_per_game_in = MapCompose(safe_float)
    away_points_per_game_in = MapCompose(safe_float)
    goals_per_game_overall_in = MapCompose(safe_float)
    goals_conceded_per_game_in = MapCompose(safe_float)
    goal_difference_per_game_in = MapCompose(safe_float)
    win_percentage_in = MapCompose(safe_float)
    home_win_percentage_in = MapCompose(safe_float)
    away_win_percentage_in = MapCompose(safe_float)
    
    # Timestamp field
    extracted_at_in = MapCompose(lambda x: datetime.now())

def validate_league_table_item(item_data: dict) -> bool:
    """Validate league table data structure before processing"""
    required_fields = ['id', 'name', 'position']
    
    if not isinstance(item_data, dict):
        return False
    
    for field in required_fields:
        if field not in item_data or item_data[field] is None:
            return False
    
    # Validate position is numeric and positive
    try:
        position = int(item_data['position'])
        if position <= 0:
            return False
    except (ValueError, TypeError):
        return False
    
    return True

def create_league_table_item(item_data: dict) -> LeagueTableItem:
    """Create league table item from API data"""
    loader = LeagueTableLoader()
    
    # Basic team information
    loader.add_value('id', item_data.get('id'))
    loader.add_value('name', item_data.get('name'))
    loader.add_value('cleanName', item_data.get('cleanName'))
    loader.add_value('shortName', item_data.get('shortName'))
    loader.add_value('image', item_data.get('image'))
    loader.add_value('country', item_data.get('country'))
    loader.add_value('shortHand', item_data.get('shortHand'))
    loader.add_value('url', item_data.get('url'))
    loader.add_value('seasonURL_overall', item_data.get('seasonURL_overall'))
    loader.add_value('seasonURL_home', item_data.get('seasonURL_home'))
    loader.add_value('seasonURL_away', item_data.get('seasonURL_away'))
    loader.add_value('zone', item_data.get('zone'))
    loader.add_value('corrections', item_data.get('corrections'))
    
    # League position data (map API field names)
    loader.add_value('position', item_data.get('position'))
    loader.add_value('played', item_data.get('matchesPlayed'))
    loader.add_value('wins', item_data.get('seasonWins_overall'))
    loader.add_value('draws', item_data.get('seasonDraws_overall'))
    loader.add_value('losses', item_data.get('seasonLosses_overall'))
    loader.add_value('goals_for', item_data.get('seasonGoals'))
    loader.add_value('goals_against', item_data.get('seasonConceded'))
    loader.add_value('goal_difference', item_data.get('seasonGoalDifference'))
    loader.add_value('points', item_data.get('points'))
    
    # Form and performance (map API field names)
    loader.add_value('form', item_data.get('form'))  # This might not exist in API
    loader.add_value('home_wins', item_data.get('seasonWins_home'))
    loader.add_value('home_draws', item_data.get('seasonDraws_home'))
    loader.add_value('home_losses', item_data.get('seasonLosses_home'))
    loader.add_value('away_wins', item_data.get('seasonWins_away'))
    loader.add_value('away_draws', item_data.get('seasonDraws_away'))
    loader.add_value('away_losses', item_data.get('seasonLosses_away'))
    
    # Goal statistics by venue (map API field names)
    loader.add_value('home_goals_for', item_data.get('seasonGoals_home'))
    loader.add_value('home_goals_against', item_data.get('seasonConceded_home'))
    loader.add_value('away_goals_for', item_data.get('seasonGoals_away'))
    loader.add_value('away_goals_against', item_data.get('seasonConceded_away'))
    
    # Additional metrics (map API field names)
    loader.add_value('points_per_game', item_data.get('ppg_overall'))
    loader.add_value('goal_average', item_data.get('goal_average'))  # This might not exist in API
    loader.add_value('clean_sheets', item_data.get('clean_sheets'))  # This might not exist in API
    loader.add_value('failed_to_score', item_data.get('failed_to_score'))  # This might not exist in API
    
    # Extended metrics
    loader.add_value('home_played', item_data.get('matchesPlayed_home'))
    loader.add_value('away_played', item_data.get('matchesPlayed_away'))
    loader.add_value('home_goal_difference', item_data.get('seasonGoalDifference_home'))
    loader.add_value('away_goal_difference', item_data.get('seasonGoalDifference_away'))
    loader.add_value('home_points', item_data.get('points_home'))
    loader.add_value('away_points', item_data.get('points_away'))
    loader.add_value('home_points_per_game', item_data.get('ppg_home'))
    loader.add_value('away_points_per_game', item_data.get('ppg_away'))
    
    # Performance indicators
    loader.add_value('goals_per_game_overall', item_data.get('goals_per_game_overall'))
    loader.add_value('goals_conceded_per_game', item_data.get('goals_conceded_per_game'))
    loader.add_value('goal_difference_per_game', item_data.get('goal_difference_per_game'))
    loader.add_value('current_form', item_data.get('current_form'))
    loader.add_value('last_5_results', item_data.get('last_5_results'))
    loader.add_value('last_10_results', item_data.get('last_10_results'))
    loader.add_value('win_percentage', item_data.get('win_percentage'))
    loader.add_value('home_win_percentage', item_data.get('home_win_percentage'))
    loader.add_value('away_win_percentage', item_data.get('away_win_percentage'))
    
    # Season context
    loader.add_value('season_id', item_data.get('season_id'))
    loader.add_value('league_name', item_data.get('league_name'))
    loader.add_value('competition_id', item_data.get('competition_id'))
    
    # Metadata
    loader.add_value('extracted_at', None)
    
    return loader.load_item()