# FootyStats Items - CLAUDE.md

This file provides comprehensive guidance for developing, testing, and maintaining FootyStats item structures, field mappings, and data processing workflows.

## Overview

FootyStats items define the data structures for comprehensive football/soccer data extracted from the FootyStats API. Each item includes validation functions, data loaders, and type-safe field processing to ensure data quality and consistency.

## Development Philosophy

### API-First Data Modeling
Items are designed to mirror API response structures while adding defensive processing:
- **Direct Field Mapping**: Map API fields to item fields with minimal transformation
- **Type Safety**: Use safe conversion functions for all numeric and date fields
- **Null Tolerance**: Handle missing/null values gracefully without errors
- **Forward Compatibility**: Over-inclusive field mapping captures new API fields

### Comprehensive Field Coverage Strategy
Each item captures **all available fields** from API responses:
- **Future-Proof Design**: New API fields won't break existing workflows
- **Rich Analytics Data**: Comprehensive data enables advanced betting strategies
- **Type-Safe Processing**: All fields use appropriate validation and conversion
- **Metadata Enrichment**: Add spider context and extraction timestamps

## Item Architecture

### Standard Item Pattern
Each FootyStats item follows a consistent pattern:
1. **Item Class** - Defines field structure with comprehensive coverage
2. **ItemLoader Class** - Handles field processing and type conversion  
3. **Validation Function** - Validates data structure before processing
4. **Creation Function** - Creates item instances from API data

### Field Processing Standards
- **String fields**: `MapCompose(clean_string)` - Strips whitespace
- **Integer fields**: `MapCompose(safe_int)` - Safe integer conversion
- **Float fields**: `MapCompose(safe_float)` - Safe float conversion  
- **Array fields**: `Identity()` output processor - Preserves arrays
- **Timestamp fields**: `MapCompose(lambda x: datetime.now())` - Auto-timestamps

## Item Development Workflow

### 1. HTML Documentation Analysis
Before creating any item, analyze the saved HTML documentation to understand API structure:

```bash
# View saved API documentation
open scrapers/tests/resources/footystats/your_endpoint_api_documentations.html

# Identify field structure from documentation
# Look for:
# - Required vs optional fields
# - Data types (string, integer, float, array)
# - Nested objects and their properties
# - Example values and formats
```

### 2. JSON Sample Response Analysis
Extract field mapping from sample responses:

```python
# Load sample responses
import json
with open('scrapers/tests/resources/footystats/sample_responses.json', 'r') as f:
    samples = json.load(f)

# Analyze your endpoint's structure
endpoint_sample = samples['your_endpoint']['response']

# For array responses, examine first item
if isinstance(endpoint_sample, list) and len(endpoint_sample) > 0:
    sample_item = endpoint_sample[0]
    print("Available fields:", list(sample_item.keys()))
    
    # Check for nested objects
    for key, value in sample_item.items():
        if isinstance(value, dict):
            print(f"Nested object '{key}':", list(value.keys()))
```

### 3. Test-Driven Item Development
Follow TDD approach for item creation:

#### Step 1: Write Failing Test
```python
# tests/contracts/test_footystats_your_endpoint_items.py
import pytest
from odds_scraper.items.footystats.your_endpoint_items import (
    YourEndpointItem, validate_your_endpoint_item, create_your_endpoint_item
)

class TestYourEndpointItem:
    def test_item_creation_with_valid_data(self, sample_api_data):
        """Test item creation with valid API data"""
        assert validate_your_endpoint_item(sample_api_data)
        item = create_your_endpoint_item(sample_api_data)
        
        # Test required fields
        assert item['id'] is not None
        assert item['name'] is not None
        
        # Test field types
        assert isinstance(item['id'], int)
        assert isinstance(item['name'], str)
```

#### Step 2: Create Item Structure
```python
# odds_scraper/items/footystats/your_endpoint_items.py
from scrapy import Item, Field
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Identity
from datetime import datetime

class YourEndpointItem(Item):
    # Required fields (from API documentation)
    id = Field()
    name = Field()
    
    # Optional fields (comprehensive coverage)
    clean_name = Field()
    short_name = Field()
    description = Field()
    
    # Numeric fields
    value = Field()
    count = Field()
    percentage = Field()
    
    # Nested object fields
    stats_field1 = Field()
    stats_field2 = Field()
    
    # Array fields
    recent_form = Field()
    categories = Field()
    
    # Metadata fields
    spider_name = Field()
    scraped_at = Field()
    schema_version = Field()

class YourEndpointLoader(ItemLoader):
    default_item_class = YourEndpointItem
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()
    
    # String field processors
    name_in = MapCompose(clean_string)
    clean_name_in = MapCompose(clean_string)
    short_name_in = MapCompose(clean_string)
    
    # Numeric field processors
    id_in = MapCompose(safe_int)
    value_in = MapCompose(safe_float)
    count_in = MapCompose(safe_int)
    percentage_in = MapCompose(safe_float)
    
    # Array field processors
    recent_form_out = Identity()
    categories_out = Identity()
    
    # Metadata processors
    scraped_at_in = MapCompose(lambda x: datetime.now().isoformat())
    schema_version_in = MapCompose(lambda x: "1.0.0")
```

#### Step 3: Implement Validation and Creation Functions
```python
def validate_your_endpoint_item(item_data: dict) -> bool:
    """Validate API data structure before processing"""
    if not isinstance(item_data, dict):
        return False
    
    # Check required fields
    required_fields = ['id', 'name']
    for field in required_fields:
        if field not in item_data or item_data[field] is None:
            return False
    
    # Validate field types for critical fields
    if not isinstance(item_data.get('id'), (int, str)):
        return False
    
    if not isinstance(item_data.get('name'), str):
        return False
    
    return True

def create_your_endpoint_item(item_data: dict) -> YourEndpointItem:
    """Create item instance from validated API data"""
    loader = YourEndpointLoader()
    
    # Required fields
    loader.add_value('id', item_data.get('id'))
    loader.add_value('name', item_data.get('name'))
    
    # Optional fields with safe extraction
    loader.add_value('clean_name', item_data.get('cleanName'))
    loader.add_value('short_name', item_data.get('shortName'))
    loader.add_value('description', item_data.get('description'))
    
    # Numeric fields
    loader.add_value('value', item_data.get('value'))
    loader.add_value('count', item_data.get('count'))
    loader.add_value('percentage', item_data.get('percentage'))
    
    # Handle nested objects safely
    stats = item_data.get('stats', {})
    if isinstance(stats, dict):
        loader.add_value('stats_field1', stats.get('field1'))
        loader.add_value('stats_field2', stats.get('field2'))
    
    # Handle array fields
    loader.add_value('recent_form', item_data.get('recentForm', []))
    loader.add_value('categories', item_data.get('categories', []))
    
    # Add metadata
    loader.add_value('scraped_at', None)  # Processor handles timestamp
    loader.add_value('schema_version', None)  # Processor handles version
    
    return loader.load_item()
```

### 4. HTML Sample Workflow Integration
Items are designed to handle data from HTML documentation samples:

#### Processing Documentation Examples
```python
# Extract fields from HTML documentation examples
def extract_fields_from_html_sample(html_content):
    """Extract field structure from API documentation HTML"""
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Look for JSON examples in documentation
    json_examples = soup.find_all('code', class_='json')
    
    for example in json_examples:
        try:
            sample_data = json.loads(example.text)
            if isinstance(sample_data, dict):
                return analyze_field_structure(sample_data)
        except json.JSONDecodeError:
            continue
    
    return {}

def analyze_field_structure(data_dict):
    """Analyze field types and nesting in sample data"""
    field_analysis = {}
    
    for key, value in data_dict.items():
        field_analysis[key] = {
            'type': type(value).__name__,
            'required': value is not None,
            'sample_value': value
        }
        
        if isinstance(value, dict):
            field_analysis[key]['nested_fields'] = analyze_field_structure(value)
    
    return field_analysis
```

#### Generating Item Templates from Samples
```python
def generate_item_template(endpoint_name, sample_data):
    """Generate item class template from sample data"""
    template = f"""
class {endpoint_name.title()}Item(Item):
    # Generated from sample data analysis
"""
    
    field_analysis = analyze_field_structure(sample_data)
    
    for field_name, analysis in field_analysis.items():
        comment = f"# {analysis['type']}"
        if analysis.get('nested_fields'):
            comment += " (nested object)"
        
        template += f"    {field_name} = Field()  {comment}\n"
    
    return template
```

### 5. Integration Testing with Real API Data
Test items with actual API responses:

```python
# Integration test with live API data
def test_item_with_live_api_data():
    """Test item creation with real API response"""
    import requests
    
    # Make actual API call (with rate limiting)
    response = requests.get(
        'https://api.football-data-api.com/your-endpoint',
        params={'key': 'example', 'param': 'value'}
    )
    
    if response.status_code == 200:
        api_data = response.json().get('data', [])
        
        if api_data:
            # Test with first item
            first_item = api_data[0] if isinstance(api_data, list) else api_data
            
            assert validate_your_endpoint_item(first_item)
            item = create_your_endpoint_item(first_item)
            
            # Verify no fields are missing
            assert item is not None
            print(f"Successfully created item: {item.get('name', 'Unknown')}")
```

### 6. Error Handling Patterns
Robust error handling for production use:

```python
def safe_create_item(item_data, spider_logger=None):
    """Safely create item with comprehensive error handling"""
    try:
        # Validate structure first
        if not validate_your_endpoint_item(item_data):
            if spider_logger:
                spider_logger.warning(f"Invalid item data structure: {item_data}")
            return None
        
        # Create item
        item = create_your_endpoint_item(item_data)
        
        if spider_logger:
            spider_logger.debug(f"Created item: {item.get('name', 'Unknown')}")
        
        return item
        
    except Exception as e:
        if spider_logger:
            spider_logger.error(f"Error creating item: {e}, Data: {item_data}")
        return None
```

## Available Item Types

### Core Items (Existing)
- `CountryListItem` - Country information
- `LeagueListItem` - League information
- `LeagueMatchesItem` - Match data (300+ fields)
- `LeagueStatsItem` - League statistics
- `LeagueTeamItem` - Team data (700+ fields)
- `LeaguePlayersItem` - Player data
- `LeagueRefereesItem` - Referee data
- `MatchDetailsItem` - Detailed match information
- `TeamItem` - Individual team data
- `PlayerItem` - Individual player data
- `RefereeItem` - Individual referee data
- `TodayItem` - Today's matches

### New Comprehensive Items
- `LeagueTableItem` - League standings and positions
- `BttsStatsItem` - Both Teams To Score statistics
- `OverStatsItem` - Over/Under goal statistics
- `TeamLastItem` - Recent team form analysis
- `TeamVsTeamItem` - Head-to-head team statistics
- `SeasonInfoItem` - Season metadata and information

## Detailed Item Documentation

### 1. League Table Item (`LeagueTableItem`)

**Purpose**: Captures league standings with comprehensive position and performance data.

**Field Count**: 33 fields

**Key Field Groups**:
```python
# Basic team information (5 fields)
id, name, cleanName, shortName, image

# League position data (9 fields)  
position, played, wins, draws, losses, goals_for, goals_against, goal_difference, points

# Form and performance (6 fields)
form, home_wins, home_draws, home_losses, away_wins, away_draws, away_losses

# Goal statistics by venue (4 fields)
home_goals_for, home_goals_against, away_goals_for, away_goals_against

# Additional metrics (4 fields)
points_per_game, goal_average, clean_sheets, failed_to_score

# Context and metadata (5 fields)
season_id, league_name, competition_id, extracted_at
```

**Usage Example**:
```python
from odds_scraper.items.footystats.league_table_items import (
    LeagueTableItem, validate_league_table_item, create_league_table_item
)

# Validate data
if validate_league_table_item(api_data):
    item = create_league_table_item(api_data)
    print(f"Team: {item['name']}, Position: {item['position']}, Points: {item['points']}")
```

**Data Flow**:
```
API Response → Validation (id, name, position required) → Field Processing → LeagueTableItem
```

---

### 2. BTTS Statistics Item (`BttsStatsItem`)

**Purpose**: Captures Both Teams To Score betting statistics with comprehensive breakdowns.

**Field Count**: 35 fields

**Key Field Groups**:
```python
# League identification (3 fields)
season_id, league_name, competition_id

# Core BTTS statistics (5 fields)
total_matches, btts_matches, btts_percentage, no_btts_matches, no_btts_percentage

# Venue breakdown (4 fields)
btts_home_matches, btts_home_percentage, btts_away_matches, btts_away_percentage

# Timing analysis (6 fields)
btts_first_half, btts_first_half_percentage, btts_second_half, btts_second_half_percentage, 
btts_both_halves, btts_both_halves_percentage

# Goal threshold combinations (6 fields)
btts_over_15, btts_over_15_percentage, btts_over_25, btts_over_25_percentage,
btts_over_35, btts_over_35_percentage

# Pattern analysis (8 fields)
avg_goals_btts_matches, avg_goals_no_btts_matches, longest_btts_streak, 
longest_no_btts_streak, current_btts_streak, current_no_btts_streak,
btts_last_5, btts_last_5_percentage, btts_last_10, btts_last_10_percentage

# Metadata (1 field)
extracted_at
```

**Usage Example**:
```python
from odds_scraper.items.footystats.btts_stats_items import (
    BttsStatsItem, validate_btts_stats_item, create_btts_stats_item
)

# Process BTTS data
if validate_btts_stats_item(api_data):
    item = create_btts_stats_item(api_data)
    print(f"League: {item['league_name']}, BTTS: {item['btts_percentage']}%")
```

---

### 3. Over/Under Statistics Item (`OverStatsItem`)

**Purpose**: Captures comprehensive Over/Under goal statistics for multiple thresholds.

**Field Count**: 62 fields

**Key Field Groups**:
```python
# League identification (3 fields)
season_id, league_name, competition_id

# Basic statistics (1 field)
total_matches

# Goal thresholds 0.5-5.5 (24 fields)
over_05_matches, over_05_percentage, under_05_matches, under_05_percentage,
over_15_matches, over_15_percentage, under_15_matches, under_15_percentage,
# ... (pattern continues for 2.5, 3.5, 4.5, 5.5)

# Venue breakdown (8 fields)
home_over_25_matches, home_over_25_percentage, home_under_25_matches, home_under_25_percentage,
away_over_25_matches, away_over_25_percentage, away_under_25_matches, away_under_25_percentage

# Half-time analysis (12 fields)
first_half_over_05_matches, first_half_over_05_percentage, # ... (for 0.5, 1.5, 2.5)
second_half_over_05_matches, second_half_over_05_percentage, # ... (for 0.5, 1.5, 2.5)

# Goal averages and patterns (5 fields)
average_goals_per_match, average_home_goals, average_away_goals,
highest_scoring_match, lowest_scoring_match

# Streaks and recent form (8 fields)
longest_over_25_streak, longest_under_25_streak, current_over_25_streak, current_under_25_streak,
over_25_last_5, over_25_last_5_percentage, over_25_last_10, over_25_last_10_percentage

# Metadata (1 field)
extracted_at
```

**Usage Example**:
```python
from odds_scraper.items.footystats.over_stats_items import (
    OverStatsItem, validate_over_stats_item, create_over_stats_item
)

# Process over/under data
if validate_over_stats_item(api_data):
    item = create_over_stats_item(api_data)
    print(f"League: {item['league_name']}, Over 2.5: {item['over_25_percentage']}%")
```

---

### 4. Team Recent Form Item (`TeamLastItem`)

**Purpose**: Captures recent team performance analysis for last N games.

**Field Count**: 75 fields

**Key Field Groups**:
```python
# Team identification (4 fields)
team_id, team_name, clean_name, image

# Form period configuration (3 fields)
games_analyzed, period_start_date, period_end_date

# Basic form statistics (7 fields)
matches_played, wins, draws, losses, win_percentage, points, points_per_game

# Goal statistics (7 fields)
goals_for, goals_against, goal_difference, goals_for_per_game, goals_against_per_game,
clean_sheets, failed_to_score

# Home/away breakdown (12 fields)
home_matches, home_wins, home_draws, home_losses, home_goals_for, home_goals_against,
away_matches, away_wins, away_draws, away_losses, away_goals_for, away_goals_against

# Form patterns (5 fields)
recent_results, form_string, current_streak, current_streak_length

# Performance metrics (4 fields)
btts_matches, btts_percentage, over_25_matches, over_25_percentage

# Opposition analysis (3 fields)
avg_opposition_position, strong_opposition_results, weak_opposition_results

# Timing patterns (4 fields)
first_half_goals_for, first_half_goals_against, second_half_goals_for, second_half_goals_against

# Match outcome patterns (5 fields)
leading_at_ht, drawing_at_ht, trailing_at_ht, comeback_wins, blown_leads

# Context and metadata (4 fields)
season_id, competition_id, last_updated, extracted_at
```

**Usage Example**:
```python
from odds_scraper.items.footystats.team_last_items import (
    TeamLastItem, validate_team_last_item, create_team_last_item
)

# Process team form data
if validate_team_last_item(api_data):
    item = create_team_last_item(api_data)
    print(f"Team: {item['team_name']}, Form: {item['form_string']}, PPG: {item['points_per_game']}")
```

---

### 5. Head-to-Head Item (`TeamVsTeamItem`)

**Purpose**: Captures comprehensive historical matchup data between two teams.

**Field Count**: 69 fields

**Key Field Groups**:
```python
# Team identification (6 fields)
home_team_id, home_team_name, home_team_image, away_team_id, away_team_name, away_team_image

# H2H summary (7 fields)
total_matches, home_team_wins, away_team_wins, draws, 
home_win_percentage, away_win_percentage, draw_percentage

# Goal statistics (6 fields)
total_goals, home_team_goals, away_team_goals, average_goals_per_match,
home_team_avg_goals, away_team_avg_goals

# Venue breakdown (15 fields)
matches_at_home_ground, home_ground_home_wins, home_ground_away_wins, home_ground_draws,
matches_at_away_ground, away_ground_home_wins, away_ground_away_wins, away_ground_draws,
neutral_venue_matches, neutral_venue_home_wins, neutral_venue_away_wins, neutral_venue_draws

# Competition breakdown (4 fields)
league_matches, cup_matches, friendly_matches, other_competition_matches

# Recent form (5 fields)
last_5_matches, last_5_home_wins, last_5_away_wins, last_5_draws, last_10_matches

# Goal patterns (6 fields)
btts_matches, btts_percentage, over_25_matches, over_25_percentage, under_25_matches, under_25_percentage

# Scoring patterns (4 fields)
clean_sheets_home, clean_sheets_away, failed_to_score_home, failed_to_score_away

# High/low scoring (4 fields)
highest_scoring_match, lowest_scoring_match, biggest_home_win, biggest_away_win

# Time periods (3 fields)
first_meeting_date, last_meeting_date, years_span

# Context information (9 fields)
matches_by_season, recent_seasons_record, recent_match_details, upcoming_fixtures,
sample_size_rating, competitive_balance, dominance_factor, competition_names,
season_ids, total_different_competitions, analysis_date, extracted_at
```

**Usage Example**:
```python
from odds_scraper.items.footystats.team_vs_team_items import (
    TeamVsTeamItem, validate_team_vs_team_item, create_team_vs_team_item
)

# Process H2H data
if validate_team_vs_team_item(api_data):
    item = create_team_vs_team_item(api_data)
    print(f"H2H: {item['home_team_name']} vs {item['away_team_name']}")
    print(f"Record: {item['home_team_wins']}-{item['draws']}-{item['away_team_wins']}")
```

---

### 6. Season Information Item (`SeasonInfoItem`)

**Purpose**: Captures comprehensive season metadata and competition information.

**Field Count**: 58 fields

**Key Field Groups**:
```python
# Season identification (4 fields)
season_id, season_name, season_display, season_format

# Competition information (7 fields)
competition_id, competition_name, competition_type, competition_level,
country_name, country_code, country_id

# Season timeline (5 fields)
season_start_date, season_end_date, current_matchday, total_matchdays, season_status

# Season structure (6 fields)
total_teams, total_matches, matches_played, matches_remaining, rounds_total, rounds_completed

# Points system (3 fields)
points_for_win, points_for_draw, points_for_loss

# Competition format (8 fields)
promotion_spots, relegation_spots, playoff_spots, european_spots,
home_away_format, neutral_venues, extra_time_rules, penalty_rules

# Current standings (6 fields)
current_leader_id, current_leader_name, current_leader_points,
bottom_team_id, bottom_team_name, bottom_team_points

# Statistics (3 fields)
top_scorer_name, top_scorer_goals, top_scorer_team

# Historical context (3 fields)
previous_season_id, next_season_id, historical_winner

# Additional metadata (13 fields)
typical_matchday, match_frequency, winter_break, prize_money_total, tv_revenue,
attendance_average, broadcast_partners, var_usage, goal_line_technology,
inaugural_season, total_editions, most_successful_team, extracted_at
```

**Usage Example**:
```python
from odds_scraper.items.footystats.season_info_items import (
    SeasonInfoItem, validate_season_info_item, create_season_info_item
)

# Process season info
if validate_season_info_item(api_data):
    item = create_season_info_item(api_data)
    print(f"Season: {item['season_name']}, Competition: {item['competition_name']}")
    print(f"Teams: {item['total_teams']}, Matches: {item['matches_played']}/{item['total_matches']}")
```

## Field Processing Utilities

### Safe Type Conversion Functions
```python
def safe_int(value):
    """Safely convert to integer, returns None for invalid values"""
    try:
        return int(value) if value is not None else None
    except (ValueError, TypeError):
        return None

def safe_float(value):
    """Safely convert to float, returns None for invalid values"""
    try:
        return float(value) if value is not None else None
    except (ValueError, TypeError):
        return None

def clean_string(value):
    """Clean and strip string values"""
    if isinstance(value, str):
        return value.strip()
    return value
```

### Standard Validation Pattern
```python
def validate_*_item(item_data: dict) -> bool:
    """Validate data structure before processing"""
    required_fields = ['id', 'name']  # Adjust per item type
    
    if not isinstance(item_data, dict):
        return False
    
    for field in required_fields:
        if field not in item_data or item_data[field] is None:
            return False
    
    # Additional validation logic
    return True
```

## Data Quality Assurance

### Field Coverage Strategy
Each item is designed with **over-inclusive field coverage** to ensure:
1. **Comprehensive Data Capture** - All possible API fields are mapped
2. **Forward Compatibility** - New API fields won't break existing code
3. **Graceful Degradation** - Missing fields are handled safely
4. **Type Safety** - All fields use appropriate type conversion

### Validation Levels
1. **Structure Validation** - Ensures data is dict with required fields
2. **Type Validation** - Validates critical field types (IDs, counts)
3. **Business Logic Validation** - Checks for logical constraints
4. **Graceful Processing** - Handles missing or invalid optional fields

### Error Handling Pattern
```python
try:
    item = create_*_item(api_data)
    logger.debug(f"Created item: {item.get('name', 'Unknown')}")
    return item
except Exception as e:
    logger.error(f"Error creating item: {e}")
    return None
```

## Integration Guidelines

### Working with Items
```python
# Import pattern
from odds_scraper.items.footystats.{endpoint}_items import (
    {Endpoint}Item,
    validate_{endpoint}_item,
    create_{endpoint}_item
)

# Usage pattern in spiders
if validate_{endpoint}_item(api_data):
    item = create_{endpoint}_item(api_data)
    if item:
        yield item
```

### Custom Field Processing
```python
# Extend ItemLoader for custom processing
class CustomLoader({Endpoint}Loader):
    # Add custom field processors
    custom_field_in = MapCompose(custom_function)
```

### Output Format Consistency
All items produce consistent JSON output with:
- Standardized field names
- Type-safe values
- Metadata fields (extracted_at)
- Null handling for missing data

This ensures compatibility across all FootyStats data processing pipelines.

## DAG and Script Integration Patterns

### Airflow DAG Integration
Items are designed for seamless integration with Airflow orchestration:

```python
# In Airflow DAGs - Task for data extraction
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

def process_scraped_data(task_instance, **context):
    """Process scraped items in Airflow task"""
    import json
    from odds_scraper.items.footystats.league_table_items import (
        validate_league_table_item, create_league_table_item
    )
    
    # Get scraped data from previous task
    scraped_file = context['params']['output_file']
    
    with open(scraped_file, 'r') as f:
        scraped_items = [json.loads(line) for line in f]
    
    processed_items = []
    for item_data in scraped_items:
        if validate_league_table_item(item_data):
            item = create_league_table_item(item_data)
            processed_items.append(dict(item))
    
    # Store processed data
    processed_file = scraped_file.replace('.jsonl', '_processed.jsonl')
    with open(processed_file, 'w') as f:
        for item in processed_items:
            f.write(json.dumps(item) + '\n')
    
    return processed_file

# DAG task definition
extract_task = BashOperator(
    task_id='extract_league_table',
    bash_command='scrapy crawl footystats_league_table -a season_id={{ dag_run.conf.season_id }} -O {{ params.output_file }}',
    dag=dag
)

process_task = PythonOperator(
    task_id='process_league_table',
    python_callable=process_scraped_data,
    dag=dag
)

extract_task >> process_task
```

### Batch Processing Scripts
Items support batch processing for multiple seasons or leagues:

```python
# scripts/batch_process_leagues.py
import json
import subprocess
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from odds_scraper.items.footystats.league_table_items import (
    validate_league_table_item, create_league_table_item
)

def process_league_table(season_id, api_key, output_dir):
    """Process single league table with error handling"""
    try:
        # Run spider
        output_file = f"{output_dir}/league_table_{season_id}.jsonl"
        cmd = [
            'scrapy', 'crawl', 'footystats_league_table',
            '-a', f'season_id={season_id}',
            '-a', f'api_key={api_key}',
            '-O', output_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Process items
            processed_items = []
            with open(output_file, 'r') as f:
                for line in f:
                    item_data = json.loads(line)
                    if validate_league_table_item(item_data):
                        item = create_league_table_item(item_data)
                        processed_items.append(dict(item))
            
            # Save processed data
            processed_file = output_file.replace('.jsonl', '_processed.json')
            with open(processed_file, 'w') as f:
                json.dump(processed_items, f, indent=2)
            
            return {
                'season_id': season_id,
                'status': 'success',
                'items_count': len(processed_items),
                'output_file': processed_file
            }
        else:
            return {
                'season_id': season_id,
                'status': 'error',
                'error': result.stderr
            }
            
    except Exception as e:
        return {
            'season_id': season_id,
            'status': 'error',
            'error': str(e)
        }

def main():
    """Batch process multiple league tables"""
    season_ids = ['1625', '2012', '2790']  # Multiple seasons
    api_key = 'your_api_key'
    output_dir = 'output/league_tables'
    
    # Process in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for season_id in season_ids:
            future = executor.submit(process_league_table, season_id, api_key, output_dir)
            futures.append(future)
        
        results = []
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            
            if result['status'] == 'success':
                print(f"✅ Season {result['season_id']}: {result['items_count']} items")
            else:
                print(f"❌ Season {result['season_id']}: {result['error']}")
    
    return results

if __name__ == '__main__':
    main()
```

### Data Pipeline Integration
Items integrate with data processing pipelines:

```python
# pipelines/footystats_processor.py
import json
import pandas as pd
from typing import List, Dict, Any
from odds_scraper.items.footystats.league_table_items import (
    validate_league_table_item, create_league_table_item
)

class FootyStatsProcessor:
    """Process FootyStats items for analytics pipeline"""
    
    def __init__(self, output_format='json'):
        self.output_format = output_format
        self.processed_items = []
    
    def process_file(self, input_file: str) -> List[Dict[str, Any]]:
        """Process scraped data file"""
        processed = []
        
        with open(input_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    item_data = json.loads(line)
                    
                    if validate_league_table_item(item_data):
                        item = create_league_table_item(item_data)
                        processed.append(dict(item))
                    else:
                        print(f"Invalid item at line {line_num}")
                        
                except json.JSONDecodeError as e:
                    print(f"JSON error at line {line_num}: {e}")
                except Exception as e:
                    print(f"Processing error at line {line_num}: {e}")
        
        self.processed_items.extend(processed)
        return processed
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert processed items to pandas DataFrame"""
        if not self.processed_items:
            return pd.DataFrame()
        
        return pd.DataFrame(self.processed_items)
    
    def save_to_csv(self, output_file: str):
        """Save processed data as CSV"""
        df = self.to_dataframe()
        df.to_csv(output_file, index=False)
    
    def save_to_json(self, output_file: str):
        """Save processed data as JSON"""
        with open(output_file, 'w') as f:
            json.dump(self.processed_items, f, indent=2)

# Usage in data pipeline
processor = FootyStatsProcessor()
processor.process_file('raw_data/league_table.jsonl')
processor.save_to_csv('processed_data/league_table.csv')
processor.save_to_json('processed_data/league_table.json')
```

### Analytics Integration
Items provide structured data for betting analytics:

```python
# analytics/league_analysis.py
from odds_scraper.items.footystats.league_table_items import create_league_table_item
from odds_scraper.items.footystats.btts_stats_items import create_btts_stats_item

def analyze_league_performance(league_table_data, btts_data):
    """Combine league table and BTTS data for analysis"""
    
    # Process league table
    table_items = []
    for team_data in league_table_data:
        item = create_league_table_item(team_data)
        table_items.append(dict(item))
    
    # Process BTTS stats
    btts_item = create_btts_stats_item(btts_data)
    
    # Combine for analysis
    analysis = {
        'league_stats': {
            'total_teams': len(table_items),
            'top_team': max(table_items, key=lambda x: x['points']),
            'bottom_team': min(table_items, key=lambda x: x['points']),
            'avg_goals_per_game': sum(x['goals_for'] for x in table_items) / sum(x['played'] for x in table_items)
        },
        'btts_analysis': {
            'league_btts_percentage': btts_item['btts_percentage'],
            'home_btts_percentage': btts_item['btts_home_percentage'],
            'away_btts_percentage': btts_item['btts_away_percentage']
        }
    }
    
    return analysis
```

## Development Checklist

For each new item development:

### Pre-Development
- [ ] Analyze HTML documentation for field structure
- [ ] Extract and examine JSON sample responses
- [ ] Identify required vs optional fields
- [ ] Map nested objects and array fields
- [ ] Determine appropriate data types

### Development
- [ ] Write failing tests with sample data
- [ ] Create item class with comprehensive field coverage
- [ ] Implement ItemLoader with appropriate processors
- [ ] Create validation function with required field checks
- [ ] Implement creation function with safe field extraction
- [ ] Handle nested objects and arrays properly

### Testing
- [ ] Unit tests for validation function
- [ ] Unit tests for creation function with valid data
- [ ] Error handling tests with invalid/missing data
- [ ] Integration tests with real API responses
- [ ] Type validation tests for all field types

### Integration
- [ ] Test with spider integration
- [ ] Verify DAG integration compatibility
- [ ] Test batch processing scenarios
- [ ] Validate analytics pipeline integration
- [ ] Check error handling in production scenarios

### Documentation
- [ ] Update item field documentation
- [ ] Add usage examples to CLAUDE.md
- [ ] Document any special handling requirements
- [ ] Update integration patterns if needed

This comprehensive approach ensures robust, maintainable items that integrate seamlessly with all platform components.