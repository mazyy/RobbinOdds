import json
import re
from scrapy import Item, Field
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst


def parse_json(response):
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {}


def to_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


# -------------------- Items --------------------

class TeamItem(Item):
    name = Field()

class OddsItem(Item):
    provider = Field()
    market = Field()
    scope = Field()
    selection = Field()
    value = Field()
    timestamp = Field()

class PageVarItem(Item):
    default_betting_type = Field()
    default_scope = Field()
    nav = Field()
    nav_filtered = Field()

class EventHeaderItem(Item):
    match_id = Field()
    xhash = Field()
    xhashf = Field()
    is_live = Field()
    real_live = Field()
    is_postponed = Field()
    is_started = Field()
    is_finished = Field()
    is_finished_grace_period = Field()
    sport_id = Field()
    sport_name = Field()
    sport_url = Field()
    home = Field()
    away = Field()
    tournament_id = Field()
    tournament_name = Field()
    tournament_url = Field()
    country_name = Field()
    default_bet_id = Field()
    user_bett_id = Field()
    user_id = Field()
    default_scope_id = Field()
    version_id = Field()

class EventBodyItem(Item):
    start_date = Field()
    end_date = Field()
    home_result = Field()
    away_result = Field()
    partial_result = Field()
    event_stage_name = Field()
    event_stage_id = Field()
    ft_only = Field()
    ft_only_text = Field()
    ft_only_text_short = Field()
    venue = Field()
    venue_town = Field()
    venue_country = Field()
    additional_odds_info = Field()
    providers_names = Field()
    providers_is_betting_exchange = Field()
    request_pre_match = Field()
    request_base_pre_match = Field()
    update_score_request = Field()
    updatescore_request_base = Field()
    request_match_facts = Field()
    request_event_data = Field()
    request_last_results = Field()
    request_betting_exchanges = Field()
    
class MatchItem(Item):
    header = Field()
    body = Field()
    pagevar = Field()
    home_team = Field()
    away_team = Field()
    odds = Field()
    


# -------------------- Loaders --------------------

class TeamLoader(ItemLoader):
    default_item_class = TeamItem
    default_input_processor = MapCompose()
    default_output_processor = TakeFirst()

class OddsLoader(ItemLoader):
    default_item_class = OddsItem
    default_input_processor = MapCompose()
    default_output_processor = TakeFirst()
    value_in = MapCompose(to_float)

class PageVarLoader(ItemLoader):
    default_item_class = PageVarItem
    default_input_processor = MapCompose()
    default_output_processor = TakeFirst()

class HeaderLoader(ItemLoader):
    default_item_class = EventHeaderItem
    default_input_processor = MapCompose()
    default_output_processor = TakeFirst()

class BodyLoader(ItemLoader):
    default_item_class = EventBodyItem
    default_input_processor = MapCompose()
    default_output_processor = TakeFirst()

class MatchLoader(ItemLoader):
    default_item_class = MatchItem
    default_input_processor = MapCompose()
    default_output_processor = TakeFirst()
    odds_out = MapCompose(lambda x: x)
