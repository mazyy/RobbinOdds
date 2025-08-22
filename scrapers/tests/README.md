# Testing Framework for Odds Scrapers

This directory contains comprehensive testing resources and procedures for all scraping spiders, with a focus on Test-Driven Development (TDD) and resource-based testing.

## Directory Structure

```
tests/
├── README.md                          # This file - testing overview
├── contracts/                         # Spider contract tests
│   ├── test_footystats_spiders.py    # Base test utilities
│   ├── test_footystats_league_table.py
│   ├── test_footystats_match_details.py
│   └── test_*.py                      # Other spider tests
└── resources/                         # Test data and samples
    ├── footystats/                    # FootyStats API resources
    │   ├── sample_responses.json      # JSON sample responses
    │   ├── api_documentations.html    # Main API documentation
    │   ├── *_api_documentations.html  # Endpoint-specific docs
    │   └── ...
    └── oddsportal/                    # OddsPortal resources
        ├── match_page.html            # Sample match pages
        ├── odds_response.json         # Odds API samples
        └── ...
```

## Testing Philosophy

### Test-Driven Development (TDD)
All spider development follows strict TDD principles:
1. **Red**: Write failing tests first
2. **Green**: Implement minimal code to pass tests
3. **Refactor**: Improve code while keeping tests green

### Resource-Based Testing
Real HTML/JSON samples ensure tests reflect actual data structures:
- **Offline Testing**: No external API calls during test runs
- **Consistent Results**: Same samples produce same test outcomes
- **Edge Case Coverage**: Capture unusual response structures

### Contract Testing
Spider contracts define expected behavior:
- **Input validation**: Parameter requirements and validation
- **Output structure**: Item field presence and types
- **Error handling**: Graceful failure scenarios
- **Performance**: Response time and memory usage

## HTML Sample Workflow

### 1. Collecting HTML Documentation

#### For FootyStats API Endpoints
```bash
# Navigate to API documentation page
# Example: https://footystats.org/api/documentations/league-table

# Use Scrapy shell to collect documentation
scrapy shell "https://footystats.org/api/documentations/league-table"

# In shell, save the documentation
>>> with open('scrapers/tests/resources/footystats/league_table_api_documentations.html', 'wb') as f:
...     f.write(response.body)
>>> print("Documentation saved successfully")

# Exit shell
>>> exit()
```

#### For OddsPortal HTML Pages
```bash
# Use proper user agent for realistic scraping
scrapy shell -s USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" "https://www.oddsportal.com/football/england/premier-league/match-url/"

# Save HTML response
>>> with open('scrapers/tests/resources/oddsportal/match_page.html', 'wb') as f:
...     f.write(response.body)
>>> view(response)  # Opens in browser for verification
```

### 2. Extracting JSON Sample Responses

#### From FootyStats API Documentation
```python
# Extract JSON samples from HTML documentation
from bs4 import BeautifulSoup
import json

def extract_json_from_docs(html_file, endpoint_name):
    """Extract JSON examples from API documentation HTML"""
    with open(html_file, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Find JSON code blocks
    json_blocks = soup.find_all('code', class_='json')
    
    for block in json_blocks:
        try:
            sample_data = json.loads(block.text)
            
            # Add to sample_responses.json
            sample_entry = {
                endpoint_name: {
                    "endpoint": f"https://api.football-data-api.com/{endpoint_name}",
                    "parameters": {"key": "example"},  # Add endpoint-specific params
                    "response": sample_data
                }
            }
            
            return sample_entry
        except json.JSONDecodeError:
            continue
    
    return None
```

#### Direct API Sampling
```bash
# Use scrapy shell to call API directly
scrapy shell "https://api.football-data-api.com/league-tables?key=example&season_id=2012"

# Extract and save JSON response
>>> import json
>>> data = json.loads(response.text)
>>> 
>>> # Create sample entry
>>> sample = {
...     "league_table": {
...         "endpoint": "https://api.football-data-api.com/league-tables",
...         "parameters": {"key": "example", "season_id": 2012},
...         "response": data.get('data', [])
...     }
... }
>>> 
>>> # Add to existing samples
>>> with open('scrapers/tests/resources/footystats/sample_responses.json', 'r+') as f:
...     existing = json.load(f)
...     existing.update(sample)
...     f.seek(0)
...     json.dump(existing, f, indent=2)
...     f.truncate()
```

### 3. Using Samples in Tests

#### Mock Response Creation
```python
# tests/contracts/test_footystats_spiders.py
import json
from scrapy.http import HtmlResponse, Request

class FootyStatsTestBase:
    """Base test utilities for FootyStats spiders"""
    
    @pytest.fixture
    def sample_responses(self):
        """Load sample API responses"""
        with open('scrapers/tests/resources/footystats/sample_responses.json', 'r') as f:
            return json.load(f)
    
    def create_json_response(self, url, data):
        """Create mock JSON response for testing"""
        request = Request(url=url)
        json_data = {"success": True, "data": data}
        
        return HtmlResponse(
            url=url,
            body=json.dumps(json_data).encode('utf-8'),
            encoding='utf-8',
            request=request
        )
    
    def create_html_response(self, url, html_file):
        """Create mock HTML response from saved file"""
        with open(html_file, 'rb') as f:
            body = f.read()
        
        request = Request(url=url)
        return HtmlResponse(url=url, body=body, encoding='utf-8', request=request)
```

#### Spider Contract Tests
```python
# tests/contracts/test_footystats_league_table.py
class TestFootyStatsLeagueTableSpider(FootyStatsTestBase):
    
    @pytest.fixture
    def mock_response(self, sample_responses):
        """Create mock response from sample data"""
        endpoint_data = sample_responses['league_table']
        return self.create_json_response(
            url=endpoint_data['endpoint'],
            data=endpoint_data['response']
        )
    
    def test_parse_response_data(self, spider, mock_response):
        """Test parsing with real sample data"""
        items = list(spider.parse(mock_response))
        
        # Contract: Should yield items matching sample structure
        assert len(items) > 0
        
        item = items[0]
        assert 'team_id' in item
        assert 'name' in item
        assert 'position' in item
```

## Testing Procedures

### 1. Unit Testing Individual Components

```bash
# Test specific spider functionality
pytest scrapers/tests/contracts/test_footystats_league_table.py::TestFootyStatsLeagueTableSpider::test_parse_response_data -v

# Test with coverage
pytest scrapers/tests/contracts/ --cov=scrapers/odds_scraper/odds_scraper/spiders/footystats --cov-report=html
```

### 2. Integration Testing with Real APIs

```bash
# Test spider with example API key (limited functionality)
scrapy crawl footystats_league_table -a api_key=example -a season_id=1625 -L DEBUG

# Test with production key (careful with rate limits)
scrapy crawl footystats_league_table -a api_key=your_real_key -a season_id=2012 -O test_output.json -L INFO
```

### 3. Contract Testing with Scrapy

```bash
# Use Scrapy's built-in contract testing
scrapy check footystats_league_table

# Check all FootyStats spiders
scrapy list | grep footystats | xargs -I {} scrapy check {}
```

### 4. Error Handling Testing

```python
def test_handle_missing_data(self, spider):
    """Test graceful handling of missing elements"""
    # Create response with missing data
    empty_response = self.create_json_response(
        'https://api.test.com/league-tables',
        []  # Empty data
    )
    
    # Should not crash
    items = list(spider.parse(empty_response))
    assert len(items) == 0

def test_handle_malformed_response(self, spider):
    """Test handling of malformed JSON"""
    malformed_response = self.create_json_response(
        'https://api.test.com/league-tables',
        {'error': 'Invalid request'}  # Error response
    )
    
    # Should handle gracefully
    items = list(spider.parse(malformed_response))
    assert isinstance(items, list)
```

## Resource Management Guidelines

### HTML Documentation Files
- **Naming**: `{endpoint}_api_documentations.html`
- **Size limit**: < 5MB per file
- **Update frequency**: When API documentation changes
- **Encoding**: UTF-8

### JSON Sample Responses
- **Naming**: `sample_responses.json` (single file for all endpoints)
- **Structure**: Nested by endpoint name
- **Size limit**: < 10MB total
- **Update frequency**: When API responses change

### Test Resource Organization
```json
{
  "endpoint_name": {
    "endpoint": "https://api.url/endpoint",
    "parameters": {
      "key": "example",
      "required_param": "value"
    },
    "response": [
      {
        "sample": "data"
      }
    ]
  }
}
```

## Running Tests

### Local Development
```bash
# Run all tests
pytest scrapers/tests/

# Run specific test file
pytest scrapers/tests/contracts/test_footystats_league_table.py -v

# Run with debug output
pytest scrapers/tests/contracts/test_footystats_league_table.py -v -s

# Run tests with coverage
pytest scrapers/tests/ --cov=scrapers/odds_scraper --cov-report=html
```

### Continuous Integration
```bash
# CI pipeline test command
pytest scrapers/tests/contracts/ --cov=scrapers/odds_scraper/odds_scraper/spiders --cov-fail-under=80 --tb=short
```

### Performance Testing
```bash
# Test spider performance with time limits
timeout 30s scrapy crawl footystats_league_table -a api_key=example -a season_id=1625

# Memory usage testing
/usr/bin/time -v scrapy crawl footystats_league_table -a api_key=example -a season_id=1625
```

## Best Practices

### Sample Collection
1. **Representative Data**: Collect samples that represent typical API responses
2. **Edge Cases**: Include responses with missing fields, empty arrays, null values
3. **Error Responses**: Save API error responses for error handling tests
4. **Version Control**: Commit samples to track API changes over time

### Test Development
1. **Test First**: Write tests before implementing spider functionality
2. **Descriptive Names**: Use clear, descriptive test method names
3. **Independent Tests**: Each test should be self-contained
4. **Mocking**: Mock external dependencies to ensure test reliability

### Resource Maintenance
1. **Regular Updates**: Update samples when APIs change
2. **Size Management**: Keep sample files reasonably sized
3. **Documentation**: Document any special handling required for samples
4. **Cleanup**: Remove outdated samples when endpoints are deprecated

## Troubleshooting

### Test Failures
```bash
# Debug failed tests with verbose output
pytest scrapers/tests/contracts/test_footystats_league_table.py::test_parse_response_data -v -s --tb=long

# Run single test with pdb debugger
pytest scrapers/tests/contracts/test_footystats_league_table.py::test_parse_response_data --pdb
```

### Sample Updates
```bash
# Verify sample structure
python -m json.tool scrapers/tests/resources/footystats/sample_responses.json

# Update samples from live API
scrapy shell "https://api.football-data-api.com/league-tables?key=example&season_id=2012"
```

### Spider Debugging
```bash
# Test spider with cached responses
scrapy crawl footystats_league_table -a api_key=example -a season_id=1625 -s HTTPCACHE_ENABLED=True -L DEBUG

# Check spider contracts
scrapy check footystats_league_table --verbose
```

This testing framework ensures reliable, maintainable spiders through comprehensive test coverage and realistic sample data.