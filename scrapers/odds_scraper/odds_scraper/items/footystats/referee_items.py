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

class RefereeSeasonItem(Item):
    """Individual season statistics for referee"""
    season = Field()                    # Season string (e.g., "2023/2024")
    competition_name = Field()          # Competition name
    league = Field()                    # League name (alternative field name)
    competition_id = Field()            # Competition ID
    country = Field()                   # Country of competition
    appearances = Field()               # Appearances count in this season
    goals_per_match = Field()           # Average goals per match refereed
    cards_per_match = Field()           # Average cards per match
    penalties_per_match = Field()       # Average penalties per match
    btts_percentage = Field()           # BTTS percentage in refereed matches
    over_25_percentage = Field()        # Over 2.5 goals percentage
    wins_home = Field()                 # Home team wins
    wins_away = Field()                 # Away team wins
    draws = Field()                     # Draws
    wins_per_home = Field()             # Home win percentage
    wins_per_away = Field()             # Away win percentage
    draws_per = Field()                 # Draw percentage

class RefereeItem(Item):
    """Item for referee from /referee endpoint"""
    # Basic information
    id = Field()                        # Referee ID
    full_name = Field()                 # Full referee name
    first_name = Field()                # First name
    last_name = Field()                 # Last name
    known_as = Field()                  # Known as name
    shorthand = Field()                 # Shorthand identifier
    age = Field()                       # Current age
    nationality = Field()               # Referee nationality
    birthday = Field()                  # Birthday timestamp
    
    # Career totals across all competitions
    career_appearances = Field()        # Total career appearances
    career_goals_per_match = Field()    # Career average goals per match
    career_cards_per_match = Field()    # Career average cards per match
    career_penalties_per_match = Field() # Career average penalties per match
    career_btts_percentage = Field()    # Career BTTS percentage
    career_over_25_percentage = Field() # Career Over 2.5 percentage
    
    # Career win percentages
    wins_home_percentage = Field()      # Home team win percentage
    wins_away_percentage = Field()      # Away team win percentage
    draws_percentage = Field()          # Draw percentage
    
    # Career totals
    career_home_wins = Field()          # Total home wins refereed
    career_away_wins = Field()          # Total away wins refereed
    career_draws = Field()              # Total draws refereed
    
    # Advanced statistics
    career_goals_total = Field()        # Total goals in refereed matches
    career_penalties_total = Field()    # Total penalties awarded
    career_cards_total = Field()        # Total cards shown
    career_red_cards_total = Field()    # Total red cards shown
    
    # Season breakdown
    seasons = Field()                   # List of RefereeSeasonItem
    total_seasons = Field()             # Total number of seasons
    total_competitions = Field()        # Total number of competitions
    
    # Performance indicators
    consistency_rating = Field()        # Consistency in decisions
    controversy_rating = Field()        # Controversy level
    experience_level = Field()          # Experience level rating
    
    # Recent form
    last_5_matches_goals_avg = Field()  # Goals average in last 5 matches
    last_10_matches_goals_avg = Field() # Goals average in last 10 matches
    
    # Metadata
    last_updated = Field()              # When referee data was last updated
    extracted_at = Field()              # When this was extracted

class RefereeSeasonLoader(ItemLoader):
    """Item loader for referee season data"""
    
    default_item_class = RefereeSeasonItem
    default_input_processor = MapCompose(clean_string)
    default_output_processor = TakeFirst()
    
    # Integer fields
    competition_id_in = MapCompose(safe_int)
    appearances_in = MapCompose(safe_int)
    wins_home_in = MapCompose(safe_int)
    wins_away_in = MapCompose(safe_int)
    draws_in = MapCompose(safe_int)
    
    # Float fields
    goals_per_match_in = MapCompose(safe_float)
    cards_per_match_in = MapCompose(safe_float)
    penalties_per_match_in = MapCompose(safe_float)
    btts_percentage_in = MapCompose(safe_float)
    over_25_percentage_in = MapCompose(safe_float)
    wins_per_home_in = MapCompose(safe_float)
    wins_per_away_in = MapCompose(safe_float)
    draws_per_in = MapCompose(safe_float)

class RefereeLoader(ItemLoader):
    """Item loader for referee data"""
    
    default_item_class = RefereeItem
    default_input_processor = MapCompose(clean_string)
    default_output_processor = TakeFirst()
    
    # Integer fields
    id_in = MapCompose(safe_int)
    age_in = MapCompose(safe_int)
    birthday_in = MapCompose(safe_int)
    career_appearances_in = MapCompose(safe_int)
    career_home_wins_in = MapCompose(safe_int)
    career_away_wins_in = MapCompose(safe_int)
    career_draws_in = MapCompose(safe_int)
    career_goals_total_in = MapCompose(safe_int)
    career_penalties_total_in = MapCompose(safe_int)
    career_cards_total_in = MapCompose(safe_int)
    career_red_cards_total_in = MapCompose(safe_int)
    total_seasons_in = MapCompose(safe_int)
    total_competitions_in = MapCompose(safe_int)
    last_updated_in = MapCompose(safe_int)
    
    # Float fields
    career_goals_per_match_in = MapCompose(safe_float)
    career_cards_per_match_in = MapCompose(safe_float)
    career_penalties_per_match_in = MapCompose(safe_float)
    career_btts_percentage_in = MapCompose(safe_float)
    career_over_25_percentage_in = MapCompose(safe_float)
    wins_home_percentage_in = MapCompose(safe_float)
    wins_away_percentage_in = MapCompose(safe_float)
    draws_percentage_in = MapCompose(safe_float)
    consistency_rating_in = MapCompose(safe_float)
    controversy_rating_in = MapCompose(safe_float)
    experience_level_in = MapCompose(safe_float)
    last_5_matches_goals_avg_in = MapCompose(safe_float)
    last_10_matches_goals_avg_in = MapCompose(safe_float)
    
    # Timestamp
    extracted_at_in = MapCompose(lambda x: datetime.now())
    
    # Keep seasons as list
    seasons_out = Identity()

def create_referee_season(season_data: dict) -> RefereeSeasonItem:
    """Create referee season item from season data"""
    loader = RefereeSeasonLoader()
    
    loader.add_value('season', season_data.get('season'))
    loader.add_value('competition_name', season_data.get('competition_name'))
    loader.add_value('league', season_data.get('league'))
    loader.add_value('competition_id', season_data.get('competition_id'))
    loader.add_value('country', season_data.get('country'))
    loader.add_value('appearances', season_data.get('appearances_overall'))
    loader.add_value('goals_per_match', season_data.get('goals_per_match_overall'))
    loader.add_value('cards_per_match', season_data.get('cards_per_match'))
    loader.add_value('penalties_per_match', season_data.get('penalties_per_match'))
    loader.add_value('btts_percentage', season_data.get('btts_percentage'))
    loader.add_value('over_25_percentage', season_data.get('over_25_percentage'))
    loader.add_value('wins_home', season_data.get('wins_home'))
    loader.add_value('wins_away', season_data.get('wins_away'))
    loader.add_value('draws', season_data.get('draws_overall'))
    loader.add_value('wins_per_home', season_data.get('wins_per_home'))
    loader.add_value('wins_per_away', season_data.get('wins_per_away'))
    loader.add_value('draws_per', season_data.get('draws_per'))
    
    return loader.load_item()

def validate_referee_item(item_data: dict) -> bool:
    """Validate referee data structure before processing"""
    # Handle both single referee object and array of seasons
    if isinstance(item_data, list):
        # If it's an array, check the first item
        if not item_data:
            return False
        first_item = item_data[0]
        required_fields = ['id', 'full_name']
        return all(field in first_item and first_item[field] for field in required_fields)
    elif isinstance(item_data, dict):
        required_fields = ['id', 'full_name']
        return all(field in item_data and item_data[field] for field in required_fields)
    
    return False

def create_referee_item(item_data: dict) -> RefereeItem:
    """Create referee item from API data"""
    loader = RefereeLoader()
    
    # Handle case where response is an array of seasons
    if isinstance(item_data, list):
        if not item_data:
            raise ValueError("Empty referee data array")
        
        # Use first item for basic info, process all for seasons
        first_item = item_data[0]
        seasons_data = item_data
    else:
        # Single item, extract seasons if present
        first_item = item_data
        seasons_data = item_data.get('seasons', [first_item])
    
    # Basic information from first item
    loader.add_value('id', first_item.get('id'))
    loader.add_value('full_name', first_item.get('full_name'))
    loader.add_value('first_name', first_item.get('first_name'))
    loader.add_value('last_name', first_item.get('last_name'))
    loader.add_value('known_as', first_item.get('known_as'))
    loader.add_value('shorthand', first_item.get('shorthand'))
    loader.add_value('age', first_item.get('age'))
    loader.add_value('nationality', first_item.get('nationality'))
    loader.add_value('birthday', first_item.get('birthday'))
    
    # Career totals (use first item or aggregate if needed)
    loader.add_value('career_appearances', first_item.get('appearances_overall'))
    loader.add_value('career_goals_per_match', first_item.get('goals_per_match_overall'))
    loader.add_value('career_cards_per_match', first_item.get('cards_per_match'))
    loader.add_value('career_penalties_per_match', first_item.get('penalties_per_match'))
    loader.add_value('career_btts_percentage', first_item.get('btts_percentage'))
    loader.add_value('career_over_25_percentage', first_item.get('over_25_percentage'))
    
    # Win percentages
    loader.add_value('wins_home_percentage', first_item.get('wins_per_home'))
    loader.add_value('wins_away_percentage', first_item.get('wins_per_away'))
    loader.add_value('draws_percentage', first_item.get('draws_per'))
    
    # Career totals
    loader.add_value('career_home_wins', first_item.get('wins_home'))
    loader.add_value('career_away_wins', first_item.get('wins_away'))
    loader.add_value('career_draws', first_item.get('draws_overall'))
    
    # Advanced statistics
    loader.add_value('career_goals_total', first_item.get('goals_overall'))
    loader.add_value('career_penalties_total', first_item.get('penalties_given_overall'))
    loader.add_value('career_cards_total', first_item.get('cards_overall'))
    loader.add_value('career_red_cards_total', first_item.get('red_cards_overall'))
    
    # Process seasons
    if isinstance(seasons_data, list):
        seasons = [create_referee_season(season) for season in seasons_data if isinstance(season, dict)]
        loader.add_value('seasons', seasons)
        loader.add_value('total_seasons', len(seasons))
        
        # Count unique competitions
        competitions = set()
        for season in seasons_data:
            if isinstance(season, dict) and season.get('league'):
                competitions.add(season['league'])
        loader.add_value('total_competitions', len(competitions))
    else:
        loader.add_value('seasons', [])
        loader.add_value('total_seasons', 0)
        loader.add_value('total_competitions', 0)
    
    # Performance indicators (can be calculated or provided)
    loader.add_value('consistency_rating', first_item.get('consistency_rating'))
    loader.add_value('controversy_rating', first_item.get('controversy_rating'))
    loader.add_value('experience_level', first_item.get('experience_level'))
    
    # Recent form
    loader.add_value('last_5_matches_goals_avg', first_item.get('last_5_matches_goals_avg'))
    loader.add_value('last_10_matches_goals_avg', first_item.get('last_10_matches_goals_avg'))
    
    # Metadata
    loader.add_value('last_updated', first_item.get('last_updated'))
    loader.add_value('extracted_at', None)
    
    return loader.load_item()