from scrapy import Item, Field
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Identity
from datetime import datetime
import json


class FootyStatsBaseItem(Item):
    """Base item for all FootyStats API responses"""
    
    # Metadata fields - always present
    schema_version = Field(default="1.0.0")
    scraped_at = Field(default_factory=lambda: datetime.utcnow().isoformat())
    spider_name = Field()
    source_url = Field()
    api_endpoint = Field()
    
    # Common API fields
    api_key_used = Field()
    response_status = Field()
    
    def __setitem__(self, key, value):
        """Override to ensure consistent datetime formatting"""
        if key == 'scraped_at' and isinstance(value, datetime):
            value = value.isoformat()
        super().__setitem__(key, value)


class FootyStatsBaseItemLoader(ItemLoader):
    """Base loader for FootyStats items with common processors"""
    
    default_item_class = FootyStatsBaseItem
    
    # Default processors
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()
    
    # Metadata processors
    scraped_at_in = MapCompose(
        lambda x: datetime.fromisoformat(x) if isinstance(x, str) else x,
        lambda x: x.isoformat() if isinstance(x, datetime) else x
    )
    
    # Numeric processors
    @staticmethod
    def process_integer(value):
        """Convert to integer, handle None and empty strings"""
        if value is None or value == '':
            return None
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def process_float(value):
        """Convert to float, handle None and empty strings"""
        if value is None or value == '':
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def process_boolean(value):
        """Convert to boolean"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        return bool(value)
    
    @staticmethod
    def process_json_list(value):
        """Parse JSON list from string"""
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return []
        return []


# Common processing functions
def safe_int(value):
    """Safely convert to integer, returns None for invalid values"""
    if value is None or value == '':
        return None
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return None


def safe_float(value):
    """Safely convert to float, returns None for invalid values"""
    if value is None or value == '':
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def clean_string(value):
    """Clean and strip string values"""
    if isinstance(value, str):
        return value.strip()
    return value


# Export main classes
__all__ = ['FootyStatsBaseItem', 'FootyStatsBaseItemLoader', 'safe_int', 'safe_float', 'clean_string']