# SPEC PRP: FootyStats API Spider Development

## Specification: Comprehensive FootyStats Spider Implementation with TDD Testing

Develop a complete set of Scrapy spiders, items, and test contracts for FootyStats API endpoints following TDD methodology and CLAUDE.md guidelines.

## Analysis Process

### 1. Current State Assessment

**Files Currently Present:**
- `scrapers/tests/resources/footystats/` - Contains 13 HTML documentation files
- `scrapers/odds_scraper/odds_scraper/items/footystats/` - Partially implemented items
- `scrapers/odds_scraper/odds_scraper/spiders/footystats/` - Partially implemented spiders

**Existing Implementation:**
```yaml
current_state:
  files:
    - scrapers/odds_scraper/odds_scraper/items/footystats/btts_stats_items.py
    - scrapers/odds_scraper/odds_scraper/items/footystats/league_table_items.py
    - scrapers/odds_scraper/odds_scraper/items/footystats/over_stats_items.py
    - scrapers/odds_scraper/odds_scraper/spiders/footystats/btts_stats_spider.py
    - scrapers/odds_scraper/odds_scraper/spiders/footystats/league_table_spider.py
    - scrapers/odds_scraper/odds_scraper/spiders/footystats/over_stats_spider.py
  behavior: Partial implementation with limited endpoint coverage
  issues:
    - Missing comprehensive item schemas based on actual API responses
    - No test contracts following TDD methodology
    - Missing critical endpoints (match details, team info, etc.)
    - No ItemLoaders for data processing
    - Incomplete API parameter handling
```

**Pain Points:**
- Manual implementation without TDD validation
- Missing test resources for contract validation
- Incomplete coverage of FootyStats API endpoints
- No systematic approach to schema evolution

### 2. Desired State Research

**Target Architecture:**
```yaml
desired_state:
  files:
    - Complete item classes for all 13+ API endpoints
    - Corresponding ItemLoader classes for data processing
    - Spider implementations for each endpoint
    - Test contracts with mock responses
    - Sample JSON responses for schema validation
  behavior:
    - TDD-driven development with contract testing
    - Comprehensive API coverage
    - Proper error handling and validation
    - Modular and extensible design
  benefits:
    - Reliable data extraction from FootyStats
    - Easy maintenance and schema updates
    - Comprehensive test coverage
    - Integration with existing pipeline architecture
```

**Best Practices Research:**
- Scrapy Item and ItemLoader patterns for API data
- TDD with pytest and mock responses
- API pagination handling
- Rate limiting and authentication
- Schema versioning for API evolution

## 3. User Clarification

**Transformation Goals:**
- Create comprehensive FootyStats spider ecosystem
- Implement TDD methodology with contract testing
- Ensure all 13+ API endpoints are covered
- Provide robust error handling and data validation

**Priority Objectives:**
1. **High Priority:** League table, matches, match details, teams
2. **Medium Priority:** Player stats, referee data, country/league lists
3. **Low Priority:** Advanced statistics and specialized endpoints

**Acceptable Trade-offs:**
- Start with core endpoints, expand incrementally
- Use mock responses initially, real API integration later
- Prioritize data integrity over speed optimization

## PRP Generation

### Hierarchical Objectives

#### High-Level: Complete FootyStats API Integration
Transform partial implementation into comprehensive, test-driven spider ecosystem for FootyStats API.

#### Mid-Level Milestones:
1. **Schema Definition:** Create complete item classes and loaders
2. **Spider Implementation:** Develop spiders for all endpoints
3. **Test Infrastructure:** Implement TDD with contract testing
4. **Integration:** Connect with existing pipeline architecture

#### Low-Level Tasks:

### Task Specification

#### 1. Schema Foundation
```yaml
create_base_items:
  action: CREATE
  file: scrapers/odds_scraper/odds_scraper/items/footystats/__init__.py
  changes: |
    - Create base FootyStats item with common fields
    - Add schema versioning support
    - Include metadata fields (scraped_at, spider_name, etc.)
  validation:
    - command: "python -c 'from odds_scraper.items.footystats import FootyStatsBaseItem; print(\"Import successful\")'"
    - expect: "Import successful"

create_league_table_item:
  action: MODIFY
  file: scrapers/odds_scraper/odds_scraper/items/footystats/league_table_items.py
  changes: |
    - Extend from FootyStatsBaseItem
    - Add all league table fields based on API schema
    - Include team statistics fields
    - Add ItemLoader with proper processors
  validation:
    - command: "python -c 'from odds_scraper.items.footystats.league_table_items import LeagueTableItem; print(len(LeagueTableItem.fields))'"
    - expect: "Field count > 15"

create_match_details_item:
  action: CREATE
  file: scrapers/odds_scraper/odds_scraper/items/footystats/match_details_items.py
  changes: |
    - Create comprehensive match details item
    - Include all match statistics (possession, shots, cards, etc.)
    - Add betting odds fields
    - Create MatchDetailsLoader with validation
  validation:
    - command: "python -c 'from odds_scraper.items.footystats.match_details_items import MatchDetailsItem; print(\"Created\")'"
    - expect: "Created"

create_league_matches_item:
  action: CREATE
  file: scrapers/odds_scraper/odds_scraper/items/footystats/league_matches_items.py
  changes: |
    - Create league matches item for schedule data
    - Include pagination support
    - Add match list processing
  validation:
    - command: "python -c 'from odds_scraper.items.footystats.league_matches_items import LeagueMatchesItem; print(\"Created\")'"
    - expect: "Created"

create_team_item:
  action: CREATE
  file: scrapers/odds_scraper/odds_scraper/items/footystats/team_items.py
  changes: |
    - Create team item with statistics support
    - Include team metadata fields
    - Add TeamLoader for data processing
  validation:
    - command: "python -c 'from odds_scraper.items.footystats.team_items import TeamItem; print(\"Created\")'"
    - expect: "Created"
```

#### 2. Spider Implementation
```yaml
create_league_table_spider:
  action: MODIFY
  file: scrapers/odds_scraper/odds_scraper/spiders/footystats/league_table_spider.py
  changes: |
    - Implement complete API parameter handling
    - Add proper authentication with API key
    - Include error handling and validation
    - Support optional statistics inclusion
  validation:
    - command: "scrapy check footystats_league_table"
    - expect: "OK"

create_match_details_spider:
  action: CREATE
  file: scrapers/odds_scraper/odds_scraper/spiders/footystats/match_details_spider.py
  changes: |
    - Create spider for individual match details
    - Handle match_id parameter validation
    - Process comprehensive match statistics
    - Include odds data extraction
  validation:
    - command: "scrapy check footystats_match_details"
    - expect: "OK"

create_league_matches_spider:
  action: CREATE
  file: scrapers/odds_scraper/odds_scraper/spiders/footystats/league_matches_spider.py
  changes: |
    - Create spider for league match schedules
    - Implement pagination handling
    - Support season_id parameter
    - Handle large result sets efficiently
  validation:
    - command: "scrapy check footystats_league_matches"
    - expect: "OK"

create_team_spider:
  action: CREATE
  file: scrapers/odds_scraper/odds_scraper/spiders/footystats/team_spider.py
  changes: |
    - Create individual team data spider
    - Support statistics inclusion
    - Handle team_id parameter validation
  validation:
    - command: "scrapy check footystats_team"
    - expect: "OK"

create_league_teams_spider:
  action: CREATE
  file: scrapers/odds_scraper/odds_scraper/spiders/footystats/league_teams_spider.py
  changes: |
    - Create spider for all teams in a league
    - Support season_id parameter
    - Include optional statistics
  validation:
    - command: "scrapy check footystats_league_teams"
    - expect: "OK"
```

#### 3. Test Infrastructure
```yaml
create_test_structure:
  action: CREATE
  file: scrapers/tests/contracts/test_footystats_spiders.py
  changes: |
    - Create base test class for FootyStats spiders
    - Implement mock response loading utilities
    - Add common test fixtures
  validation:
    - command: "python -c 'import scrapers.tests.contracts.test_footystats_spiders; print(\"Test module created\")'"
    - expect: "Test module created"

create_sample_responses:
  action: CREATE
  file: scrapers/tests/resources/footystats/sample_responses.json
  changes: |
    - Create sample JSON responses for each endpoint
    - Include realistic data based on API documentation
    - Add edge cases and error responses
  validation:
    - command: "python -c 'import json; json.load(open(\"scrapers/tests/resources/footystats/sample_responses.json\")); print(\"Valid JSON\")'"
    - expect: "Valid JSON"

create_league_table_tests:
  action: CREATE
  file: scrapers/tests/contracts/test_footystats_league_table.py
  changes: |
    - Create TDD tests for league table spider
    - Test item extraction and validation
    - Test error handling scenarios
    - Test ItemLoader processing
  validation:
    - command: "pytest scrapers/tests/contracts/test_footystats_league_table.py -v"
    - expect: "All tests pass"

create_match_details_tests:
  action: CREATE
  file: scrapers/tests/contracts/test_footystats_match_details.py
  changes: |
    - Create comprehensive tests for match details
    - Test all statistical fields extraction
    - Test odds data processing
    - Test error scenarios
  validation:
    - command: "pytest scrapers/tests/contracts/test_footystats_match_details.py -v"
    - expect: "All tests pass"
```

#### 4. Additional Endpoints
```yaml
create_additional_items:
  action: CREATE
  file: scrapers/odds_scraper/odds_scraper/items/footystats/additional_items.py
  changes: |
    - Create items for remaining endpoints:
      - CountryListItem
      - LeagueListItem
      - PlayerItem
      - RefereeItem
      - TodaysMatchesItem
  validation:
    - command: "python -c 'from odds_scraper.items.footystats.additional_items import CountryListItem; print(\"Created\")'"
    - expect: "Created"

create_additional_spiders:
  action: CREATE
  file: scrapers/odds_scraper/odds_scraper/spiders/footystats/additional_spiders.py
  changes: |
    - Create spiders for remaining endpoints
    - Implement proper parameter handling
    - Add comprehensive error handling
  validation:
    - command: "scrapy list | grep footystats | wc -l"
    - expect: "Count >= 10"
```

#### 5. Integration and Validation
```yaml
update_settings:
  action: MODIFY
  file: scrapers/odds_scraper/odds_scraper/settings.py
  changes: |
    - Add FootyStats-specific settings
    - Configure API rate limiting
    - Set up authentication handling
  validation:
    - command: "python -c 'from odds_scraper import settings; print(\"Settings updated\")'"
    - expect: "Settings updated"

create_integration_tests:
  action: CREATE
  file: scrapers/tests/integration/test_footystats_pipeline.py
  changes: |
    - Create end-to-end pipeline tests
    - Test spider-to-pipeline integration
    - Validate data flow and storage
  validation:
    - command: "pytest scrapers/tests/integration/test_footystats_pipeline.py -v"
    - expect: "All tests pass"

update_documentation:
  action: CREATE
  file: scrapers/odds_scraper/odds_scraper/spiders/footystats/CLAUDE.md
  changes: |
    - Document FootyStats spider architecture
    - Include usage examples
    - Add troubleshooting guide
    - Document API limitations and rate limits
  validation:
    - command: "ls -la scrapers/odds_scraper/odds_scraper/spiders/footystats/CLAUDE.md"
    - expect: "File exists"
```

### Implementation Strategy

#### Dependencies:
1. **Schema Definition** → Spider Implementation
2. **Sample Responses** → Test Creation
3. **Base Tests** → Specific Endpoint Tests
4. **Core Spiders** → Additional Endpoints
5. **All Components** → Integration Testing

#### Order of Implementation:
1. Create base items and schema foundation
2. Implement core spiders (league table, matches, match details)
3. Create sample responses and test infrastructure
4. Develop TDD tests for core functionality
5. Implement remaining endpoints
6. Integration testing and documentation

#### Progressive Enhancement:
- Start with static data extraction
- Add dynamic parameter handling
- Implement pagination and error handling
- Add comprehensive validation and testing

#### Rollback Plans:
- Keep existing partial implementations as backup
- Version control checkpoints at each milestone
- Incremental deployment with fallback options

## Risk Assessment

### Identified Risks:
1. **API Changes:** FootyStats API may evolve, breaking spiders
2. **Rate Limiting:** API may have undocumented rate limits
3. **Authentication:** API key requirements may change
4. **Data Volume:** Large responses may cause memory issues

### Mitigations:
1. **Schema Versioning:** Implement version handling in items
2. **Rate Limiting:** Add configurable delays and retry logic
3. **Authentication:** Externalize API keys and auth handling
4. **Memory Management:** Implement streaming for large datasets

### Go/No-Go Criteria:
- ✅ **Go:** If mock responses can be created and basic tests pass
- ❌ **No-Go:** If API authentication fails or schemas are inconsistent

## Quality Checklist

- [x] Current state fully documented
- [x] Desired state clearly defined
- [x] All objectives measurable
- [x] Tasks ordered by dependency
- [x] Each task has validation that AI can run
- [x] Risks identified with mitigations
- [x] Rollback strategy included
- [x] Integration points noted

## Context Requirements

- FootyStats API documentation analysis (completed)
- Existing Scrapy project structure
- TDD testing framework setup
- Sample response data for validation

---

**Focus:** This PRP emphasizes the transformation from partial implementation to comprehensive, test-driven FootyStats spider ecosystem following TDD methodology and CLAUDE.md guidelines.