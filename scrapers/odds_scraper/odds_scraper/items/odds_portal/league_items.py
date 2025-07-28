# scrapers/odds_scraper/odds_scraper/items/odds_portal/league_items.py

from scrapy import Item, Field
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst, Identity
from datetime import datetime

def convert_unix_timestamp(timestamp):
    """Convert UNIX timestamp to datetime object"""
    try:
        if isinstance(timestamp, (int, float)):
            return datetime.fromtimestamp(timestamp)
        return None
    except (ValueError, TypeError):
        return None

# -------------------- League Discovery Items --------------------

class SportItem(Item):
    """Sport information"""
    sport_id = Field()
    sport_name = Field()
    sport_url_slug = Field()

class CountryItem(Item):
    """Country information"""
    country_id = Field()
    country_name = Field()
    country_url_slug = Field()
    region = Field()

class LeagueItem(Item):
    """League/Tournament information"""
    league_id = Field()           # Encoded ID from OddsPortal
    league_name = Field()         # Display name
    league_url_slug = Field()     # URL component
    league_url = Field()          # Full base URL
    sport_id = Field()
    sport_name = Field()
    country_id = Field()
    country_name = Field()
    is_active = Field()
    league_type = Field()         # domestic, international, cup

class SeasonItem(Item):
    """Individual season for a league"""
    season_id = Field()           # e.g., "2023-2024" or "current"
    season_name = Field()         # Display name
    season_url = Field()          # Full URL to season
    league_id = Field()
    league_name = Field()
    is_current = Field()          # Boolean
    start_year = Field()          # Extracted from season_id
    end_year = Field()            # Extracted from season_id
    has_results = Field()         # Whether /results/ page exists
    has_fixtures = Field()        # Whether upcoming matches exist

class LeagueDiscoveryItem(Item):
    """Complete league discovery result"""
    # Sport info
    sport = Field()               # SportItem
    
    # Country info
    country = Field()             # CountryItem
    
    # League info
    league = Field()              # LeagueItem
    
    # Available seasons
    seasons = Field()             # List of SeasonItem
    total_seasons = Field()
    
    # Metadata
    discovery_timestamp = Field()
    discovery_url = Field()       # URL used for discovery

# -------------------- Match List Items --------------------

class MatchInfoItem(Item):
    """Minimal match info for feeding to match spider"""
    # Essential identifiers
    match_id = Field()            # OddsPortal match ID
    match_url = Field()           # Full URL to match page
    
    # Timing
    match_timestamp = Field()     # datetime object
    status = Field()              # scheduled, finished, live, postponed
    
    # Teams
    home_team = Field()
    away_team = Field()
    
    # Context
    league_id = Field()
    league_name = Field()
    season_id = Field()
    sport_id = Field()
    tournament_stage = Field()    # Regular Season, Playoffs, etc.
    
    # Metadata
    extracted_at = Field()        # When this was extracted

class SeasonMatchesItem(Item):
    """Container for matches from a season"""
    # Season identification  
    league_id = Field()
    league_name = Field()
    season_id = Field()
    sport_id = Field()
    sport_name = Field()
    country_name = Field()
    
    # Extraction info
    extraction_type = Field()     # "results" or "fixtures"
    page_number = Field()
    total_pages = Field()
    has_next_page = Field()
    
    # Matches
    matches = Field()             # List of MatchInfoItem
    total_matches = Field()
    
    # Metadata
    extraction_timestamp = Field()
    source_url = Field()

# -------------------- Loaders --------------------

class SportLoader(ItemLoader):
    default_item_class = SportItem
    default_input_processor = MapCompose()
    default_output_processor = TakeFirst()

class CountryLoader(ItemLoader):
    default_item_class = CountryItem
    default_input_processor = MapCompose()
    default_output_processor = TakeFirst()

class LeagueLoader(ItemLoader):
    default_item_class = LeagueItem
    default_input_processor = MapCompose()
    default_output_processor = TakeFirst()
    
    is_active_in = MapCompose(lambda x: x if isinstance(x, bool) else True)

class SeasonLoader(ItemLoader):
    default_item_class = SeasonItem
    default_input_processor = MapCompose()
    default_output_processor = TakeFirst()
    
    # Extract years from season_id like "2023-2024"
    start_year_in = MapCompose(lambda x: int(x.split('-')[0]) if '-' in str(x) else None)
    end_year_in = MapCompose(lambda x: int(x.split('-')[1]) if '-' in str(x) else None)
    
    # Boolean fields
    is_current_in = MapCompose(lambda x: x if isinstance(x, bool) else False)
    has_results_in = MapCompose(lambda x: x if isinstance(x, bool) else True)
    has_fixtures_in = MapCompose(lambda x: x if isinstance(x, bool) else False)

class LeagueDiscoveryLoader(ItemLoader):
    default_item_class = LeagueDiscoveryItem
    default_input_processor = MapCompose()
    default_output_processor = TakeFirst()
    
    # Object fields stay as objects
    sport_out = Identity()
    country_out = Identity()
    league_out = Identity()
    
    # List fields
    seasons_out = Identity()
    
    # Timestamp
    discovery_timestamp_in = MapCompose(lambda x: datetime.now())

class MatchInfoLoader(ItemLoader):
    default_item_class = MatchInfoItem
    default_input_processor = MapCompose()
    default_output_processor = TakeFirst()
    
    # Timestamp conversion
    match_timestamp_in = MapCompose(convert_unix_timestamp)
    extracted_at_in = MapCompose(lambda x: datetime.now())
    
    # Status mapping from status-id
    status_in = MapCompose(lambda x: {
        0: "scheduled",
        1: "live", 
        2: "live",
        3: "finished",
        4: "postponed",
        5: "cancelled"
    }.get(x, "unknown") if isinstance(x, int) else x)

class SeasonMatchesLoader(ItemLoader):
    default_item_class = SeasonMatchesItem
    default_input_processor = MapCompose()
    default_output_processor = TakeFirst()
    
    # List field
    matches_out = Identity()
    
    # Timestamp
    extraction_timestamp_in = MapCompose(lambda x: datetime.now())