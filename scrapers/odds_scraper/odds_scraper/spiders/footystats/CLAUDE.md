# FootyStats Spiders - CLAUDE.md

This file provides comprehensive guidance for working with FootyStats API spiders, development workflows, testing procedures, and integration patterns.

## Overview

FootyStats spiders extract comprehensive football/soccer data from the FootyStats API. All spiders inherit from `FootyStatsBaseSpider` which provides automatic pagination, rate limiting (2-second delays), error handling, and request statistics tracking.

## Development Philosophy

### API-First Architecture
FootyStats spiders work with structured JSON API responses, not HTML scraping:
- Clean JSON data reduces parsing complexity
- Structured responses enable comprehensive field mapping
- API rate limiting is handled automatically
- Error handling focuses on API status codes and data validation

### Comprehensive Field Coverage
Each item captures **all available fields** from API responses:
- Forward compatibility with API changes
- Rich data for analytics and betting strategies
- Type-safe field processing with validation
- Graceful handling of missing/null values

## Development Workflow

### 1. HTML Documentation Collection
Before developing any spider, collect HTML documentation from FootyStats API:

```bash
# Navigate to FootyStats API documentation page
# Example: https://footystats.org/api/documentations/league-table

# Open scrapy shell to save documentation
scrapy shell "https://footystats.org/api/documentations/your-endpoint"

# In shell, save HTML documentation:
>>> with open('scrapers/tests/resources/footystats/your_endpoint_api_documentations.html', 'wb') as f:
...     f.write(response.body)
>>> print("Documentation saved successfully")
```

### 2. JSON Sample Response Extraction
Extract sample API responses for testing:

```bash
# Method 1: From documentation HTML
# Look for embedded JSON examples in documentation
# Copy them to sample_responses.json

# Method 2: Live API testing
scrapy shell "https://api.football-data-api.com/your-endpoint?key=example&param=value"

# In shell, extract and save JSON:
>>> import json
>>> data = json.loads(response.text)
>>> sample = {
...     "your_endpoint": {
...         "endpoint": "https://api.football-data-api.com/your-endpoint",
...         "parameters": {"key": "example", "your_param": "value"},
...         "response": data.get('data', [])
...     }
... }
>>> with open('scrapers/tests/resources/footystats/sample_responses.json', 'r+') as f:
...     existing = json.load(f)
...     existing.update(sample)
...     f.seek(0)
...     json.dump(existing, f, indent=2)
...     f.truncate()
```

### 3. Test-Driven Development (TDD) Workflow

#### Step 1: Create Test Contract
```bash
# Create test file: scrapers/tests/contracts/test_footystats_your_endpoint.py
touch scrapers/tests/contracts/test_footystats_your_endpoint.py
```

#### Step 2: Write Failing Tests
```python
# Example test structure
class TestFootyStatsYourEndpointSpider(FootyStatsTestBase):
    def test_spider_initialization(self, spider):
        """Test spider initializes with correct parameters"""
        assert spider.your_param == 'expected_value'
        assert spider.api_key == 'test_key'
    
    def test_parse_response_data(self, spider, mock_response):
        """Test extraction of data from API response"""
        items = list(spider.parse(mock_response))
        assert len(items) > 0
        # Add specific field assertions
```

#### Step 3: Run Tests (Should Fail)
```bash
# Run specific test
pytest scrapers/tests/contracts/test_footystats_your_endpoint.py -v

# Expected: ImportError or NotImplementedError
```

#### Step 4: Create Item Structure
```bash
# Create item file: scrapers/odds_scraper/odds_scraper/items/footystats/your_endpoint_items.py
touch scrapers/odds_scraper/odds_scraper/items/footystats/your_endpoint_items.py
```

#### Step 5: Create Spider Implementation
```bash
# Create spider file: scrapers/odds_scraper/odds_scraper/spiders/footystats/your_endpoint_spider.py
touch scrapers/odds_scraper/odds_scraper/spiders/footystats/your_endpoint_spider.py
```

#### Step 6: Implement and Iterate
```bash
# Run tests repeatedly until they pass
pytest scrapers/tests/contracts/test_footystats_your_endpoint.py -v

# Test spider functionality
scrapy crawl footystats_your_endpoint -a api_key=example -a your_param=test_value
```

### 4. HTML Sample Workflow for Future Development

#### Storing HTML Documentation
```
scrapers/tests/resources/footystats/
├── api_documentations.html                    # Main API documentation
├── your_endpoint_api_documentations.html      # Specific endpoint docs
├── sample_responses.json                      # JSON sample responses
└── [endpoint]_api_documentations.html         # Other endpoint docs
```

#### Using HTML Samples for Development
1. **Reference for Field Mapping**: HTML docs show all available fields
2. **Parameter Documentation**: Shows required and optional parameters
3. **Response Structure**: Understanding nested objects and arrays
4. **Error Response Examples**: How API behaves with invalid requests

#### Sample Response JSON Structure
```json
{
  "your_endpoint": {
    "endpoint": "https://api.football-data-api.com/your-endpoint",
    "parameters": {
      "key": "example",
      "required_param": "value",
      "optional_param": "value"
    },
    "response": [
      {
        "id": 123,
        "name": "Sample Data",
        "field1": "value1",
        "field2": 42,
        "nested_object": {
          "sub_field": "sub_value"
        }
      }
    ]
  }
}
```

### 5. Testing Workflow

#### Unit Testing
```bash
# Test individual spider functionality
pytest scrapers/tests/contracts/test_footystats_your_endpoint.py::TestClass::test_method -v

# Test with coverage
pytest scrapers/tests/contracts/ --cov=scrapers/odds_scraper/odds_scraper/spiders/footystats
```

#### Integration Testing
```bash
# Test with real API (limited)
scrapy crawl footystats_your_endpoint -a api_key=example -a param=value -L DEBUG

# Test with production key (careful with rate limits)
scrapy crawl footystats_your_endpoint -a api_key=your_real_key -a param=value -O test_output.json
```

#### Contract Testing
```bash
# Use Scrapy's built-in contract testing
scrapy check footystats_your_endpoint

# Check all FootyStats spiders
scrapy check | grep footystats
```

### 6. Spider Implementation Template

```python
from .base_spider import FootyStatsBaseSpider
from odds_scraper.items.footystats.your_endpoint_items import (
    create_your_endpoint_item, validate_your_endpoint_item
)

class FootyStatsYourEndpointSpider(FootyStatsBaseSpider):
    name = 'footystats_your_endpoint'
    endpoint_name = 'your-endpoint'
    
    def __init__(self, your_param: str = None, **kwargs):
        super().__init__(**kwargs)
        
        if not your_param:
            raise ValueError("your_param is required")
        
        self.your_param = your_param
        self.logger.info(f"Initialized with your_param: {your_param}")
    
    def get_request_params(self) -> dict:
        return {
            'your_param': self.your_param,
            # Add other parameters
        }
    
    def parse_data_item(self, item_data: dict):
        """Parse individual data item from API response"""
        if not validate_your_endpoint_item(item_data):
            self.logger.warning(f"Invalid item data: {item_data}")
            return None
        
        try:
            return create_your_endpoint_item(item_data)
        except Exception as e:
            self.logger.error(f"Error creating item: {e}")
            return None
```

### 7. Integration with DAGs and Scripts

The comprehensive documentation enables:

#### Airflow DAG Integration
```python
# In Airflow DAGs
from airflow.operators.bash import BashOperator

run_spider = BashOperator(
    task_id='run_footystats_your_endpoint',
    bash_command='scrapy crawl footystats_your_endpoint -a api_key={{ var.value.footystats_api_key }} -a your_param={{ dag_run.conf.your_param }} -O {{ params.output_path }}',
    dag=dag
)
```

#### Batch Processing Scripts
```python
import subprocess
import json

def run_footystats_spider(endpoint, params, output_file):
    """Run FootyStats spider with parameters"""
    cmd = [
        'scrapy', 'crawl', f'footystats_{endpoint}',
        '-a', f'api_key={params["api_key"]}',
        '-O', output_file
    ]
    
    # Add endpoint-specific parameters
    for param, value in params.items():
        if param != 'api_key':
            cmd.extend(['-a', f'{param}={value}'])
    
    return subprocess.run(cmd, capture_output=True, text=True)
```

## Available Spiders

### Core Spiders (Existing)
- `footystats_country_list` - List of available countries
- `footystats_league_list` - Leagues in a specific country  
- `footystats_league_matches` - Matches in a league season
- `footystats_league_stats` - League statistics
- `footystats_league_teams` - Teams in a league with comprehensive stats
- `footystats_league_players` - Players in a league
- `footystats_league_referees` - Referees in a league
- `footystats_match_details` - Detailed match information
- `footystats_team` - Individual team data
- `footystats_player` - Individual player data
- `footystats_referee` - Individual referee data
- `footystats_today` - Today's matches

### New Comprehensive Spiders
- `footystats_league_table` - League standings and table positions
- `footystats_btts_stats` - Both Teams To Score statistics
- `footystats_over_stats` - Over/Under goal statistics  
- `footystats_team_last` - Recent team form analysis
- `footystats_team_vs_team` - Head-to-head team statistics
- `footystats_season_info` - Season metadata and information

## Spider Usage Patterns

### Basic Command Structure
```bash
scrapy crawl <spider_name> -a api_key=<key> [additional_parameters] [output_options]
```

### Authentication
All spiders require an API key:
- **Production**: Use your FootyStats API key
- **Testing**: Use `api_key=example` (limited functionality)

### Output Options
```bash
# Save to JSON file
-O output.json

# Save to CSV file  
-O output.csv

# Print to console (default)
# No additional parameters needed
```

## Individual Spider Documentation

### 1. League Table Spider (`footystats_league_table`)

**Purpose**: Extract league standings with positions, points, and goal statistics.

**Required Parameters**:
- `season_id` - Season identifier (e.g., "1625" for EPL 2018/2019)

**Optional Parameters**: None

**Usage Examples**:
```bash
# Basic usage
scrapy crawl footystats_league_table -a api_key=example -a season_id=1625

# Save to file
scrapy crawl footystats_league_table -a api_key=your_key -a season_id=2012 -O table.json

# Debug mode
scrapy crawl footystats_league_table -a api_key=example -a season_id=1625 -L DEBUG
```

**Data Output**: League table with team positions, points, wins/draws/losses, goals for/against, goal difference, form, and venue-specific statistics.

---

### 2. BTTS Statistics Spider (`footystats_btts_stats`)

**Purpose**: Extract Both Teams To Score statistics for betting analysis.

**Required Parameters**:
- `season_id` - Season identifier

**Optional Parameters**: None

**Usage Examples**:
```bash
# Basic usage
scrapy crawl footystats_btts_stats -a api_key=example -a season_id=1625

# Production usage
scrapy crawl footystats_btts_stats -a api_key=your_key -a season_id=2012 -O btts.json
```

**Data Output**: BTTS match counts and percentages, venue breakdown (home/away), timing analysis (first half, second half), goal threshold combinations, and recent form patterns.

---

### 3. Over/Under Statistics Spider (`footystats_over_stats`)

**Purpose**: Extract Over/Under goal statistics for various thresholds.

**Required Parameters**:
- `season_id` - Season identifier

**Optional Parameters**:
- `threshold` - Specific goal threshold to focus on (e.g., "2.5")

**Usage Examples**:
```bash
# All thresholds
scrapy crawl footystats_over_stats -a api_key=example -a season_id=1625

# Focus on 2.5 goals
scrapy crawl footystats_over_stats -a api_key=example -a season_id=1625 -a threshold=2.5

# Save comprehensive data
scrapy crawl footystats_over_stats -a api_key=your_key -a season_id=2012 -O over_under.json
```

**Data Output**: Over/Under match counts and percentages for thresholds 0.5-5.5 goals, venue breakdown, first/second half analysis, goal averages, and streak patterns.

---

### 4. Team Recent Form Spider (`footystats_team_last`)

**Purpose**: Analyze recent team performance over last N games.

**Required Parameters**:
- `team_id` - Team identifier (e.g., "2" for Arsenal)

**Optional Parameters**:
- `games` - Number of recent games to analyze (default: "5")

**Usage Examples**:
```bash
# Last 5 games (default)
scrapy crawl footystats_team_last -a api_key=example -a team_id=2

# Last 10 games
scrapy crawl footystats_team_last -a api_key=example -a team_id=2 -a games=10

# Analysis for multiple teams
scrapy crawl footystats_team_last -a api_key=your_key -a team_id=6 -a games=8 -O chelsea_form.json
```

**Data Output**: Win/draw/loss record, goal statistics, home/away form breakdown, BTTS and over/under performance, opposition quality metrics, and current streak information.

---

### 5. Head-to-Head Spider (`footystats_team_vs_team`)

**Purpose**: Extract historical matchup data between two specific teams.

**Required Parameters**:
- `home_id` - Home team identifier
- `away_id` - Away team identifier (must be different from home_id)

**Optional Parameters**: None

**Usage Examples**:
```bash
# Arsenal vs Chelsea
scrapy crawl footystats_team_vs_team -a api_key=example -a home_id=2 -a away_id=6

# Liverpool vs Manchester United  
scrapy crawl footystats_team_vs_team -a api_key=your_key -a home_id=3 -a away_id=1 -O h2h.json
```

**Data Output**: Historical win/draw/loss record, goal statistics, venue breakdown (home/away/neutral), competition analysis (league/cup), recent form, BTTS and over/under patterns, and match significance metrics.

---

### 6. Season Information Spider (`footystats_season_info`)

**Purpose**: Extract comprehensive season metadata and competition details.

**Required Parameters**:
- `season_id` - Season identifier

**Optional Parameters**: None

**Usage Examples**:
```bash
# Basic season info
scrapy crawl footystats_season_info -a api_key=example -a season_id=1625

# Comprehensive metadata
scrapy crawl footystats_season_info -a api_key=your_key -a season_id=2012 -O season_meta.json
```

**Data Output**: Season timeline, competition structure, points system, promotion/relegation rules, current leaders, statistical summaries, and historical context.

## Data Flow Architecture

### 1. Request Flow
```
Spider Command → Parameter Validation → FootyStatsBaseSpider → API Request → Response Processing
```

### 2. Data Processing Flow
```
API Response → JSON Validation → Item Creation → Field Processing → Data Validation → Output
```

### 3. Error Handling Flow
```
API Error → Base Spider Handler → Retry Logic → Graceful Failure → Logging
```

## Common Usage Patterns

### Batch Processing
```bash
# Process multiple seasons
for season in 1625 2012 2790; do
    scrapy crawl footystats_league_table -a api_key=your_key -a season_id=$season -O table_$season.json
done

# Process team form for multiple teams
for team in 2 6 3 1; do
    scrapy crawl footystats_team_last -a api_key=your_key -a team_id=$team -a games=10 -O team_$team_form.json
done
```

### Data Pipeline Integration
```bash
# Extract league table and team stats together
scrapy crawl footystats_league_table -a api_key=your_key -a season_id=1625 -O current_table.json
scrapy crawl footystats_btts_stats -a api_key=your_key -a season_id=1625 -O btts_analysis.json
scrapy crawl footystats_over_stats -a api_key=your_key -a season_id=1625 -O goal_analysis.json
```

## Rate Limiting and Best Practices

### Automatic Rate Limiting
- All spiders inherit 2-second delays between requests
- 1800 requests/hour API limit shared across all spiders
- Auto-throttle enabled for optimal performance

### Best Practices
```bash
# Monitor API usage with INFO logging
scrapy crawl footystats_league_table -a api_key=your_key -a season_id=1625 -L INFO

# Use DEBUG for troubleshooting
scrapy crawl footystats_team_vs_team -a api_key=example -a home_id=2 -a away_id=6 -L DEBUG

# Always specify output for production
scrapy crawl footystats_over_stats -a api_key=your_key -a season_id=2012 -O production_data.json
```

## Error Handling

### Common Error Scenarios
1. **Missing Parameters**: Clear error messages with required parameter names
2. **Invalid Team IDs**: Validation prevents same team comparisons
3. **API Rate Limits**: Automatic retry with exponential backoff
4. **Network Issues**: Graceful failure with detailed logging

### Debugging Commands
```bash
# Test parameter validation
scrapy crawl footystats_league_table -a api_key=example  # Should fail gracefully

# Test with invalid data
scrapy crawl footystats_team_vs_team -a api_key=example -a home_id=2 -a away_id=2  # Should fail gracefully

# Full debug output
scrapy crawl footystats_btts_stats -a api_key=example -a season_id=1625 -L DEBUG -s LOG_LEVEL=DEBUG
```

## Development Checklist

For each new spider development:

### Pre-Development
- [ ] Collect HTML documentation from FootyStats
- [ ] Extract and save sample JSON responses
- [ ] Document required and optional parameters
- [ ] Understand response structure and nested objects

### Development
- [ ] Create test contract with failing tests
- [ ] Implement item structure with comprehensive fields
- [ ] Create spider inheriting from FootyStatsBaseSpider
- [ ] Implement parameter validation
- [ ] Add comprehensive field mapping
- [ ] Handle nested objects and arrays

### Testing
- [ ] Unit tests for all major functionality
- [ ] Integration tests with sample responses
- [ ] Error handling tests (missing fields, API errors)
- [ ] Parameter validation tests
- [ ] Live API testing with example key

### Documentation
- [ ] Update spider CLAUDE.md with usage examples
- [ ] Update items CLAUDE.md with field documentation
- [ ] Add comprehensive docstrings
- [ ] Update README.md with user instructions

### Integration
- [ ] Test with Airflow DAG integration
- [ ] Verify output format compatibility
- [ ] Check rate limiting behavior
- [ ] Validate error handling in production

## Integration with Existing Spiders

All new spiders follow the same patterns as existing FootyStats spiders:
- Inherit from `FootyStatsBaseSpider`
- Use consistent parameter validation
- Follow established error handling patterns
- Generate compatible output formats
- Share rate limiting and quota management

This ensures seamless integration with existing workflows and Airflow orchestration.

## Future Development Guidelines

### When Adding New Endpoints
1. **API Documentation First**: Always collect HTML docs and sample responses
2. **Test-Driven Development**: Write tests before implementation
3. **Comprehensive Field Coverage**: Capture all available API fields
4. **Consistent Patterns**: Follow existing spider and item patterns
5. **Thorough Testing**: Unit, integration, and error handling tests
6. **Documentation**: Update all relevant CLAUDE.md and README files

### When Modifying Existing Spiders
1. **Backward Compatibility**: Maintain existing field names and structures
2. **Version Schema**: Update schema_version field when making breaking changes
3. **Test Updates**: Update tests to reflect new functionality
4. **Documentation**: Update usage examples and field documentation

### API Changes Handling
1. **Forward Compatibility**: Over-inclusive field mapping handles new fields
2. **Graceful Degradation**: Missing fields are handled without errors
3. **Monitoring**: Log warnings for structural changes
4. **Validation**: Strong validation prevents bad data propagation