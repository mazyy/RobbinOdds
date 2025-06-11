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

def parse_score(score_str):
    """Parse score string like '98:107' into dict"""
    try:
        if score_str and ':' in score_str:
            home, away = score_str.strip().split(':')
            return {
                'home': int(home.strip()),
                'away': int(away.strip())
            }
        return None
    except (ValueError, TypeError):
        return None

def parse_partial_scores(partial_str):
    """Parse partial scores like '29:32, 19:21, 27:26, 23:28' into list of dicts"""
    try:
        if not partial_str:
            return []
        
        quarters = []
        for quarter in partial_str.split(','):
            if ':' in quarter:
                home, away = quarter.strip().split(':')
                quarters.append({
                    'home': int(home.strip()),
                    'away': int(away.strip())
                })
        return quarters
    except (ValueError, TypeError):
        return []

# -------------------- Items --------------------

class MatchResultItem(Item):
    """Individual match result from league results page"""
    # Match identification
    match_id = Field()
    encoded_event_id = Field()
    match_url = Field()
    
    # Teams
    home_team_name = Field()
    away_team_name = Field()
    home_team_id = Field()
    away_team_id = Field()
    home_country = Field()
    away_country = Field()
    
    # Match status
    status_id = Field()
    event_stage_id = Field()
    event_stage_name = Field()
    is_finished = Field()
    is_after_extra_time = Field()
    
    # Tournament info
    tournament_id = Field()
    tournament_name = Field()
    tournament_stage_id = Field()
    tournament_stage_name = Field()
    sport_id = Field()
    sport_name = Field()
    country_name = Field()
    
    # Scores
    final_score = Field()  # Dict with 'home' and 'away' keys
    home_score = Field()
    away_score = Field()
    partial_scores = Field()  # List of dicts for quarter/period scores
    
    # Winner
    home_winner_status = Field()  # 'win', 'lost', 'draw'
    away_winner_status = Field()
    
    # Match timing
    match_timestamp = Field()  # datetime object
    
    # Venue
    venue = Field()
    venue_town = Field()
    venue_country = Field()
    
    # Odds summary
    bookmakers_count = Field()
    odds_summary = Field()  # List of OddsSummaryItem
    
    # Additional info
    match_info = Field()  # List of additional match info

class OddsSummaryItem(Item):
    """Summary of odds for a specific betting type/outcome"""
    event_id = Field()
    outcome_id = Field()
    outcome_result_id = Field()  # 1 or 2 indicating which team
    betting_type_id = Field()
    scope_id = Field()
    avg_odds = Field()
    max_odds = Field()
    max_odds_provider_id = Field()
    is_active = Field()
    active_bookmakers_count = Field()

class LeagueResultsPageItem(Item):
    """Container for a page of league results"""
    tournament_id = Field()
    tournament_name = Field()
    season = Field()
    page_number = Field()
    total_matches = Field()
    matches_per_page = Field()
    total_pages = Field()
    has_next_page = Field()
    matches = Field()  # List of MatchResultItem

# -------------------- Loaders --------------------

class MatchResultLoader(ItemLoader):
    default_item_class = MatchResultItem
    default_input_processor = MapCompose()
    default_output_processor = TakeFirst()
    
    # List fields
    partial_scores_in = MapCompose(parse_partial_scores)
    partial_scores_out = Identity()  # Keep as list
    
    odds_summary_out = Identity()  # Keep as list
    match_info_out = Identity()  # Keep as list
    
    # Score parsing
    final_score_in = MapCompose(parse_score)
    
    # Timestamp conversion
    match_timestamp_in = MapCompose(convert_unix_timestamp)
    
    # Boolean fields
    is_finished_in = MapCompose(lambda x: x == 3)
    is_after_extra_time_in = MapCompose(lambda x: x == 10)

class OddsSummaryLoader(ItemLoader):
    default_item_class = OddsSummaryItem
    default_input_processor = MapCompose()
    default_output_processor = TakeFirst()
    
    # Float fields
    avg_odds_in = MapCompose(float)
    max_odds_in = MapCompose(float)
    
    # Integer fields
    active_bookmakers_count_in = MapCompose(int)

class LeagueResultsPageLoader(ItemLoader):
    default_item_class = LeagueResultsPageItem
    default_input_processor = MapCompose()
    default_output_processor = TakeFirst()
    
    # List field
    matches_out = Identity()  # Keep as list