# FootyStats Spiders - User Guide

A comprehensive collection of Scrapy spiders for extracting football/soccer data from the FootyStats API. These spiders provide structured data for betting analytics, league analysis, and team performance tracking.

## Quick Start

### Prerequisites
- Python 3.11+
- Scrapy 2.11.2+
- FootyStats API key (get one at https://footystats.org/api)

### Basic Usage
```bash
# Install dependencies
pip install scrapy requests

# Run a spider with example key (limited functionality)
scrapy crawl footystats_league_table -a api_key=example -a season_id=1625

# Run with your API key for full access
scrapy crawl footystats_league_table -a api_key=your_real_key -a season_id=2012 -O output.json
```

## Available Spiders

### Core Data Spiders

#### 1. Country List (`footystats_country_list`)
Extract available countries for league data.

**Parameters**: None (except API key)

**Usage**:
```bash
scrapy crawl footystats_country_list -a api_key=your_key -O countries.json
```

**Output**: Country ID, name, ISO code, flag URL

---

#### 2. League List (`footystats_league_list`) 
Extract leagues available in a specific country.

**Required Parameters**:
- `country_id` - Country identifier (e.g., "1" for England)

**Usage**:
```bash
scrapy crawl footystats_league_list -a api_key=your_key -a country_id=1 -O leagues.json
```

**Output**: League ID, name, country, tier level, logo

---

#### 3. League Matches (`footystats_league_matches`)
Extract all matches from a league season.

**Required Parameters**:
- `season_id` - Season identifier (e.g., "2012" for current EPL season)

**Usage**:
```bash
scrapy crawl footystats_league_matches -a api_key=your_key -a season_id=2012 -O matches.json
```

**Output**: Match ID, teams, date, result, venue

---

### League Analysis Spiders

#### 4. League Table (`footystats_league_table`)
Extract current league standings with comprehensive statistics.

**Required Parameters**:
- `season_id` - Season identifier

**Usage**:
```bash
# Current Premier League table
scrapy crawl footystats_league_table -a api_key=your_key -a season_id=2012

# Save to CSV format
scrapy crawl footystats_league_table -a api_key=your_key -a season_id=2012 -O table.csv
```

**Output**: Team positions, points, wins/draws/losses, goals, form, venue-specific stats

---

#### 5. BTTS Statistics (`footystats_btts_stats`)
Extract Both Teams To Score statistics for betting analysis.

**Required Parameters**:
- `season_id` - Season identifier

**Usage**:
```bash
scrapy crawl footystats_btts_stats -a api_key=your_key -a season_id=2012 -O btts.json
```

**Output**: BTTS percentages by venue, timing, goal thresholds, recent form

---

#### 6. Over/Under Statistics (`footystats_over_stats`)
Extract Over/Under goal statistics for various thresholds.

**Required Parameters**:
- `season_id` - Season identifier

**Optional Parameters**:
- `threshold` - Focus on specific threshold (e.g., "2.5")

**Usage**:
```bash
# All thresholds
scrapy crawl footystats_over_stats -a api_key=your_key -a season_id=2012

# Focus on Over 2.5 goals
scrapy crawl footystats_over_stats -a api_key=your_key -a season_id=2012 -a threshold=2.5
```

**Output**: Over/Under percentages for 0.5-5.5 goals, venue breakdowns, timing analysis

---

### Team Analysis Spiders

#### 7. Team Recent Form (`footystats_team_last`)
Analyze recent team performance over last N games.

**Required Parameters**:
- `team_id` - Team identifier (e.g., "2" for Arsenal)

**Optional Parameters**:
- `games` - Number of recent games (default: "5")

**Usage**:
```bash
# Last 5 games
scrapy crawl footystats_team_last -a api_key=your_key -a team_id=2

# Last 10 games
scrapy crawl footystats_team_last -a api_key=your_key -a team_id=2 -a games=10
```

**Output**: Win/draw/loss record, goals, form breakdown, BTTS/over-under performance

---

#### 8. Head-to-Head Analysis (`footystats_team_vs_team`)
Extract historical matchup data between two teams.

**Required Parameters**:
- `home_id` - Home team identifier
- `away_id` - Away team identifier (must be different)

**Usage**:
```bash
# Arsenal vs Chelsea
scrapy crawl footystats_team_vs_team -a api_key=your_key -a home_id=2 -a away_id=6

# Liverpool vs Manchester United
scrapy crawl footystats_team_vs_team -a api_key=your_key -a home_id=3 -a away_id=1
```

**Output**: Historical record, goal stats, venue breakdown, recent form

---

### Metadata Spiders

#### 9. Season Information (`footystats_season_info`)
Extract comprehensive season metadata and competition details.

**Required Parameters**:
- `season_id` - Season identifier

**Usage**:
```bash
scrapy crawl footystats_season_info -a api_key=your_key -a season_id=2012 -O season.json
```

**Output**: Season timeline, competition structure, current leaders, statistics

---

## Output Formats

All spiders support multiple output formats:

```bash
# JSON (default)
-O output.json

# JSON Lines (for large datasets)
-O output.jsonl

# CSV (for spreadsheet analysis)
-O output.csv

# Print to console
# (no output parameter needed)
```

## Common Usage Patterns

### Comprehensive League Analysis
```bash
# Get complete league overview
scrapy crawl footystats_league_table -a api_key=your_key -a season_id=2012 -O table.json
scrapy crawl footystats_btts_stats -a api_key=your_key -a season_id=2012 -O btts.json
scrapy crawl footystats_over_stats -a api_key=your_key -a season_id=2012 -O over.json
```

### Team Performance Analysis
```bash
# Analyze top teams' recent form
scrapy crawl footystats_team_last -a api_key=your_key -a team_id=2 -a games=10 -O arsenal.json
scrapy crawl footystats_team_last -a api_key=your_key -a team_id=6 -a games=10 -O chelsea.json

# Head-to-head for upcoming fixture
scrapy crawl footystats_team_vs_team -a api_key=your_key -a home_id=2 -a away_id=6 -O h2h.json
```

### Batch Processing Multiple Seasons
```bash
# Historical analysis across seasons
for season in 1625 2012 2790; do
    scrapy crawl footystats_league_table -a api_key=your_key -a season_id=$season -O table_$season.json
done
```

## API Rate Limits

- **Automatic rate limiting**: 2-second delays between requests
- **Daily limit**: 1800 requests per day for free tier
- **Shared quota**: All spiders share the same rate limit
- **Auto-throttle**: Automatically adjusts speed based on response times

### Best Practices
```bash
# Monitor API usage
scrapy crawl footystats_league_table -a api_key=your_key -a season_id=2012 -L INFO

# Debug mode for troubleshooting
scrapy crawl footystats_team_vs_team -a api_key=example -a home_id=2 -a away_id=6 -L DEBUG
```

## Common Parameters Reference

### Team IDs (Major Teams)
- `1` - Manchester United
- `2` - Arsenal  
- `3` - Liverpool
- `6` - Chelsea
- `7` - Manchester City
- `8` - Tottenham

### Season IDs (Popular Leagues)
- `2012` - Premier League 2024/25
- `1625` - Premier League 2018/19
- `2790` - La Liga 2024/25
- `1674` - Bundesliga 2024/25

### Country IDs
- `1` - England
- `2` - Spain
- `3` - Germany
- `4` - Italy
- `5` - France

## Error Handling

### Common Issues

#### Missing Parameters
```bash
# ❌ This will fail
scrapy crawl footystats_league_table -a api_key=your_key

# ✅ This works
scrapy crawl footystats_league_table -a api_key=your_key -a season_id=2012
```

#### Invalid Team Comparison
```bash
# ❌ Same team comparison fails
scrapy crawl footystats_team_vs_team -a api_key=your_key -a home_id=2 -a away_id=2

# ✅ Different teams work
scrapy crawl footystats_team_vs_team -a api_key=your_key -a home_id=2 -a away_id=6
```

#### Rate Limit Exceeded
```
[2025-01-20 14:30:15] WARNING: Rate limit exceeded, will retry automatically
[2025-01-20 14:30:20] INFO: Retry attempt 1/3
```

### Debugging Commands

```bash
# Test parameter validation
scrapy crawl footystats_league_table -a api_key=example  # Should show clear error

# Full debug output
scrapy crawl footystats_btts_stats -a api_key=example -a season_id=1625 -L DEBUG

# Check spider contracts
scrapy check footystats_league_table
```

## Integration Examples

### Python Script Integration
```python
import subprocess
import json

def get_league_table(season_id, api_key):
    """Get league table data programmatically"""
    cmd = [
        'scrapy', 'crawl', 'footystats_league_table',
        '-a', f'api_key={api_key}',
        '-a', f'season_id={season_id}',
        '-O', 'temp_table.json'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        with open('temp_table.json', 'r') as f:
            return json.load(f)
    else:
        print(f"Error: {result.stderr}")
        return None

# Usage
table_data = get_league_table('2012', 'your_api_key')
if table_data:
    for team in table_data:
        print(f"{team['position']}. {team['name']}: {team['points']} points")
```

### Airflow DAG Integration
```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

dag = DAG(
    'footystats_daily_update',
    default_args={
        'owner': 'data_team',
        'retries': 1,
        'retry_delay': timedelta(minutes=5)
    },
    schedule_interval='@daily',
    start_date=datetime(2025, 1, 1)
)

# Extract league table daily
extract_table = BashOperator(
    task_id='extract_league_table',
    bash_command='scrapy crawl footystats_league_table -a api_key={{ var.value.footystats_key }} -a season_id=2012 -O /data/daily/table_{{ ds }}.json',
    dag=dag
)

# Extract BTTS stats weekly
extract_btts = BashOperator(
    task_id='extract_btts_stats',
    bash_command='scrapy crawl footystats_btts_stats -a api_key={{ var.value.footystats_key }} -a season_id=2012 -O /data/weekly/btts_{{ ds }}.json',
    dag=dag
)
```

## Data Structure Examples

### League Table Output
```json
{
  "team_id": 251,
  "name": "Sheffield United",
  "clean_name": "Sheffield United",
  "short_name": "Sheffield Utd",
  "position": 1,
  "played": 11,
  "wins": 8,
  "draws": 2,
  "losses": 1,
  "goals_for": 23,
  "goals_against": 7,
  "goal_difference": 16,
  "points": 26,
  "form": ["W", "W", "D", "W", "W"],
  "scraped_at": "2025-01-20T14:30:15",
  "schema_version": "1.0.0"
}
```

### BTTS Statistics Output
```json
{
  "season_id": "2012",
  "league_name": "Premier League",
  "total_matches": 220,
  "btts_matches": 132,
  "btts_percentage": 60.0,
  "btts_home_percentage": 58.2,
  "btts_away_percentage": 61.8,
  "btts_over_25_percentage": 45.5,
  "scraped_at": "2025-01-20T14:30:15"
}
```

## Support and Troubleshooting

### API Key Issues
- **Free tier**: Limited to 1800 requests/day with "example" key functionality
- **Paid tier**: Higher limits and full feature access
- **Key validation**: Test with `api_key=example` first

### Performance Optimization
- Use specific output files (`-O filename`) for large datasets
- Monitor with INFO logging to track API usage
- Process multiple seasons sequentially to respect rate limits

### Getting Help
- Check spider documentation: `scrapy crawl <spider_name> --help`
- View available spiders: `scrapy list | grep footystats`
- Test with debug logging: `-L DEBUG`

---

*For detailed implementation information, see the technical documentation in CLAUDE.md files.*