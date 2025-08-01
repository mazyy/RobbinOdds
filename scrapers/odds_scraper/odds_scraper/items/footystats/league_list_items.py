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

class SeasonItem(Item):
    """Individual season entity"""
    id = Field()            # Season ID from FootyStats
    year = Field()          # Season year or year range
    extracted_at = Field()  # When this was extracted

class LeagueListItem(Item):
    """Item for individual league from /league-list endpoint"""
    name = Field()          # Full league name (e.g., "USA MLS")
    country = Field()       # Country name
    league_name = Field()   # League name only (e.g., "MLS")
    season = Field()        # List of SeasonItem objects
    extracted_at = Field()  # When this was extracted

class SeasonLoader(ItemLoader):
    """Item loader for season data"""
    
    default_item_class = SeasonItem
    default_input_processor = MapCompose()
    default_output_processor = TakeFirst()
    
    id_in = MapCompose(safe_int)
    year_in = MapCompose(safe_int)
    extracted_at_in = MapCompose(lambda x: datetime.now())

class LeagueListLoader(ItemLoader):
    """Item loader for league list data"""
    
    default_item_class = LeagueListItem
    default_input_processor = MapCompose(clean_string)
    default_output_processor = TakeFirst()
    
    name_in = MapCompose(clean_string)
    country_in = MapCompose(clean_string)
    league_name_in = MapCompose(clean_string)
    season_out = Identity()  # Keep as list
    extracted_at_in = MapCompose(lambda x: datetime.now())

def validate_league_list_item(item_data: dict) -> bool:
    """Validate league data structure before processing"""
    required_fields = ['name', 'country', 'league_name']
    
    if not isinstance(item_data, dict):
        return False
    
    for field in required_fields:
        if field not in item_data or not item_data[field]:
            return False
    
    return True

def create_season_item(season_data: dict) -> SeasonItem:
    """Create season item from API data"""
    loader = SeasonLoader()
    
    loader.add_value('id', season_data.get('id'))
    loader.add_value('year', season_data.get('year'))
    loader.add_value('extracted_at', None)
    
    return loader.load_item()

def create_league_list_item(item_data: dict) -> LeagueListItem:
    """Create league list item from API data"""
    loader = LeagueListLoader()
    
    loader.add_value('name', item_data.get('name'))
    loader.add_value('country', item_data.get('country'))
    loader.add_value('league_name', item_data.get('league_name'))
    loader.add_value('extracted_at', None)
    
    # Process seasons
    seasons_data = item_data.get('season', [])
    season_items = []
    
    for season_data in seasons_data:
        if isinstance(season_data, dict):
            season_item = create_season_item(season_data)
            season_items.append(season_item)
    
    loader.add_value('season', season_items)
    
    return loader.load_item()