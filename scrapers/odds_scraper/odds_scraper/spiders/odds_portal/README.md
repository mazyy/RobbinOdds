# OddsPortal Spiders Documentation

## Spider Architecture

The OddsPortal scraping system consists of four specialized spiders:

1. **League Spider** - Discovers leagues and available seasons
2. **Season Spider** - Extracts match lists from seasons (design phase)
3. **Match Spider** - Scrapes match metadata
4. **Odds Spider** - Fetches odds data using match parameters

## 1. League Spider (`oddsportal_league_spider`)

### Purpose
Discovers the structure of a league including all available seasons (historical and current).

### Usage
```bash
scrapy crawl oddsportal_league_spider \
  -a league_url="https://www.oddsportal.com/basketball/usa/nba/" \
  -O nba_discovery.json
```

### Output Structure
```json
{
  "sport": {
    "sport_id": "1",
    "sport_name": "Basketball",
    "sport_url_slug": "basketball"
  },
  "country": {
    "country_id": "USA",
    "country_name": "Usa",
    "country_url_slug": "usa",
    "region": "North America"
  },
  "league": {
    "league_id": "nba_encoded_id",
    "league_name": "NBA",
    "league_url": "https://www.oddsportal.com/basketball/usa/nba",
    "sport_id": "1",
    "is_active": true,
    "league_type": "domestic"
  },
  "seasons": [
    {
      "season_id": "current",
      "season_name": "NBA Current Season",
      "is_current": true,
      "has_results": true,
      "has_fixtures": true
    },
    {
      "season_id": "2023-2024",
      "season_name": "NBA 2023-2024",
      "season_url": "https://www.oddsportal.com/basketball/usa/nba-2023-2024/results/",
      "start_year": 2023,
      "end_year": 2024
    }
  ]
}
```

## 2. Season Spider (`oddsportal_season_spider`) - Coming Soon

### Purpose
Extracts all matches from a specific season with minimal information needed for match/odds spiders.

### Planned Usage
```bash
# Historical season results
scrapy crawl oddsportal_season_spider \
  -a league_id="nba_encoded_id" \
  -a season_id="2023-2024" \
  -a season_url="https://www.oddsportal.com/basketball/usa/nba-2023-2024/results/" \
  -a sport_id="1" \
  -a mode="results" \
  -O nba_2023_2024_matches.json

# Current season fixtures
scrapy crawl oddsportal_season_spider \
  -a league_id="nba_encoded_id" \
  -a season_id="current" \
  -a season_url="https://www.oddsportal.com/basketball/usa/nba/" \
  -a sport_id="1" \
  -a mode="fixtures" \
  -O nba_upcoming_matches.json
```

### Output Structure
```json
{
  "league_id": "nba_encoded_id",
  "season_id": "2023-2024",
  "extraction_type": "results",
  "matches": [
    {
      "match_id": "vRiDNL8C",
      "match_url": "https://www.oddsportal.com/basketball/usa/nba/lakers-celtics-vRiDNL8C/",
      "match_timestamp": "2024-03-15T19:00:00",
      "status": "finished",
      "home_team": "LA Lakers",
      "away_team": "Boston Celtics"
    }
  ]
}
```

## 3. Match Spider (`oddsportal_match_spider`)

### Purpose
Extracts detailed match metadata including parameters needed for odds extraction.

### Usage
```bash
scrapy crawl oddsportal_match_spider \
  -a match_url="https://www.oddsportal.com/football/england/premier-league/arsenal-fulham-vRiDNL8C/" \
  -O match_metadata.json
```

### Key Output Fields
- `match_id`: Unique match identifier
- `xhashf`: URL-encoded hash for odds endpoints
- `sport_id`: Sport identifier
- `version_id`: API version
- `is_started`: Match status boolean
- Team names, tournament info, venue details

## 4. Odds Spider (`oddsportal_odds_spider`)

### Purpose
Directly fetches odds data using parameters from match spider.

### Usage
```bash
# Basic 1X2 odds
scrapy crawl oddsportal_odds_spider \
  -a match_url="https://www.oddsportal.com/football/england/premier-league/arsenal-fulham-vRiDNL8C/" \
  -a match_id="vRiDNL8C" \
  -a xhashf="%79%6a%63%34%63" \
  -a sport_id="1" \
  -a is_started="true" \
  -O odds_data.json

# Multiple markets
scrapy crawl oddsportal_odds_spider \
  -a match_url="https://www.oddsportal.com/football/england/premier-league/arsenal-fulham-vRiDNL8C/" \
  -a match_id="vRiDNL8C" \
  -a xhashf="%79%6a%63%34%63" \
  -a sport_id="1" \
  -a bet_types="1,2,5" \
  -a scopes="2,3" \
  -O odds_multiple_markets.json
```

### Parameters
- **Required**: `match_url`, `match_id`, `xhashf`, `sport_id`
- **Optional**: 
  - `bet_types`: Comma-separated betting type IDs (default: "1")
  - `scopes`: Comma-separated scope IDs (default: "2")
  - `is_started`: "true"/"false" (default: "false")
  - `version_id`: API version (default: "1")

## Data Flow Pipeline

```
1. League Discovery
   ├── Input: League URL
   └── Output: Sport, Country, League info + Season list

2. Season Extraction (per season)
   ├── Input: Season URL + League metadata
   └── Output: List of matches with timestamps

3. Match Scraping (per match)
   ├── Input: Match URL
   └── Output: Match metadata + xhash parameters

4. Odds Collection (per match/market)
   ├── Input: Match parameters + market selection
   └── Output: Detailed odds history by bookmaker
```

## Common Betting Types

| ID | Type | Description |
|----|------|-------------|
| 1 | 1X2 | Home/Draw/Away |
| 2 | Over/Under | Total goals/points |
| 3 | Home/Away | No draw option |
| 4 | Double Chance | Two outcomes covered |
| 5 | Asian Handicap | Handicap betting |
| 6 | Draw No Bet | Stake returned on draw |
| 8 | Correct Score | Exact result |
| 9 | HT/FT | Half time/Full time |
| 10 | Odd/Even | Total goals odd or even |
| 12 | European Handicap | Fixed handicap |
| 13 | Both Teams Score | Yes/No |

## Common Scopes

| ID | Scope | Sports |
|----|-------|---------|
| 2 | Full Time | All |
| 3 | First Half | Football, Basketball |
| 4 | Second Half | Football, Basketball |
| 5-7 | Periods | Hockey |
| 8-11 | Quarters | Basketball |
| 12-16 | Sets | Tennis |

## Rate Limiting

All spiders implement rate limiting:
- `CONCURRENT_REQUESTS`: 2-4
- `DOWNLOAD_DELAY`: 1-2 seconds
- `AUTOTHROTTLE_ENABLED`: True
- Random delay variation to avoid detection

## Error Handling

Spiders include:
- Decryption error recovery
- HTTP error handling
- Automatic retries with backoff
- Detailed logging for debugging

## Storage Considerations

Output can be saved as:
- JSON (recommended for development)
- CSV (for simple analysis)
- Direct to database (production)

The spiders are decoupled from storage, allowing flexible integration with any data pipeline.

## Future Enhancements

1. **Live Odds Spider**: Real-time odds during matches
2. **Team Spider**: Extract team-specific data
3. **Player Props Spider**: Player performance markets
4. **Historical Odds Spider**: Bulk historical data extraction

## Troubleshooting

### Common Issues

1. **Empty xhash**: Match might be too old or removed
2. **Decryption failures**: Usually rate limiting, increase delays
3. **Missing seasons**: Some leagues have limited historical data
4. **404 errors**: Match URLs change, use fresh discovery data

### Debug Mode

Run with increased logging:
```bash
scrapy crawl spider_name -L DEBUG -a param=value
```

### Testing Individual Components

```bash
# Test league parsing
scrapy shell "https://www.oddsportal.com/basketball/usa/nba/results/"

# In shell
from scrapers.odds_scraper.odds_scraper.spiders.odds_portal.utils.league_discovery_parser import LeagueDiscoveryParser
parser = LeagueDiscoveryParser("https://www.oddsportal.com/basketball/usa/nba")
discovery = parser.parse_discovery_page(response)
```