# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
Sports betting odds scraping platform that extracts data from FootyStats API and OddsPortal website. Uses Scrapy framework with Airflow orchestration for automated data collection.

## Common Commands

### Scrapy Operations
```bash
# Navigate to scrapy project directory
cd scrapers/odds_scraper

# List all available spiders
scrapy list

# Run FootyStats spiders
scrapy crawl footystats_country_list -a api_key="your_key"
scrapy crawl footystats_league_list -a api_key="your_key" -a country="England"
scrapy crawl footystats_league_matches -a api_key="your_key" -a league_id="2790"

# Run OddsPortal spiders (decoupled workflow)
# Step 1: Get match metadata
scrapy crawl oddsportal_match_spider -O match_data.json \
  -a match_url="https://www.oddsportal.com/football/england/premier-league/arsenal-fulham-vRiDNL8C/"

# Step 2: Extract odds using metadata parameters
scrapy crawl oddsportal_odds_spider -O odds_data.json \
  -a match_url="https://www.oddsportal.com/football/england/premier-league/arsenal-fulham-vRiDNL8C/" \
  -a match_id="vRiDNL8C" \
  -a xhashf="%79%6a%63%34%63" \
  -a sport_id="1" \
  -a is_started="true"

# Save output to files
scrapy crawl <spider_name> -O output.json -a param="value"

# Debug with scrapy shell
scrapy shell "https://example.com"
```

### Docker & Airflow Operations
```bash
# Start Airflow stack
docker-compose up -d

# Access Airflow webserver
# URL: http://localhost:8080 (airflow:airflow)

# View logs
docker-compose logs airflow-webserver
docker-compose logs airflow-scheduler

# Stop services
docker-compose down
```

## Architecture

### Spider Architecture
The project uses two distinct spider architectures:

**FootyStats Spiders**: API-based spiders inheriting from `FootyStatsBaseSpider`
- Automatic pagination handling
- Built-in rate limiting and error handling
- Request statistics tracking
- Handles both list and single object API responses

**OddsPortal Spiders**: Web scraping with decoupled workflow
- `BaseSpider`: Abstract template with parse → follow pattern
- Match spider: Extracts metadata (match_id, xhashf, sport_id)
- Odds spider: Uses metadata to fetch odds directly

### Data Pipeline Flow
1. **FootyStats**: API key → Base spider → Auto-pagination → Item yield
2. **OddsPortal**: Match URL → Match metadata → Odds extraction → Item yield
3. **Airflow**: Orchestrates spider execution and scheduling
4. **Docker**: Containerized deployment with PostgreSQL + Redis

### Key Configuration
- `ROBOTSTXT_OBEY = False` in settings.py
- Custom rate limiting per spider type
- Async reactor for performance
- UTF-8 feed encoding

## Spider Parameters

### FootyStats Required Parameters
- `api_key`: API authentication key
- Additional params vary by endpoint (country, league_id, team_id, etc.)

### OddsPortal Required Parameters
**Match Spider**: `match_url`
**Odds Spider**: `match_url`, `match_id`, `xhashf`, `sport_id`
**Optional**: `version_id`, `bet_types`, `scopes`, `is_started`

### Common Bet Types
- `1`: 1X2 (Home/Draw/Away)
- `2`: Over/Under
- `5`: Asian Handicap
- `8`: Correct Score

### Common Scopes
- `2`: Full Time
- `3`: First Half
- `4`: Second Half