# Default: Only 1X2 Full Time
scrapy crawl oddsportal_match_spider -a match_url="https://www.oddsportal.com/football/europe/champions-league/psg-inter-6LTndcTP"

# Specific bet types and scopes
scrapy crawl oddsportal_match_spider -a match_url="https://www.oddsportal.com/football/europe/champions-league/psg-inter-6LTndcTP" -a bet_types="1,2,5" -a scopes="2,3"

# All bet types for full time only
scrapy crawl oddsportal_match_spider -a match_url="https://www.oddsportal.com/football/europe/champions-league/psg-inter-6LTndcTP" -a scopes="2"

# To save output
scrapy crawl oddsportal_match_spider -O odds_data.json -a match_url="https://www.oddsportal.com/football/europe/champions-league/psg-inter-6LTndcTP"