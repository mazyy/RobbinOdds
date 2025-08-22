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

class LeagueStatsItem(Item):
    """Item for league statistics from /league-stats endpoint"""
    # Basic league information
    id = Field()                            # League ID
    name = Field()                          # League name
    english_name = Field()                  # English league name
    country = Field()                       # Country name
    domestic_scale = Field()                # Domestic scale
    international_scale = Field()           # International scale  
    status = Field()                        # League status
    format = Field()                        # League format
    division = Field()                      # Division level
    starting_year = Field()                 # Starting year
    ending_year = Field()                   # Ending year
    women = Field()                         # Women's league flag
    continent = Field()                     # Continent
    comp_master_id = Field()                # Competition master ID
    image = Field()                         # League image URL
    clubNum = Field()                       # Number of clubs
    season = Field()                        # Season string
    totalMatches = Field()                  # Total matches in season
    matchesCompleted = Field()              # Completed matches
    canceledMatchesNum = Field()            # Canceled matches
    game_week = Field()                     # Current game week
    total_game_week = Field()               # Total game weeks
    round = Field()                         # Current round
    progress = Field()                      # Season progress percentage
    
    # Goal statistics
    total_goals = Field()                   # Total goals in season
    home_teams_goals = Field()              # Home team goals
    home_teams_conceded = Field()           # Home team goals conceded
    away_teams_goals = Field()              # Away team goals
    away_teams_conceded = Field()           # Away team goals conceded
    seasonAVG_overall = Field()             # Average goals per match
    seasonAVG_home = Field()                # Average home goals
    seasonAVG_away = Field()                # Average away goals
    
    # BTTS (Both Teams To Score) statistics
    btts_matches = Field()                  # BTTS matches count
    seasonBTTSPercentage = Field()          # BTTS percentage
    seasonCSPercentage = Field()            # Clean sheet percentage
    home_teams_clean_sheets = Field()       # Home clean sheets
    away_teams_clean_sheets = Field()       # Away clean sheets
    home_teams_failed_to_score = Field()   # Home failed to score
    away_teams_failed_to_score = Field()   # Away failed to score
    
    # Corner statistics
    cornersAVG_overall = Field()            # Average corners per match
    cornersAVG_home = Field()               # Average home corners
    cornersAVG_away = Field()               # Average away corners
    cornersTotal_overall = Field()          # Total corners
    cornersTotal_home = Field()             # Total home corners
    cornersTotal_away = Field()             # Total away corners
    
    # Card statistics
    cardsAVG_overall = Field()              # Average cards per match
    cardsAVG_home = Field()                 # Average home cards
    cardsAVG_away = Field()                 # Average away cards
    cardsTotal_overall = Field()            # Total cards
    cardsTotal_home = Field()               # Total home cards
    cardsTotal_away = Field()               # Total away cards
    
    # Risk and advantage statistics
    riskNum = Field()                       # Risk number
    homeAttackAdvantagePercentage = Field() # Home attack advantage
    homeDefenceAdvantagePercentage = Field() # Home defense advantage
    homeOverallAdvantage = Field()          # Home overall advantage
    
    # Additional statistics
    foulsTotal_overall = Field()            # Total fouls
    foulsTotal_home = Field()               # Total home fouls  
    foulsTotal_away = Field()               # Total away fouls
    foulsAVG_overall = Field()              # Average fouls per match
    foulsAVG_home = Field()                 # Average home fouls
    foulsAVG_away = Field()                 # Average away fouls
    
    # Shot statistics
    shotsTotal_overall = Field()            # Total shots
    shotsTotal_home = Field()               # Total home shots
    shotsTotal_away = Field()               # Total away shots
    shotsAVG_overall = Field()              # Average shots per match
    shotsAVG_home = Field()                 # Average home shots
    shotsAVG_away = Field()                 # Average away shots
    
    # Offside statistics
    offsidesTotal_overall = Field()         # Total offsides
    offsidesTotal_home = Field()            # Total home offsides
    offsidesTotal_away = Field()            # Total away offsides
    offsidesAVG_overall = Field()           # Average offsides per match
    offsidesAVG_home = Field()              # Average home offsides
    offsidesAVG_away = Field()              # Average away offsides
    
    # Top scorers, assists, clean sheets arrays
    top_scorers = Field()                   # Top scorers array
    top_assists = Field()                   # Top assists array  
    top_clean_sheets = Field()              # Top clean sheets array

    # Additional metadata
    latest = Field()                        # Latest update flag
    goalTimingDisabled = Field()            # Goal timing disabled flag
    extracted_at = Field()                  # When this was extracted

class LeagueStatsLoader(ItemLoader):
    """Item loader for league stats data"""
    
    default_item_class = LeagueStatsItem
    default_input_processor = MapCompose(clean_string)
    default_output_processor = TakeFirst()
    
    # Integer fields
    id_in = MapCompose(safe_int)
    domestic_scale_in = MapCompose(safe_int)
    international_scale_in = MapCompose(safe_int)
    starting_year_in = MapCompose(safe_int)
    ending_year_in = MapCompose(safe_int)
    women_in = MapCompose(safe_int)
    comp_master_id_in = MapCompose(safe_int)
    clubNum_in = MapCompose(safe_int)
    totalMatches_in = MapCompose(safe_int)
    matchesCompleted_in = MapCompose(safe_int)
    canceledMatchesNum_in = MapCompose(safe_int)
    game_week_in = MapCompose(safe_int)
    total_game_week_in = MapCompose(safe_int)
    round_in = MapCompose(safe_int)
    total_goals_in = MapCompose(safe_int)
    home_teams_goals_in = MapCompose(safe_int)
    home_teams_conceded_in = MapCompose(safe_int)
    away_teams_goals_in = MapCompose(safe_int)
    away_teams_conceded_in = MapCompose(safe_int)
    btts_matches_in = MapCompose(safe_int)
    home_teams_clean_sheets_in = MapCompose(safe_int)
    away_teams_clean_sheets_in = MapCompose(safe_int)
    home_teams_failed_to_score_in = MapCompose(safe_int)
    away_teams_failed_to_score_in = MapCompose(safe_int)
    cornersTotal_overall_in = MapCompose(safe_int)
    cornersTotal_home_in = MapCompose(safe_int)
    cornersTotal_away_in = MapCompose(safe_int)
    cardsTotal_overall_in = MapCompose(safe_int)
    cardsTotal_home_in = MapCompose(safe_int)
    cardsTotal_away_in = MapCompose(safe_int)
    foulsTotal_overall_in = MapCompose(safe_int)
    foulsTotal_home_in = MapCompose(safe_int)
    foulsTotal_away_in = MapCompose(safe_int)
    shotsTotal_overall_in = MapCompose(safe_int)
    shotsTotal_home_in = MapCompose(safe_int)
    shotsTotal_away_in = MapCompose(safe_int)
    offsidesTotal_overall_in = MapCompose(safe_int)
    offsidesTotal_home_in = MapCompose(safe_int)
    offsidesTotal_away_in = MapCompose(safe_int)
    riskNum_in = MapCompose(safe_int)
    
    # Float fields
    progress_in = MapCompose(safe_float)
    seasonAVG_overall_in = MapCompose(safe_float)
    seasonAVG_home_in = MapCompose(safe_float)
    seasonAVG_away_in = MapCompose(safe_float)
    seasonBTTSPercentage_in = MapCompose(safe_float)
    seasonCSPercentage_in = MapCompose(safe_float)
    cornersAVG_overall_in = MapCompose(safe_float)
    cornersAVG_home_in = MapCompose(safe_float)
    cornersAVG_away_in = MapCompose(safe_float)
    cardsAVG_overall_in = MapCompose(safe_float)
    cardsAVG_home_in = MapCompose(safe_float)
    cardsAVG_away_in = MapCompose(safe_float)
    foulsAVG_overall_in = MapCompose(safe_float)
    foulsAVG_home_in = MapCompose(safe_float)
    foulsAVG_away_in = MapCompose(safe_float)
    shotsAVG_overall_in = MapCompose(safe_float)
    shotsAVG_home_in = MapCompose(safe_float)
    shotsAVG_away_in = MapCompose(safe_float)
    offsidesAVG_overall_in = MapCompose(safe_float)
    offsidesAVG_home_in = MapCompose(safe_float)
    offsidesAVG_away_in = MapCompose(safe_float)
    homeAttackAdvantagePercentage_in = MapCompose(safe_float)
    homeDefenceAdvantagePercentage_in = MapCompose(safe_float)
    homeOverallAdvantage_in = MapCompose(safe_float)
    
    # Timestamp
    extracted_at_in = MapCompose(lambda x: datetime.now())

def validate_league_stats_item(item_data: dict) -> bool:
    """Validate league stats data structure before processing"""
    required_fields = ['name', 'season']
    
    if not isinstance(item_data, dict):
        return False
    
    for field in required_fields:
        if field not in item_data or not item_data[field]:
            return False
    
    return True

def create_league_stats_item(item_data: dict) -> LeagueStatsItem:
    """Create league stats item from API data"""
    loader = LeagueStatsLoader()
    
    # Basic information
    loader.add_value('id', item_data.get('id'))
    loader.add_value('name', item_data.get('name'))
    loader.add_value('english_name', item_data.get('english_name'))
    loader.add_value('country', item_data.get('country'))
    loader.add_value('domestic_scale', item_data.get('domestic_scale'))
    loader.add_value('international_scale', item_data.get('international_scale'))
    loader.add_value('status', item_data.get('status'))
    loader.add_value('format', item_data.get('format'))
    loader.add_value('division', item_data.get('division'))
    loader.add_value('starting_year', item_data.get('starting_year'))
    loader.add_value('ending_year', item_data.get('ending_year'))
    loader.add_value('women', item_data.get('women'))
    loader.add_value('continent', item_data.get('continent'))
    loader.add_value('comp_master_id', item_data.get('comp_master_id'))
    loader.add_value('image', item_data.get('image'))
    loader.add_value('clubNum', item_data.get('clubNum'))
    loader.add_value('season', item_data.get('season'))
    loader.add_value('totalMatches', item_data.get('totalMatches'))
    loader.add_value('matchesCompleted', item_data.get('matchesCompleted'))
    loader.add_value('canceledMatchesNum', item_data.get('canceledMatchesNum'))
    loader.add_value('game_week', item_data.get('game_week'))
    loader.add_value('total_game_week', item_data.get('total_game_week'))
    loader.add_value('round', item_data.get('round'))
    loader.add_value('progress', item_data.get('progress'))
    
    # Goal statistics
    loader.add_value('total_goals', item_data.get('total_goals'))
    loader.add_value('home_teams_goals', item_data.get('home_teams_goals'))
    loader.add_value('home_teams_conceded', item_data.get('home_teams_conceded'))
    loader.add_value('away_teams_goals', item_data.get('away_teams_goals'))
    loader.add_value('away_teams_conceded', item_data.get('away_teams_conceded'))
    loader.add_value('seasonAVG_overall', item_data.get('seasonAVG_overall'))
    loader.add_value('seasonAVG_home', item_data.get('seasonAVG_home'))
    loader.add_value('seasonAVG_away', item_data.get('seasonAVG_away'))
    
    # BTTS statistics
    loader.add_value('btts_matches', item_data.get('btts_matches'))
    loader.add_value('seasonBTTSPercentage', item_data.get('seasonBTTSPercentage'))
    loader.add_value('seasonCSPercentage', item_data.get('seasonCSPercentage'))
    loader.add_value('home_teams_clean_sheets', item_data.get('home_teams_clean_sheets'))
    loader.add_value('away_teams_clean_sheets', item_data.get('away_teams_clean_sheets'))
    loader.add_value('home_teams_failed_to_score', item_data.get('home_teams_failed_to_score'))
    loader.add_value('away_teams_failed_to_score', item_data.get('away_teams_failed_to_score'))
    
    # Corner statistics
    loader.add_value('cornersAVG_overall', item_data.get('cornersAVG_overall'))
    loader.add_value('cornersAVG_home', item_data.get('cornersAVG_home'))
    loader.add_value('cornersAVG_away', item_data.get('cornersAVG_away'))
    loader.add_value('cornersTotal_overall', item_data.get('cornersTotal_overall'))
    loader.add_value('cornersTotal_home', item_data.get('cornersTotal_home'))
    loader.add_value('cornersTotal_away', item_data.get('cornersTotal_away'))
    
    # Card statistics
    loader.add_value('cardsAVG_overall', item_data.get('cardsAVG_overall'))
    loader.add_value('cardsAVG_home', item_data.get('cardsAVG_home'))
    loader.add_value('cardsAVG_away', item_data.get('cardsAVG_away'))
    loader.add_value('cardsTotal_overall', item_data.get('cardsTotal_overall'))
    loader.add_value('cardsTotal_home', item_data.get('cardsTotal_home'))
    loader.add_value('cardsTotal_away', item_data.get('cardsTotal_away'))
    
    # Risk and advantage
    loader.add_value('riskNum', item_data.get('riskNum'))
    loader.add_value('homeAttackAdvantagePercentage', item_data.get('homeAttackAdvantagePercentage'))
    loader.add_value('homeDefenceAdvantagePercentage', item_data.get('homeDefenceAdvantagePercentage'))
    loader.add_value('homeOverallAdvantage', item_data.get('homeOverallAdvantage'))
    
    # Additional statistics
    loader.add_value('foulsTotal_overall', item_data.get('foulsTotal_overall'))
    loader.add_value('foulsTotal_home', item_data.get('foulsTotal_home'))
    loader.add_value('foulsTotal_away', item_data.get('foulsTotal_away'))
    loader.add_value('foulsAVG_overall', item_data.get('foulsAVG_overall'))
    loader.add_value('foulsAVG_home', item_data.get('foulsAVG_home'))
    loader.add_value('foulsAVG_away', item_data.get('foulsAVG_away'))
    
    loader.add_value('shotsTotal_overall', item_data.get('shotsTotal_overall'))
    loader.add_value('shotsTotal_home', item_data.get('shotsTotal_home'))
    loader.add_value('shotsTotal_away', item_data.get('shotsTotal_away'))
    loader.add_value('shotsAVG_overall', item_data.get('shotsAVG_overall'))
    loader.add_value('shotsAVG_home', item_data.get('shotsAVG_home'))
    loader.add_value('shotsAVG_away', item_data.get('shotsAVG_away'))
    
    loader.add_value('offsidesTotal_overall', item_data.get('offsidesTotal_overall'))
    loader.add_value('offsidesTotal_home', item_data.get('offsidesTotal_home'))
    loader.add_value('offsidesTotal_away', item_data.get('offsidesTotal_away'))
    loader.add_value('offsidesAVG_overall', item_data.get('offsidesAVG_overall'))
    loader.add_value('offsidesAVG_home', item_data.get('offsidesAVG_home'))
    loader.add_value('offsidesAVG_away', item_data.get('offsidesAVG_away'))
    
    # Top lists (arrays)
    loader.add_value('top_scorers', item_data.get('top_scorers'))
    loader.add_value('top_assists', item_data.get('top_assists'))
    loader.add_value('top_clean_sheets', item_data.get('top_clean_sheets'))
    
    # Metadata
    loader.add_value('latest', item_data.get('latest'))
    loader.add_value('goalTimingDisabled', item_data.get('goalTimingDisabled'))
    loader.add_value('extracted_at', None)
    
    return loader.load_item()