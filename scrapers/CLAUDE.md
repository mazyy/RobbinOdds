# CLAUDE.md - Scrapers Directory

This guide provides comprehensive instructions for working with the scraping layer of the value betting platform.

## Scraping Philosophy

### Data Integrity First
Raw data is sacred. Always capture and store raw responses before any processing. We can always re-process, but we can't re-scrape the past.

### Defensive Programming
Websites change. Our scrapers must be resilient:
- Validate all selectors
- Handle missing elements gracefully
- Log extensively when parsing fails
- Alert on structural changes

## 📁 Directory Structure

```
scrapers/
├── CLAUDE.md                   # This file
├── odds_scraper/              # Main Scrapy project
│   ├── CLAUDE.md             # Spider implementation details
│   ├── scrapy.cfg            # Scrapy configuration
│   └── odds_scraper/
│       ├── spiders/          # Spider implementations
│       ├── items/            # Data models
│       ├── pipelines/        # Data processing
│       ├── middlewares/      # Request/response processing
│       └── utils/            # Helper functions
├── common/                    # Shared scraping utilities
│   ├── proxies.py           # Proxy management
│   ├── user_agents.py       # User agent rotation
│   └── validators.py        # Data validation
└── tests/                    # Scraper tests
```

## 🕷️ Spider Development Principles

### 1. Single Responsibility
Each spider does ONE thing well:
```python
# ✅ Good - Focused spider
class OddsPortalMatchSpider(Spider):
    """Extracts match metadata only"""
    
# ❌ Bad - Does too much
class OddsPortalEverythingSpider(Spider):
    """Gets matches, odds, stats, everything"""
```

### 2. Explicit Parameters
Spiders should declare their required parameters:
```python
class OddsPortalOddsSpider(Spider):
    name = "oddsportal_odds"
    
    def __init__(self, match_id=None, xhashf=None, *args, **kwargs):
        if not match_id or not xhashf:
            raise ValueError("match_id and xhashf are required")
        super().__init__(*args, **kwargs)
```

### 3. Predictable Output
Spiders should yield well-defined items:
```python
# Always use Items, not dicts
yield MatchItem(
    match_id=match_id,
    home_team=home_team,
    away_team=away_team,
    timestamp=timestamp
)
```

## 🏗️ Spider Architecture Patterns

### OddsPortal Spider Architecture
OddsPortal spiders follow a specific hierarchy matching their data structure:

```
OddsPortal League Spider → OddsPortal Season Spider → OddsPortal Match Spider → OddsPortal Odds Spider
         ↓                        ↓                           ↓                        ↓
    League URLs             Match URLs              Match Metadata + xhashf      Encrypted Odds Data
```

**Note**: Each website has its own spider architecture. See site-specific CLAUDE.md files for details.

## 📊 Data Models (Items)

### Item Design Principles

1. **Mirror the source structure** - Don't transform in items
2. **Use descriptive field names** - `match_timestamp` not `ts`
3. **Include metadata** - Always add `scraped_at`, `spider_name`
4. **Version your schemas** - Add `schema_version` field

### Item Example
```python
from scrapy import Item, Field
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from datetime import datetime

class MatchItem(Item):
    # Identity
    match_id = Field()
    schema_version = Field(default="1.0.0")
    
    # Match data
    home_team = Field()
    away_team = Field()
    match_timestamp = Field()
    
    # Metadata
    scraped_at = Field()
    spider_name = Field()
    source_url = Field()

class MatchLoader(ItemLoader):
    default_item_class = MatchItem
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()
    
    # Custom processors
    match_timestamp_in = MapCompose(
        lambda x: datetime.fromisoformat(x) if isinstance(x, str) else x
    )
```

## 🔄 Pipeline Architecture

### Pipeline Responsibilities

```python
# 1. Validation Pipeline - First
class ValidationPipeline:
    """Ensure data integrity"""
    def process_item(self, item, spider):
        self.validate_required_fields(item)
        self.validate_data_types(item)
        return item

# 2. Deduplication Pipeline
class DeduplicationPipeline:
    """Prevent duplicate data"""
    def process_item(self, item, spider):
        if self.is_duplicate(item):
            raise DropItem(f"Duplicate item: {item['match_id']}")
        return item

# 3. Storage Pipeline - Last
class StoragePipeline:
    """Persist to S3/Database"""
    def process_item(self, item, spider):
        self.store_raw(item)
        self.store_processed(item)
        return item
```

### Pipeline Configuration
```python
# settings.py
ITEM_PIPELINES = {
    'odds_scraper.pipelines.ValidationPipeline': 100,
    'odds_scraper.pipelines.DeduplicationPipeline': 200,
    'odds_scraper.pipelines.StoragePipeline': 900,
}
```

## 🛡️ Middleware Patterns

### Request Middleware
```python
class ProxyMiddleware:
    """Rotate proxies for each request"""
    
    def process_request(self, request, spider):
        proxy = self.get_next_proxy()
        request.meta['proxy'] = proxy
        return None

class UserAgentMiddleware:
    """Rotate user agents"""
    
    def process_request(self, request, spider):
        ua = self.get_random_user_agent()
        request.headers['User-Agent'] = ua
        return None
```

### Response Middleware
```python
class RetryMiddleware:
    """Smart retry logic"""
    
    def process_response(self, request, response, spider):
        if response.status in [429, 503]:
            return self._retry(request) or response
        return response
```

## 🔧 Settings Management

### Environment-Specific Settings
```python
# settings.py
import os

ENV = os.getenv('SCRAPY_ENV', 'development')

# Base settings
BOT_NAME = 'odds_scraper'
ROBOTSTXT_OBEY = False  # We check manually

# Environment-specific
if ENV == 'production':
    CONCURRENT_REQUESTS = 16
    DOWNLOAD_DELAY = 1
    AUTOTHROTTLE_ENABLED = True
else:
    CONCURRENT_REQUESTS = 2
    DOWNLOAD_DELAY = 3
    AUTOTHROTTLE_ENABLED = False

# Retry configuration
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]
```

## 🧪 Testing Spiders - TDD Approach

### Test-Driven Development Workflow

#### 1. Resource Collection
First, collect HTML responses for testing:
```bash
# Open scrapy shell with fake user-agent
scrapy shell -s USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" "https://target-url.com"

# In shell, save response for later use:
>>> view(response)  # Opens in browser
>>> # Save HTML to resources
>>> with open('scrapers/tests/resources/site_name/page_type.html', 'wb') as f:
...     f.write(response.body)
```

#### 2. Directory Structure for Test Resources
```
scrapers/
├── tests/
│   ├── resources/
│   │   ├── oddsportal/
│   │   │   ├── match_page.html
│   │   │   ├── odds_response.json
│   │   │   ├── league_page.html
│   │   │   └── encrypted_data.txt
│   │   ├── footystats/
│   │   │   ├── league_table.html
│   │   │   └── match_stats.html
│   │   └── other_sites/
│   └── contracts/
│       ├── test_oddsportal_match.py
│       └── test_footystats_table.py
```

#### 3. Spider Contracts with Mock Responses
```python
# tests/contracts/test_oddsportal_match.py
import os
import pytest
from scrapy.http import HtmlResponse, Request
from odds_scraper.spiders.oddsportal.match_spider import OddsPortalMatchSpider
from odds_scraper.items.oddsportal import MatchItem

class TestOddsPortalMatchSpider:
    @pytest.fixture
    def spider(self):
        """Initialize spider with test parameters"""
        return OddsPortalMatchSpider(
            match_url="https://www.oddsportal.com/test/match/"
        )
    
    @pytest.fixture
    def mock_response(self):
        """Load saved HTML as mock response"""
        html_path = 'scrapers/tests/resources/oddsportal/match_page.html'
        with open(html_path, 'rb') as f:
            body = f.read()
        
        request = Request(url='https://www.oddsportal.com/test/match/')
        return HtmlResponse(
            url='https://www.oddsportal.com/test/match/',
            body=body,
            encoding='utf-8',
            request=request
        )
    
    def test_parse_match_metadata(self, spider, mock_response):
        """Test extraction of match metadata"""
        # Contract: Should extract required fields
        items = list(spider.parse(mock_response))
        
        assert len(items) == 1
        item = items[0]
        
        # Verify all required fields are present
        assert isinstance(item, MatchItem)
        assert item.get('match_id') is not None
        assert item.get('xhashf') is not None
        assert item.get('sport_id') is not None
        
    def test_parse_encrypted_data(self, spider, mock_response):
        """Test decryption of embedded data"""
        # Contract: Should successfully decrypt PBKDF2HMAC data
        items = list(spider.parse(mock_response))
        
        item = items[0]
        # Verify decrypted fields have expected format
        assert isinstance(item.get('match_id'), str)
        assert len(item.get('xhashf')) > 0
        
    def test_handle_missing_data(self, spider):
        """Test graceful handling of missing elements"""
        # Create response with missing data
        body = b'<html><body>No data here</body></html>'
        response = HtmlResponse(
            url='https://www.oddsportal.com/test/',
            body=body
        )
        
        # Contract: Should not crash, should log error
        items = list(spider.parse(response))
        assert len(items) == 0
```

#### 4. Running Tests
```bash
# Run all spider contracts
pytest scrapers/tests/contracts/

# Run specific spider test
pytest scrapers/tests/contracts/test_oddsportal_match.py -v

# Run with coverage
pytest scrapers/tests/contracts/ --cov=scrapers/odds_scraper/odds_scraper/spiders
```

### Scrapy Contract Decorators (Alternative)
```python
class OddsPortalMatchSpider(Spider):
    """Spider with inline contracts"""
    name = 'oddsportal_match'
    
    def parse(self, response):
        """Parse match page.
        
        @url https://www.oddsportal.com/football/test/match/
        @returns items 1 1
        @returns requests 0 0
        @scrapes match_id xhashf sport_id
        """
        # Implementation here
        pass
```

### Testing Commands for Development
```bash
# Check spider contracts
scrapy check oddsportal_match

# Test with saved cache (using local HTML)
scrapy crawl oddsportal_match \
    -s HTTPCACHE_ENABLED=True \
    -s HTTPCACHE_DIR=scrapers/tests/cache \
    -L DEBUG
```

## 📈 Performance Optimization

### 1. Concurrent Requests
Balance speed vs. politeness:
```python
# Per domain limits
CONCURRENT_REQUESTS_PER_DOMAIN = 2
DOWNLOAD_DELAY = 1  # Minimum delay between requests
```

### 2. Caching During Development
```python
# Enable HTTP cache for development
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600
HTTPCACHE_DIR = 'httpcache'
```

### 3. Selective Field Extraction
Only extract what you need:
```python
# ✅ Good - Specific extraction
yield {
    'match_id': response.css('.match-id::text').get(),
    'home_team': response.css('.home-team::text').get(),
}

# ❌ Bad - Extract everything
yield {
    'html': response.text,  # Don't store entire HTML
}
```

## 🔍 Debugging Techniques

### Debug Shell
```bash
# Open Scrapy shell for URL
scrapy shell "http://example.com/match"

# In shell:
>>> response.css('.selector').get()
>>> response.xpath('//div[@class="test"]').getall()
```

### Logging
```python
import logging

class MySpider(Spider):
    def parse(self, response):
        self.logger.info(f"Parsing {response.url}")
        
        # Debug selector
        self.logger.debug(
            f"Found elements: {response.css('.target').getall()}"
        )
        
        # Warning for issues
        if not response.css('.expected'):
            self.logger.warning(f"Expected element missing on {response.url}")
```

## 🚨 Common Pitfalls

### 1. Not Handling Dynamic Content
```python
# ❌ Wrong - Assumes static HTML
data = response.css('.dynamic-content::text').get()

# ✅ Right - Check for JavaScript-rendered content
# Use Splash or Selenium middleware if needed
```

### 2. Hardcoding Selectors
```python
# ❌ Wrong - Brittle selector
price = response.css('div:nth-child(3) > span::text').get()

# ✅ Right - Semantic selector
price = response.css('[data-testid="price"]::text').get()
```

### 3. Ignoring Encoding
```python
# ✅ Always specify encoding
response.css('.text::text').get().encode('utf-8')
```

## 📝 Spider Documentation Template

```python
class ExampleSpider(Spider):
    """
    Spider for extracting [data type] from [source].
    
    Arguments:
        param1 (str): Description of param1
        param2 (int): Description of param2
    
    Yields:
        ItemType: Description of yielded items
    
    Example:
        scrapy crawl example_spider -a param1="value"
    
    Notes:
        - Special considerations
        - Known limitations
    """
```

## ⚠️ Important Reminders

### For Claude Code
- **Test spiders with single URLs first**
- **Always check robots.txt manually**
- **Log extensively but avoid logging sensitive data**
- **Use Items, not dictionaries**
- **Check the specific spider's CLAUDE.md for implementation details**

### Current Spider Status
- ✅ OddsPortal match spider
- ✅ OddsPortal odds spider  
- 🔄 OddsPortal league spider
- 📋 OddsPortal season spider
- 📋 FootyStats spiders

---

_For specific spider implementations, see odds_scraper/CLAUDE.md_