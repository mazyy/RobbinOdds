# scrapers/odds_scraper/odds_scraper/items/footystats/country_list_items.py

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

class CountryListItem(Item):
    """Item for individual country from /country-list endpoint"""
    id = Field()            # Country ID from FootyStats
    iso = Field()           # ISO country code
    country = Field()       # Country name
    iso_number = Field()    # ISO numeric code
    extracted_at = Field()  # When this was extracted

class CountryListLoader(ItemLoader):
    """Item loader for country list data with validation and processing"""
    
    default_item_class = CountryListItem
    default_input_processor = MapCompose(clean_string)
    default_output_processor = TakeFirst()
    
    id_in = MapCompose(safe_int)
    iso_in = MapCompose(clean_string) 
    country_in = MapCompose(clean_string)
    iso_number_in = MapCompose(safe_int)
    extracted_at_in = MapCompose(lambda x: datetime.now())

def validate_country_list_item(item_data: dict) -> bool:
    """Validate country data structure before processing"""
    required_fields = ['id', 'country']
    
    if not isinstance(item_data, dict):
        return False
    
    for field in required_fields:
        if field not in item_data or not item_data[field]:
            return False
    
    return True

def create_country_list_item(item_data: dict) -> CountryListItem:
    """Create country list item from API data"""
    loader = CountryListLoader()
    
    loader.add_value('id', item_data.get('id'))
    loader.add_value('iso', item_data.get('iso'))
    loader.add_value('country', item_data.get('country'))
    loader.add_value('iso_number', item_data.get('iso_number'))
    loader.add_value('extracted_at', None)
    
    return loader.load_item()