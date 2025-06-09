# Decoupled OddsPortal Spiders Usage

## Overview

The OddsPortal scraping system is split into two separate spiders:

1. **Match Spider** (`oddsportal_match_spider`) - Scrapes match metadata (once per match)
2. **Odds Spider** (`oddsportal_odds_spider`) - Scrapes odds data directly using essential parameters

## Match Spider

### Purpose
- Extracts match metadata including teams, tournament, venue, match state
- Retrieves available betting markets and bookmakers
- Should be run once per match to gather necessary parameters for odds spider

### Usage
```bash
# Basic usage
scrapy crawl oddsportal_match_spider -a match_url="https://www.oddsportal.com/football/england/premier-league/arsenal-fulham-vRiDNL8C/"

# Save output to file
scrapy crawl oddsportal_match_spider -O match_data.json -a match_url="https://www.oddsportal.com/football/england/premier-league/arsenal-fulham-vRiDNL8C/"
```

### Output
The spider yields three items:
1. `EventHeaderItem` - Contains match_id, xhashf, sport_id, version_id, is_started
2. `EventBodyItem` - Match details, venue, bookmaker names
3. `PageVarItem` - Available betting markets

## Odds Spider

### Purpose
- Directly fetches odds data using essential parameters
- Builds endpoints from provided parameters without additional dependencies
- Includes is_started flag to identify if odds are closing lines

### Required Parameters
- `match_url` - Full match URL (for referer header)
- `match_id` - Match ID from EventHeaderItem
- `xhashf` - URL-encoded xhash from EventHeaderItem
- `sport_id` - Sport ID from EventHeaderItem
- `version_id` - Version ID from EventHeaderItem (optional, defaults to "1")
- `bet_types` - Comma-separated bet type IDs (optional, defaults to "1")
- `scopes` - Comma-separated scope IDs (optional, defaults to "2")
- `is_started` - Whether match has started: "true" or "false" (optional, defaults to false)

### Usage

```bash
# Basic usage - 1X2 Full Time with default mappings
scrapy crawl oddsportal_odds_spider -O odds_1x2_ft.json \
  -a match_url="https://www.oddsportal.com/football/england/premier-league/arsenal-fulham-vRiDNL8C/" \
  -a match_id="vRiDNL8C" \
  -a xhashf="%79%6a%63%34%63" \
  -a sport_id="1" \
  -a is_started="true"

# Multiple bet types and scopes
scrapy crawl oddsportal_odds_spider -O odds_multiple.json \
  -a match_url="https://www.oddsportal.com/football/england/premier-league/arsenal-fulham-vRiDNL8C/" \
  -a match_id="vRiDNL8C" \
  -a xhashf="%79%6a%63%34%63" \
  -a sport_id="1" \
  -a version_id="1" \
  -a bet_types="1,2,5" \
  -a scopes="2,3" \
  -a is_started="false"

# With custom bookmaker mappings (for different regions/proxies)
scrapy crawl oddsportal_odds_spider -O odds_custom.json \
  -a match_url="https://www.oddsportal.com/football/england/premier-league/arsenal-fulham-vRiDNL8C/" \
  -a match_id="vRiDNL8C" \
  -a xhashf="%79%6a%63%34%63" \
  -a sport_id="1" \
  -a bet_types="1" \
  -a bookmaker_names='{"16": "bet365", "18": "Pinnacle", "500": "22Bet"}'

# Asian Handicap Full Time only
scrapy crawl oddsportal_odds_spider -O odds_ah_ft.json \
  -a match_url="https://www.oddsportal.com/football/england/premier-league/arsenal-fulham-vRiDNL8C/" \
  -a match_id="vRiDNL8C" \
  -a xhashf="%79%6a%63%34%63" \
  -a sport_id="1" \
  -a bet_types="5" \
  -a scopes="2" \
  -a is_started="true"
```

### Optional Mapping Parameters

The odds spider supports custom mappings for bookmakers and betting types. This is useful when:
- Using proxies from different regions (bookmakers vary by location)
- Scraping in different languages
- Customizing output names

Available mapping parameters:
- `bookmaker_names` - JSON string mapping bookmaker IDs to names
- `betting_type_names` - JSON string mapping betting type IDs to names and short names
- `scope_names` - JSON string mapping scope IDs to names
- `handicap_names` - JSON string mapping handicap IDs to names

If not provided, the spider uses default mappings from `utils/default_mappings.py`.

## Workflow Example

```bash
# Step 1: Run match spider to get parameters
scrapy crawl oddsportal_match_spider -O arsenal_match.json \
  -a match_url="https://www.oddsportal.com/football/england/premier-league/arsenal-fulham-vRiDNL8C/"

# Step 2: Extract parameters from match data
# From the JSON output, get:
# - match_id: "vRiDNL8C"
# - xhashf: "%79%6a%63%34%63"
# - sport_id: 1
# - version_id: 1
# - is_started: true

# Step 3: Run odds spider with extracted parameters
scrapy crawl oddsportal_odds_spider -O arsenal_odds_1x2.json \
  -a match_url="https://www.oddsportal.com/football/england/premier-league/arsenal-fulham-vRiDNL8C/" \
  -a match_id="vRiDNL8C" \
  -a xhashf="%79%6a%63%34%63" \
  -a sport_id="1" \
  -a bet_types="1" \
  -a is_started="true"
```

## Common Bet Types and Scopes

### Bet Types
- `1` - 1X2 (Home/Draw/Away)
- `2` - Over/Under
- `3` - Home/Away (no draw)
- `4` - Double Chance
- `5` - Asian Handicap
- `6` - Draw No Bet
- `8` - Correct Score
- `9` - Half Time / Full Time
- `10` - Odd or Even
- `12` - European Handicap
- `13` - Both Teams to Score

### Scopes
- `2` - Full Time
- `3` - First Half
- `4` - Second Half

## Benefits

1. **Direct Control**: Explicitly provide all parameters needed to build endpoints
2. **No Dependencies**: Odds spider doesn't need to parse match data files
3. **Clear Responsibility**: Each spider has a single, focused purpose
4. **Flexibility**: Can scrape odds at any time with just the essential parameters