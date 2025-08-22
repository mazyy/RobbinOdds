name: "FootyStats Comprehensive Endpoint Implementation PRP"
description: |
  Complete implementation of all missing FootyStats API endpoints with spiders and items,
  following established architecture patterns for maximum coverage and efficiency.

---

## Goal

**Feature Goal**: Implement comprehensive FootyStats API coverage by creating spiders and items for all missing endpoints to achieve 100% endpoint coverage with consistent architecture patterns.

**Deliverable**: Complete spider and item implementations for 6 missing FootyStats endpoints: league-table, btts-stats, over-stats, team-last, team-vs-team, and season-info.

**Success Definition**: All FootyStats API endpoints accessible via consistent spider commands with standardized parameter validation, error handling, and data extraction following established codebase patterns.

## User Persona

**Target User**: Data analysts, developers, and betting market researchers

**Use Case**: Comprehensive sports data collection for analysis, requiring access to league standings, betting statistics, team form analysis, and head-to-head historical data

**User Journey**: 
1. Run spider command with standardized parameters
2. Receive validated, structured data in consistent format
3. Use data for betting analysis, performance tracking, or research

**Pain Points Addressed**: 
- Missing critical betting market endpoints (BTTS, Over/Under statistics)
- No access to league standings/tables
- Limited team form analysis capabilities
- Incomplete endpoint coverage gaps

## Why

- **Business Value**: Enables comprehensive betting market analysis and sports data research
- **Integration**: Seamlessly extends existing FootyStats spider architecture without disruption
- **Problem Solving**: Fills critical gaps in league standings, betting statistics, and team performance data
- **Efficiency**: Leverages existing rate limiting and error handling infrastructure

## What

Complete implementation of 6 missing FootyStats endpoints with full spider and item support:

1. **league-table**: League standings with position, points, goal difference
2. **btts-stats**: Both Teams To Score statistics for betting analysis  
3. **over-stats**: Over/Under goal statistics for various thresholds
4. **team-last**: Recent team form analysis (last N games)
5. **team-vs-team**: Head-to-head historical matchup data
6. **season-info**: Season metadata and competition information

### Success Criteria

- [ ] All 6 endpoints implemented with consistent spider/item patterns
- [ ] Parameter validation matches existing FootyStats spider conventions
- [ ] Error handling and rate limiting inherited from FootyStatsBaseSpider
- [ ] Data extraction follows established item loader and field processing patterns
- [ ] All spiders executable via standard `scrapy crawl` commands
- [ ] Comprehensive field coverage for each endpoint's data structure

## All Needed Context

### Context Completeness Check

_This PRP provides complete implementation guidance for someone unfamiliar with the codebase, including exact file patterns, naming conventions, field structures, and validation requirements._

### Documentation & References

```yaml
# MUST READ - Include these in your context window
- url: https://footystats.org/api/documentations/league-teams
  why: Reference API documentation pattern and parameter structure
  critical: Understand parameter requirements and response formats for similar endpoints

- file: scrapers/odds_scraper/odds_scraper/spiders/footystats/base_spider.py
  why: Core architecture pattern with automatic pagination, rate limiting, error handling
  pattern: FootyStatsBaseSpider inheritance with endpoint_name, get_request_params(), parse_data_item()
  gotcha: Must handle both list and single object responses, 2-second rate limiting mandatory

- file: scrapers/odds_scraper/odds_scraper/spiders/footystats/league_teams_spider.py
  why: Example spider implementation pattern for list-based endpoints
  pattern: Parameter validation in __init__, get_request_params() structure, parse_data_item() implementation
  gotcha: Required parameters must be validated in spider __init__, not base class

- file: scrapers/odds_scraper/odds_scraper/items/footystats/league_teams_items.py
  why: Complete item implementation pattern with validation and creation functions
  pattern: Item class, ItemLoader, validation function, creation function, utility functions
  gotcha: All items must include extracted_at field, use safe_int/safe_float for type conversion

- file: scrapers/odds_scraper/odds_scraper/spiders/footystats/today_spider.py
  why: Example of endpoint with optional parameters and date handling
  pattern: Optional parameter handling, date formatting, timezone support
  gotcha: Optional parameters must default to None and conditionally added to request params

- file: scrapers/odds_scraper/odds_scraper/items/footystats/team_items.py
  why: Example of complex item with 700+ fields and nested data structures
  pattern: Large field sets with logical grouping, dynamic field mapping for comprehensive coverage
  gotcha: Use section comments for field organization, handle nested objects with separate item classes
```

### Current Codebase Structure

```bash
scrapers/odds_scraper/odds_scraper/
├── spiders/footystats/
│   ├── base_spider.py                    # Core architecture pattern
│   ├── country_list_spider.py           # ✅ Implemented
│   ├── league_list_spider.py            # ✅ Implemented  
│   ├── league_matches_spider.py         # ✅ Implemented
│   ├── league_stats_spider.py           # ✅ Implemented
│   ├── league_teams_spider.py           # ✅ Implemented
│   ├── league_players_spider.py         # ✅ Implemented
│   ├── league_referees_spider.py        # ✅ Implemented
│   ├── match_details_spider.py          # ✅ Implemented
│   ├── team_spider.py                   # ✅ Implemented
│   ├── player_spider.py                 # ✅ Implemented
│   ├── referee_spider.py                # ✅ Implemented
│   └── today_spider.py                  # ✅ Implemented
└── items/footystats/
    ├── country_list_items.py            # ✅ Implemented
    ├── league_list_items.py             # ✅ Implemented
    ├── league_matches_items.py          # ✅ Implemented (300+ fields)
    ├── league_stats_items.py            # ✅ Implemented
    ├── league_teams_items.py            # ✅ Implemented
    ├── league_players_items.py          # ✅ Implemented
    ├── league_referees_items.py         # ✅ Implemented
    ├── match_details_items.py           # ✅ Implemented
    ├── team_items.py                    # ✅ Implemented (700+ fields)
    ├── player_items.py                  # ✅ Implemented
    ├── referee_items.py                 # ✅ Implemented
    └── today_items.py                   # ✅ Implemented
```

### Desired Codebase Structure with New Files

```bash
scrapers/odds_scraper/odds_scraper/
├── spiders/footystats/
│   ├── league_table_spider.py           # 🆕 NEW - League standings
│   ├── btts_stats_spider.py             # 🆕 NEW - BTTS statistics
│   ├── over_stats_spider.py             # 🆕 NEW - Over/Under statistics  
│   ├── team_last_spider.py              # 🆕 NEW - Recent team form
│   ├── team_vs_team_spider.py           # 🆕 NEW - Head-to-head data
│   └── season_info_spider.py            # 🆕 NEW - Season metadata
└── items/footystats/
    ├── league_table_items.py            # 🆕 NEW - League table item structure
    ├── btts_stats_items.py              # 🆕 NEW - BTTS statistics structure
    ├── over_stats_items.py              # 🆕 NEW - Over/Under statistics structure
    ├── team_last_items.py               # 🆕 NEW - Team form structure
    ├── team_vs_team_items.py            # 🆕 NEW - H2H matchup structure
    └── season_info_items.py             # 🆕 NEW - Season info structure
```

### Known Gotchas & Library Quirks

```python
# CRITICAL: FootyStats API constraints
# Rate limiting: 2-second delays mandatory, 1800 req/hour limit
# Authentication: api_key parameter required, "example" for testing
# Response formats: Both {"data": [...]} and {"data": {...}} patterns

# CRITICAL: Scrapy ItemLoader patterns
# default_input_processor = MapCompose(clean_string)  # Clean all strings
# default_output_processor = TakeFirst()              # Single values from lists
# Array fields MUST use Identity() output processor

# CRITICAL: Parameter validation requirements
# Required parameters validated in spider.__init__() with ValueError
# Optional parameters default to None, conditionally added to request params
# Base spider handles pagination automatically for list responses only

# CRITICAL: Field processing patterns  
# Integer fields: MapCompose(safe_int) input processor
# Float fields: MapCompose(safe_float) input processor
# Timestamp fields: MapCompose(convert_unix_timestamp) input processor
# extracted_at: ALWAYS MapCompose(lambda x: datetime.now()) input processor
```

## Implementation Blueprint

### Data Models and Structure

Create comprehensive data models ensuring type safety and consistency with existing patterns:

```python
# League Table Item Structure
class LeagueTableItem(Item):
    # Basic information
    id = Field()                          # Team ID
    position = Field()                    # League position
    team_name = Field()                   # Team name
    played = Field()                      # Games played
    wins = Field()                        # Wins
    draws = Field()                       # Draws  
    losses = Field()                      # Losses
    goals_for = Field()                   # Goals scored
    goals_against = Field()               # Goals conceded
    goal_difference = Field()             # Goal difference
    points = Field()                      # Total points
    form = Field()                        # Recent form (W-D-L)
    extracted_at = Field()                # Extraction timestamp

# BTTS Statistics Item Structure  
class BttsStatsItem(Item):
    # League identification
    season_id = Field()                   # Season identifier
    league_name = Field()                 # League name
    # BTTS statistics
    total_matches = Field()               # Total matches played
    btts_matches = Field()                # Matches with BTTS
    btts_percentage = Field()             # BTTS percentage
    no_btts_matches = Field()             # Matches without BTTS
    no_btts_percentage = Field()          # No BTTS percentage
    extracted_at = Field()                # Extraction timestamp

# Over/Under Statistics Item Structure
class OverStatsItem(Item):
    # League identification  
    season_id = Field()                   # Season identifier
    league_name = Field()                 # League name
    # Over/Under thresholds
    over_15_matches = Field()             # Matches over 1.5 goals
    over_15_percentage = Field()          # Over 1.5 percentage
    over_25_matches = Field()             # Matches over 2.5 goals
    over_25_percentage = Field()          # Over 2.5 percentage
    over_35_matches = Field()             # Matches over 3.5 goals
    over_35_percentage = Field()          # Over 3.5 percentage
    extracted_at = Field()                # Extraction timestamp
```

### Implementation Tasks (ordered by dependencies)

```yaml
Task 1: CREATE scrapers/odds_scraper/odds_scraper/items/footystats/league_table_items.py
  - IMPLEMENT: LeagueTableItem with position, points, goal difference fields
  - FOLLOW pattern: items/footystats/league_teams_items.py (item structure, field processing)
  - NAMING: LeagueTableItem class, LeagueTableLoader, validate_league_table_item, create_league_table_item
  - PLACEMENT: FootyStats items directory
  - DEPENDENCIES: Standard utility functions (clean_string, safe_int, safe_float)

Task 2: CREATE scrapers/odds_scraper/odds_scraper/spiders/footystats/league_table_spider.py
  - IMPLEMENT: LeagueTableSpider inheriting from FootyStatsBaseSpider
  - FOLLOW pattern: spiders/footystats/league_teams_spider.py (spider structure, parameter handling)
  - NAMING: LeagueTableSpider class, name="footystats_league_table", endpoint_name="league-table"
  - DEPENDENCIES: Import LeagueTableItem from Task 1, inherit from FootyStatsBaseSpider
  - PLACEMENT: FootyStats spiders directory

Task 3: CREATE scrapers/odds_scraper/odds_scraper/items/footystats/btts_stats_items.py
  - IMPLEMENT: BttsStatsItem with BTTS percentage and match count fields
  - FOLLOW pattern: items/footystats/league_stats_items.py (statistics structure)
  - NAMING: BttsStatsItem class, BttsStatsLoader, validate_btts_stats_item, create_btts_stats_item
  - PLACEMENT: FootyStats items directory
  - DEPENDENCIES: Standard utility functions for percentage and count processing

Task 4: CREATE scrapers/odds_scraper/odds_scraper/spiders/footystats/btts_stats_spider.py
  - IMPLEMENT: BttsStatsSpider with season_id parameter validation
  - FOLLOW pattern: spiders/footystats/league_stats_spider.py (season-based endpoint)
  - NAMING: BttsStatsSpider class, name="footystats_btts_stats", endpoint_name="btts-stats"
  - DEPENDENCIES: Import BttsStatsItem from Task 3, inherit from FootyStatsBaseSpider
  - PLACEMENT: FootyStats spiders directory

Task 5: CREATE scrapers/odds_scraper/odds_scraper/items/footystats/over_stats_items.py
  - IMPLEMENT: OverStatsItem with over/under threshold statistics
  - FOLLOW pattern: items/footystats/btts_stats_items.py (similar betting statistics structure)
  - NAMING: OverStatsItem class, OverStatsLoader, validate_over_stats_item, create_over_stats_item
  - PLACEMENT: FootyStats items directory
  - DEPENDENCIES: Standard utility functions for percentage processing

Task 6: CREATE scrapers/odds_scraper/odds_scraper/spiders/footystats/over_stats_spider.py
  - IMPLEMENT: OverStatsSpider with season_id and optional threshold parameters
  - FOLLOW pattern: spiders/footystats/btts_stats_spider.py (betting statistics endpoint)
  - NAMING: OverStatsSpider class, name="footystats_over_stats", endpoint_name="over-stats"
  - DEPENDENCIES: Import OverStatsItem from Task 5, inherit from FootyStatsBaseSpider
  - PLACEMENT: FootyStats spiders directory

Task 7: CREATE scrapers/odds_scraper/odds_scraper/items/footystats/team_last_items.py
  - IMPLEMENT: TeamLastItem with recent form statistics and averages
  - FOLLOW pattern: items/footystats/team_items.py (team-based statistics structure)
  - NAMING: TeamLastItem class, TeamLastLoader, validate_team_last_item, create_team_last_item
  - PLACEMENT: FootyStats items directory
  - DEPENDENCIES: Standard utility functions for averages and form data

Task 8: CREATE scrapers/odds_scraper/odds_scraper/spiders/footystats/team_last_spider.py
  - IMPLEMENT: TeamLastSpider with team_id and games count parameters
  - FOLLOW pattern: spiders/footystats/team_spider.py (team-based endpoint with required team_id)
  - NAMING: TeamLastSpider class, name="footystats_team_last", endpoint_name="team-last"
  - DEPENDENCIES: Import TeamLastItem from Task 7, inherit from FootyStatsBaseSpider
  - PLACEMENT: FootyStats spiders directory

Task 9: CREATE scrapers/odds_scraper/odds_scraper/items/footystats/team_vs_team_items.py
  - IMPLEMENT: TeamVsTeamItem with head-to-head historical match data
  - FOLLOW pattern: items/footystats/match_details_items.py (match-based data structure)
  - NAMING: TeamVsTeamItem class, TeamVsTeamLoader, validate_team_vs_team_item, create_team_vs_team_item
  - PLACEMENT: FootyStats items directory
  - DEPENDENCIES: Standard utility functions for match data processing

Task 10: CREATE scrapers/odds_scraper/odds_scraper/spiders/footystats/team_vs_team_spider.py
  - IMPLEMENT: TeamVsTeamSpider with home_id and away_id parameters
  - FOLLOW pattern: spiders/footystats/match_details_spider.py (dual-parameter endpoint)
  - NAMING: TeamVsTeamSpider class, name="footystats_team_vs_team", endpoint_name="team-vs-team"
  - DEPENDENCIES: Import TeamVsTeamItem from Task 9, inherit from FootyStatsBaseSpider
  - PLACEMENT: FootyStats spiders directory

Task 11: CREATE scrapers/odds_scraper/odds_scraper/items/footystats/season_info_items.py
  - IMPLEMENT: SeasonInfoItem with season metadata and competition details
  - FOLLOW pattern: items/footystats/league_list_items.py (metadata structure)
  - NAMING: SeasonInfoItem class, SeasonInfoLoader, validate_season_info_item, create_season_info_item
  - PLACEMENT: FootyStats items directory
  - DEPENDENCIES: Standard utility functions for date and metadata processing

Task 12: CREATE scrapers/odds_scraper/odds_scraper/spiders/footystats/season_info_spider.py
  - IMPLEMENT: SeasonInfoSpider with season_id parameter
  - FOLLOW pattern: spiders/footystats/league_stats_spider.py (season-based metadata endpoint)
  - NAMING: SeasonInfoSpider class, name="footystats_season_info", endpoint_name="season-info"
  - DEPENDENCIES: Import SeasonInfoItem from Task 11, inherit from FootyStatsBaseSpider
  - PLACEMENT: FootyStats spiders directory
```

### Implementation Patterns & Key Details

```python
# Standard Spider Pattern (use for ALL new spiders)
from typing import Dict, Any, Optional
from .base_spider import FootyStatsBaseSpider
from ...items.footystats.{endpoint}_items import (
    {Endpoint}Item,
    validate_{endpoint}_item,
    create_{endpoint}_item
)

class {Endpoint}Spider(FootyStatsBaseSpider):
    """Spider for FootyStats /{endpoint-name} endpoint"""
    
    name = "footystats_{endpoint}"
    endpoint_name = "{endpoint-name}"  # CRITICAL: Must match exact API path
    allowed_domains = ["api.football-data-api.com"]
    
    def __init__(self, api_key: str = "example", season_id: str = None, **kwargs):
        super().__init__(api_key=api_key, **kwargs)
        
        # PATTERN: Required parameter validation in __init__
        if not season_id:
            raise ValueError("season_id parameter is required")
        self.season_id = season_id
    
    def get_request_params(self) -> Dict[str, Any]:
        """Build request parameters for {endpoint-name} endpoint"""
        params = {"season_id": self.season_id}
        # PATTERN: Conditionally add optional parameters
        return params
    
    def parse_data_item(self, item_data: Dict[str, Any]) -> Optional[{Endpoint}Item]:
        """Parse individual item from API response"""
        if not validate_{endpoint}_item(item_data):
            self.logger.warning(f"Invalid {endpoint} data: {item_data}")
            return None
            
        try:
            item = create_{endpoint}_item(item_data)
            self.logger.debug(f"Created {endpoint} item: {item.get('id', 'N/A')}")
            return item
        except Exception as e:
            self.logger.error(f"Error creating {endpoint} item: {e}")
            return None

# Standard Item Pattern (use for ALL new items)
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

class {Endpoint}Item(Item):
    """Item for {description} from /{endpoint-name} endpoint"""
    
    # PATTERN: Always include basic fields
    id = Field()                        # Primary identifier
    extracted_at = Field()              # Extraction timestamp
    
    # PATTERN: Group fields logically with comments
    # Add endpoint-specific fields here

class {Endpoint}Loader(ItemLoader):
    """Item loader for {endpoint} data"""
    
    default_item_class = {Endpoint}Item
    default_input_processor = MapCompose(clean_string)
    default_output_processor = TakeFirst()
    
    # PATTERN: Type-specific processors
    id_in = MapCompose(safe_int)
    extracted_at_in = MapCompose(lambda x: datetime.now())

def validate_{endpoint}_item(item_data: dict) -> bool:
    """Validate {endpoint} data structure before processing"""
    required_fields = ['id']  # Adjust based on endpoint
    
    if not isinstance(item_data, dict):
        return False
    
    for field in required_fields:
        if field not in item_data or not item_data[field]:
            return False
    
    return True

def create_{endpoint}_item(item_data: dict) -> {Endpoint}Item:
    """Create {endpoint} item from API data"""
    loader = {Endpoint}Loader()
    
    # PATTERN: Basic fields first
    loader.add_value('id', item_data.get('id'))
    
    # PATTERN: Endpoint-specific fields
    # Add field mappings here
    
    # PATTERN: Metadata last
    loader.add_value('extracted_at', None)
    
    return loader.load_item()

# CRITICAL: Parameter patterns by endpoint type
# Season-based endpoints: season_id (required)
# Team-based endpoints: team_id (required), season_id (optional)
# Dual-team endpoints: home_id, away_id (both required)
# Metadata endpoints: Various required parameters
```

### Integration Points

```yaml
SPIDER_REGISTRATION:
  - location: "Automatic via Scrapy spider discovery"
  - pattern: "Spider name must follow footystats_{endpoint} pattern"
  - command: "scrapy crawl footystats_{endpoint} -a api_key=example -a param=value"

RATE_LIMITING:
  - inherited: "From FootyStatsBaseSpider"
  - settings: "2-second delays, auto-throttle enabled"
  - quota: "1800 requests/hour shared across all spiders"

ERROR_HANDLING:
  - inherited: "Comprehensive HTTP status handling"
  - validation: "Per-item validation with graceful failure"
  - logging: "Debug for success, warning for invalid items, error for exceptions"
```

## Validation Loop

### Level 1: Syntax & Style (Immediate Feedback)

```bash
# Run after each file creation - fix before proceeding
cd scrapers/odds_scraper

# Validate Python syntax
python -m py_compile odds_scraper/spiders/footystats/{new_spider}.py
python -m py_compile odds_scraper/items/footystats/{new_item}.py

# Check imports and basic structure
python -c "from odds_scraper.spiders.footystats.{new_spider} import {NewSpider}Spider; print('Spider import successful')"
python -c "from odds_scraper.items.footystats.{new_item} import {NewItem}Item; print('Item import successful')"

# Expected: No syntax errors, successful imports
```

### Level 2: Spider Functionality (Component Validation)

```bash
# Test spider parameter validation
scrapy crawl footystats_{endpoint} -a api_key=example -a season_id=1625 -L DEBUG

# Test spider with invalid parameters (should fail gracefully)
scrapy crawl footystats_{endpoint} -a api_key=example -L DEBUG

# Test spider with example data (EPL 2018/2019)
scrapy crawl footystats_{endpoint} -a api_key=example -a season_id=1625 -O test_output.json

# Expected: Proper parameter validation, successful data extraction, structured JSON output
```

### Level 3: Integration Testing (System Validation)

```bash
# Test all new spiders together
scrapy list | grep footystats

# Verify spider registration and naming
scrapy crawl footystats_league_table -a api_key=example -a season_id=1625 -O league_table.json
scrapy crawl footystats_btts_stats -a api_key=example -a season_id=1625 -O btts_stats.json
scrapy crawl footystats_over_stats -a api_key=example -a season_id=1625 -O over_stats.json
scrapy crawl footystats_team_last -a api_key=example -a team_id=2 -a games=5 -O team_last.json
scrapy crawl footystats_team_vs_team -a api_key=example -a home_id=2 -a away_id=6 -O h2h.json
scrapy crawl footystats_season_info -a api_key=example -a season_id=1625 -O season_info.json

# Validate output structure and content
jq '.[]' league_table.json | head -5
jq '.[]' btts_stats.json | head -5

# Expected: All spiders execute successfully, structured JSON output, valid data extraction
```

### Level 4: Data Quality & Coverage Validation

```bash
# Validate data completeness
python -c "
import json
with open('league_table.json') as f:
    data = json.load(f)
    print(f'League table entries: {len(data)}')
    if data:
        print(f'Sample fields: {list(data[0].keys())}')
"

# Test rate limiting and quota usage
scrapy crawl footystats_league_table -a api_key=example -a season_id=1625 -L INFO | grep -i "requests"

# Validate against established patterns
python -c "
from odds_scraper.items.footystats.league_table_items import validate_league_table_item
print('Validation function working:', validate_league_table_item({'id': 1, 'position': 1}))
"

# Expected: Data completeness verification, proper rate limiting, validation functions working
```

## Final Validation Checklist

### Technical Validation

- [ ] All 12 tasks completed successfully (6 spiders + 6 items)
- [ ] All spiders inherit from FootyStatsBaseSpider correctly
- [ ] All items follow established field and loader patterns
- [ ] Parameter validation working in all spider `__init__` methods
- [ ] Error handling and logging following established patterns

### Feature Validation

- [ ] All 6 missing endpoints accessible via spider commands
- [ ] League table spider extracts position, points, goal difference data
- [ ] BTTS stats spider extracts percentage and match count data
- [ ] Over/Under stats spider extracts threshold statistics
- [ ] Team form spider extracts recent performance data
- [ ] Head-to-head spider extracts historical matchup data
- [ ] Season info spider extracts metadata and competition details

### Code Quality Validation

- [ ] Naming conventions match existing FootyStats spiders exactly
- [ ] File placement follows established directory structure
- [ ] Import statements and dependencies correctly configured
- [ ] Field processing uses standard utility functions (safe_int, safe_float, etc.)
- [ ] All items include `extracted_at` field with datetime.now() processor

### Integration Validation

- [ ] All spiders discoverable via `scrapy list` command
- [ ] Rate limiting inherited from base spider (2-second delays)
- [ ] Error handling graceful for invalid parameters and bad responses
- [ ] Data extraction produces structured JSON output
- [ ] Validation functions prevent invalid data processing

---

## Anti-Patterns to Avoid

- ❌ Don't create custom base classes - use existing FootyStatsBaseSpider
- ❌ Don't modify existing spider files - create new files only
- ❌ Don't skip parameter validation in spider `__init__` methods
- ❌ Don't use hardcoded values - follow parameter pattern from existing spiders
- ❌ Don't ignore rate limiting - inherit from FootyStatsBaseSpider for automatic handling
- ❌ Don't create custom utility functions - use existing safe_int, safe_float, clean_string
- ❌ Don't modify endpoint names - use exact API path as endpoint_name
- ❌ Don't skip field comments - document all fields inline for maintainability