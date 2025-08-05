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

def convert_unix_timestamp(timestamp):
    """Convert UNIX timestamp to datetime object"""
    try:
        if isinstance(timestamp, (int, float)):
            return datetime.fromtimestamp(timestamp)
        return None
    except (ValueError, TypeError):
        return None

class TodayMatchItem(Item):
    """Item for individual match from /today endpoint"""
    id = Field()                    # Match ID
    date_unix = Field()             # Match timestamp as datetime
    competition_name = Field()      # League/competition name
    competition_id = Field()        # League ID
    home_name = Field()             # Home team name
    away_name = Field()             # Away team name
    home_id = Field()               # Home team ID
    away_id = Field()               # Away team ID
    status = Field()                # Match status
    extracted_at = Field()          # When this was extracted

class TodayMatchLoader(ItemLoader):
    """Item loader for today match data"""
    
    default_item_class = TodayMatchItem
    default_input_processor = MapCompose(clean_string)
    default_output_processor = TakeFirst()
    
    id_in = MapCompose(safe_int)
    date_unix_in = MapCompose(convert_unix_timestamp)
    competition_id_in = MapCompose(safe_int)
    home_id_in = MapCompose(safe_int)
    away_id_in = MapCompose(safe_int)
    extracted_at_in = MapCompose(lambda x: datetime.now())

def validate_today_match_item(item_data: dict) -> bool:
    """Validate today match data structure before processing"""
    required_fields = ['id', 'home_name', 'away_name', 'competition_name']
    
    if not isinstance(item_data, dict):
        return False
    
    for field in required_fields:
        if field not in item_data or not item_data[field]:
            return False
    
    return True

def create_today_match_item(item_data: dict) -> TodayMatchItem:
    """Create today match item from API data"""
    loader = TodayMatchLoader()
    
    loader.add_value('id', item_data.get('id'))
    loader.add_value('date_unix', item_data.get('date_unix'))
    loader.add_value('competition_name', item_data.get('competition_name'))
    loader.add_value('competition_id', item_data.get('competition_id'))
    loader.add_value('home_name', item_data.get('home_name'))
    loader.add_value('away_name', item_data.get('away_name'))
    loader.add_value('home_id', item_data.get('home_id'))
    loader.add_value('away_id', item_data.get('away_id'))
    loader.add_value('status', item_data.get('status'))
    loader.add_value('extracted_at', None)
    
    return loader.load_item()