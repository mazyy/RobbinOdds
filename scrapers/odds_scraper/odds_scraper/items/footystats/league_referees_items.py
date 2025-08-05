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

def convert_unix_timestamp(timestamp):
    """Convert UNIX timestamp to datetime object"""
    try:
        if isinstance(timestamp, (int, float)):
            return datetime.fromtimestamp(timestamp)
        return None
    except (ValueError, TypeError):
        return None

class LeagueRefereeItem(Item):
    """Item for individual referee from /league-referees endpoint"""
    # Basic referee information
    id = Field()                            # Referee ID
    full_name = Field()                     # Full referee name
    first_name = Field()                    # First name
    last_name = Field()                     # Last name
    known_as = Field()                      # Known as name
    shorthand = Field()                     # Shorthand identifier
    age = Field()                           # Referee age
    nationality = Field()                   # Referee nationality
    birthday = Field()                      # Birthday timestamp
    
    # League-specific statistics
    league = Field()                        # League name
    season = Field()                        # Season string
    competition_id = Field()                # Competition ID
    starting_year = Field()                 # Season starting year
    ending_year = Field()                   # Season ending year
    
    # Appearance statistics in this league
    appearances_overall = Field()           # Total appearances in league
    appearances_home = Field()              # Home match appearances
    appearances_away = Field()              # Away match appearances
    
    # Match outcome statistics
    wins_home = Field()                     # Home team wins
    wins_away = Field()                     # Away team wins
    draws_overall = Field()                 # Total draws
    wins_per_home = Field()                 # Home win percentage
    wins_per_away = Field()                 # Away win percentage
    draws_per = Field()                     # Draw percentage
    
    # Goal statistics
    goals_overall = Field()                 # Total goals in refereed matches
    goals_home = Field()                    # Goals by home teams
    goals_away = Field()                    # Goals by away teams
    goals_per_match_overall = Field()       # Average goals per match
    goals_per_match_home = Field()          # Average goals by home team
    goals_per_match_away = Field()          # Average goals by away team
    
    # BTTS (Both Teams To Score) statistics
    btts_overall = Field()                  # Total BTTS matches
    btts_percentage = Field()               # BTTS percentage
    
    # Penalty statistics
    penalties_given_overall = Field()       # Total penalties awarded
    penalties_given_home = Field()          # Penalties for home team
    penalties_given_away = Field()          # Penalties for away team
    penalties_given_per_match_overall = Field()    # Penalties per match
    penalties_given_per_match_home = Field()       # Home penalties per match
    penalties_given_per_match_away = Field()       # Away penalties per match
    
    # Card statistics
    cards_overall = Field()                 # Total cards shown
    cards_home = Field()                    # Cards to home team
    cards_away = Field()                    # Cards to away team
    cards_per_match_overall = Field()       # Cards per match
    cards_per_match_home = Field()          # Home cards per match
    cards_per_match_away = Field()          # Away cards per match
    
    # Red card statistics
    red_cards_overall = Field()             # Total red cards
    red_cards_home = Field()                # Red cards to home team
    red_cards_away = Field()                # Red cards to away team
    red_cards_per_match_overall = Field()   # Red cards per match
    red_cards_per_match_home = Field()      # Home red cards per match
    red_cards_per_match_away = Field()      # Away red cards per match
    
    # Over/Under statistics
    over_05_percentage = Field()            # Over 0.5 goals percentage
    over_15_percentage = Field()            # Over 1.5 goals percentage
    over_25_percentage = Field()            # Over 2.5 goals percentage
    over_35_percentage = Field()            # Over 3.5 goals percentage
    
    # Additional context
    continent = Field()                     # Continent of the league
    league_type = Field()                   # Type of league (domestic/international)
    url = Field()                          # URL to referee profile
    
    # Metadata
    extracted_at = Field()                  # When this was extracted

class LeagueRefereeLoader(ItemLoader):
    """Item loader for league referee data"""
    
    default_item_class = LeagueRefereeItem
    default_input_processor = MapCompose(clean_string)
    default_output_processor = TakeFirst()
    
    # Integer fields
    id_in = MapCompose(safe_int)
    age_in = MapCompose(safe_int)
    birthday_in = MapCompose(safe_int)
    competition_id_in = MapCompose(safe_int)
    starting_year_in = MapCompose(safe_int)
    ending_year_in = MapCompose(safe_int)
    appearances_overall_in = MapCompose(safe_int)
    appearances_home_in = MapCompose(safe_int)
    appearances_away_in = MapCompose(safe_int)
    wins_home_in = MapCompose(safe_int)
    wins_away_in = MapCompose(safe_int)
    draws_overall_in = MapCompose(safe_int)
    goals_overall_in = MapCompose(safe_int)
    goals_home_in = MapCompose(safe_int)
    goals_away_in = MapCompose(safe_int)
    btts_overall_in = MapCompose(safe_int)
    penalties_given_overall_in = MapCompose(safe_int)
    penalties_given_home_in = MapCompose(safe_int)
    penalties_given_away_in = MapCompose(safe_int)
    cards_overall_in = MapCompose(safe_int)
    cards_home_in = MapCompose(safe_int)
    cards_away_in = MapCompose(safe_int)
    red_cards_overall_in = MapCompose(safe_int)
    red_cards_home_in = MapCompose(safe_int)
    red_cards_away_in = MapCompose(safe_int)
    
    # Float fields
    wins_per_home_in = MapCompose(safe_float)
    wins_per_away_in = MapCompose(safe_float)
    draws_per_in = MapCompose(safe_float)
    goals_per_match_overall_in = MapCompose(safe_float)
    goals_per_match_home_in = MapCompose(safe_float)
    goals_per_match_away_in = MapCompose(safe_float)
    btts_percentage_in = MapCompose(safe_float)
    penalties_given_per_match_overall_in = MapCompose(safe_float)
    penalties_given_per_match_home_in = MapCompose(safe_float)
    penalties_given_per_match_away_in = MapCompose(safe_float)
    cards_per_match_overall_in = MapCompose(safe_float)
    cards_per_match_home_in = MapCompose(safe_float)
    cards_per_match_away_in = MapCompose(safe_float)
    red_cards_per_match_overall_in = MapCompose(safe_float)
    red_cards_per_match_home_in = MapCompose(safe_float)
    red_cards_per_match_away_in = MapCompose(safe_float)
    over_05_percentage_in = MapCompose(safe_float)
    over_15_percentage_in = MapCompose(safe_float)
    over_25_percentage_in = MapCompose(safe_float)
    over_35_percentage_in = MapCompose(safe_float)
    
    # Timestamp
    extracted_at_in = MapCompose(lambda x: datetime.now())

def validate_league_referee_item(item_data: dict) -> bool:
    """Validate league referee data structure before processing"""
    required_fields = ['id', 'full_name']
    
    if not isinstance(item_data, dict):
        return False
    
    for field in required_fields:
        if field not in item_data or not item_data[field]:
            return False
    
    return True

def create_league_referee_item(item_data: dict) -> LeagueRefereeItem:
    """Create league referee item from API data"""
    loader = LeagueRefereeLoader()
    
    # Basic referee information
    loader.add_value('id', item_data.get('id'))
    loader.add_value('full_name', item_data.get('full_name'))
    loader.add_value('first_name', item_data.get('first_name'))
    loader.add_value('last_name', item_data.get('last_name'))
    loader.add_value('known_as', item_data.get('known_as'))
    loader.add_value('shorthand', item_data.get('shorthand'))
    loader.add_value('age', item_data.get('age'))
    loader.add_value('nationality', item_data.get('nationality'))
    loader.add_value('birthday', item_data.get('birthday'))
    
    # League-specific information
    loader.add_value('league', item_data.get('league'))
    loader.add_value('season', item_data.get('season'))
    loader.add_value('competition_id', item_data.get('competition_id'))
    loader.add_value('starting_year', item_data.get('starting_year'))
    loader.add_value('ending_year', item_data.get('ending_year'))
    
    # Appearance statistics
    loader.add_value('appearances_overall', item_data.get('appearances_overall'))
    loader.add_value('appearances_home', item_data.get('appearances_home'))
    loader.add_value('appearances_away', item_data.get('appearances_away'))
    
    # Match outcome statistics
    loader.add_value('wins_home', item_data.get('wins_home'))
    loader.add_value('wins_away', item_data.get('wins_away'))
    loader.add_value('draws_overall', item_data.get('draws_overall'))
    loader.add_value('wins_per_home', item_data.get('wins_per_home'))
    loader.add_value('wins_per_away', item_data.get('wins_per_away'))
    loader.add_value('draws_per', item_data.get('draws_per'))
    
    # Goal statistics
    loader.add_value('goals_overall', item_data.get('goals_overall'))
    loader.add_value('goals_home', item_data.get('goals_home'))
    loader.add_value('goals_away', item_data.get('goals_away'))
    loader.add_value('goals_per_match_overall', item_data.get('goals_per_match_overall'))
    loader.add_value('goals_per_match_home', item_data.get('goals_per_match_home'))
    loader.add_value('goals_per_match_away', item_data.get('goals_per_match_away'))
    
    # BTTS statistics
    loader.add_value('btts_overall', item_data.get('btts_overall'))
    loader.add_value('btts_percentage', item_data.get('btts_percentage'))
    
    # Penalty statistics
    loader.add_value('penalties_given_overall', item_data.get('penalties_given_overall'))
    loader.add_value('penalties_given_home', item_data.get('penalties_given_home'))
    loader.add_value('penalties_given_away', item_data.get('penalties_given_away'))
    loader.add_value('penalties_given_per_match_overall', item_data.get('penalties_given_per_match_overall'))
    loader.add_value('penalties_given_per_match_home', item_data.get('penalties_given_per_match_home'))
    loader.add_value('penalties_given_per_match_away', item_data.get('penalties_given_per_match_away'))
    
    # Card statistics
    loader.add_value('cards_overall', item_data.get('cards_overall'))
    loader.add_value('cards_home', item_data.get('cards_home'))
    loader.add_value('cards_away', item_data.get('cards_away'))
    loader.add_value('cards_per_match_overall', item_data.get('cards_per_match_overall'))
    loader.add_value('cards_per_match_home', item_data.get('cards_per_match_home'))
    loader.add_value('cards_per_match_away', item_data.get('cards_per_match_away'))
    
    # Red card statistics
    loader.add_value('red_cards_overall', item_data.get('red_cards_overall'))
    loader.add_value('red_cards_home', item_data.get('red_cards_home'))
    loader.add_value('red_cards_away', item_data.get('red_cards_away'))
    loader.add_value('red_cards_per_match_overall', item_data.get('red_cards_per_match_overall'))
    loader.add_value('red_cards_per_match_home', item_data.get('red_cards_per_match_home'))
    loader.add_value('red_cards_per_match_away', item_data.get('red_cards_per_match_away'))
    
    # Over/Under statistics
    loader.add_value('over_05_percentage', item_data.get('over_05_percentage'))
    loader.add_value('over_15_percentage', item_data.get('over_15_percentage'))
    loader.add_value('over_25_percentage', item_data.get('over_25_percentage'))
    loader.add_value('over_35_percentage', item_data.get('over_35_percentage'))
    
    # Additional context
    loader.add_value('continent', item_data.get('continent'))
    loader.add_value('league_type', item_data.get('league_type'))
    loader.add_value('url', item_data.get('url'))
    
    # Metadata
    loader.add_value('extracted_at', None)
    
    return loader.load_item()