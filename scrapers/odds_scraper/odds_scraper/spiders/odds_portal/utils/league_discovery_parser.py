from typing import Dict, List, Any, Optional
from odds_scraper.items.odds_portal.league_items import (
    SportItem, CountryItem, LeagueItem, SeasonItem, LeagueDiscoveryItem,
    SportLoader, CountryLoader, LeagueLoader, SeasonLoader, LeagueDiscoveryLoader
)
import re
from urllib.parse import urlparse, urljoin

class LeagueDiscoveryParser:
    """Parser for league discovery data from OddsPortal"""
    
    def __init__(self, league_url: str):
        """
        Initialize parser with league URL
        
        Args:
            league_url: Base league URL
        """
        self.league_url = league_url.rstrip('/')
        self._parse_url_components()
    
    def _parse_url_components(self):
        """Extract sport, country, and league from URL"""
        # URL format: https://www.oddsportal.com/{sport}/{country}/{league}/
        url_parts = self.league_url.split('/')
        self.sport_slug = url_parts[-3] if len(url_parts) >= 3 else 'unknown'
        self.country_slug = url_parts[-2] if len(url_parts) >= 2 else 'unknown'
        self.league_slug = url_parts[-1] if url_parts else 'unknown'
    
    def parse_discovery_page(self, response) -> LeagueDiscoveryItem:
        """
        Parse the main league page for discovery information
        
        Args:
            response: Scrapy response object
            
        Returns:
            LeagueDiscoveryItem with complete league information
        """
        discovery_loader = LeagueDiscoveryLoader()
        
        # Parse sport
        sport_item = self._parse_sport(response)
        discovery_loader.add_value('sport', sport_item)
        
        # Parse country
        country_item = self._parse_country(response)
        discovery_loader.add_value('country', country_item)
        
        # Parse league
        league_item = self._parse_league(response)
        discovery_loader.add_value('league', league_item)
        
        # Parse seasons
        seasons = self._parse_seasons(response, league_item.get('league_id'))
        discovery_loader.add_value('seasons', seasons)
        discovery_loader.add_value('total_seasons', len(seasons))
        
        # Metadata
        discovery_loader.add_value('discovery_timestamp', None)
        discovery_loader.add_value('discovery_url', response.url)
        
        return discovery_loader.load_item()
    
    def _parse_sport(self, response) -> SportItem:
        """Extract sport information"""
        loader = SportLoader()
        
        # Extract sport ID from page scripts
        sport_id = self._extract_from_script(response, r'"sid"\s*:\s*(\d+)')
        if not sport_id:
            sport_id = self._extract_from_script(response, r'sport[/_-](\d+)')
        
        loader.add_value('sport_id', sport_id)
        loader.add_value('sport_name', self.sport_slug.title())
        loader.add_value('sport_url_slug', self.sport_slug)
        
        return loader.load_item()
    
    def _parse_country(self, response) -> CountryItem:
        """Extract country information"""
        loader = CountryLoader()
        
        # Country ID might be ISO code or custom ID
        country_id = self.country_slug.upper()[:3]  # Simple approach
        
        loader.add_value('country_id', country_id)
        loader.add_value('country_name', self.country_slug.title())
        loader.add_value('country_url_slug', self.country_slug)
        
        # Determine region based on country (you can expand this)
        region_map = {
            'usa': 'North America',
            'canada': 'North America',
            'england': 'Europe',
            'spain': 'Europe',
            'germany': 'Europe',
            'france': 'Europe',
            'italy': 'Europe',
            'brazil': 'South America',
            'argentina': 'South America',
            'australia': 'Oceania',
            'japan': 'Asia',
            'china': 'Asia',
        }
        region = region_map.get(self.country_slug, 'Unknown')
        loader.add_value('region', region)
        
        return loader.load_item()
    
    def _parse_league(self, response) -> LeagueItem:
        """Extract league information"""
        loader = LeagueLoader()
        
        # Extract league ID (encoded tournament ID)
        league_id = self._extract_league_id(response)
        
        loader.add_value('league_id', league_id)
        loader.add_value('league_name', self.league_slug.replace('-', ' ').upper())
        loader.add_value('league_url_slug', self.league_slug)
        loader.add_value('league_url', self.league_url)
        
        # Sport info
        sport_id = self._extract_from_script(response, r'"sid"\s*:\s*(\d+)')
        loader.add_value('sport_id', sport_id)
        loader.add_value('sport_name', self.sport_slug.title())
        
        # Country info
        loader.add_value('country_id', self.country_slug.upper()[:3])
        loader.add_value('country_name', self.country_slug.title())
        
        # Determine league type
        league_type = self._determine_league_type(self.league_slug, response)
        loader.add_value('league_type', league_type)
        loader.add_value('is_active', True)  # Assume active if we can access it
        
        return loader.load_item()
    
    def _parse_seasons(self, response, league_id: str) -> List[SeasonItem]:
        """Extract all available seasons"""
        seasons = []
        
        # Check for current season first
        current_season = self._parse_current_season(response, league_id)
        if current_season:
            seasons.append(current_season)
        
        # Method 1: Season dropdown
        season_options = response.css('select#season-select option, select.season-select option')
        for option in season_options:
            season_url = option.css('::attr(value)').get()
            season_text = option.css('::text').get()
            
            if season_url and season_url != '#':
                season_item = self._create_season_from_dropdown(
                    season_url, season_text, response.url, league_id
                )
                if season_item:
                    seasons.append(season_item)
        
        # Method 2: Archive/history links
        archive_links = response.css('a[href*="-20"][href*="/results/"]::attr(href)').getall()
        for link in archive_links:
            season_item = self._create_season_from_link(link, response.url, league_id)
            if season_item:
                seasons.append(season_item)
        
        # Method 3: Script patterns
        seasons.extend(self._extract_seasons_from_scripts(response, league_id))
        
        # Remove duplicates based on season_id
        seen = set()
        unique_seasons = []
        for season in seasons:
            if season.get('season_id') not in seen:
                seen.add(season.get('season_id'))
                unique_seasons.append(season)
        
        # Sort by year (newest first)
        unique_seasons.sort(
            key=lambda x: x.get('start_year', 0) if x.get('start_year') else float('inf'),
            reverse=True
        )
        
        return unique_seasons
    
    def _parse_current_season(self, response, league_id: str) -> Optional[SeasonItem]:
        """Parse current season information"""
        loader = SeasonLoader()
        
        loader.add_value('season_id', 'current')
        loader.add_value('season_name', f"{self.league_slug.upper()} Current Season")
        loader.add_value('season_url', f"{self.league_url}/results/")
        loader.add_value('league_id', league_id)
        loader.add_value('league_name', self.league_slug.upper())
        loader.add_value('is_current', True)
        loader.add_value('has_results', True)
        
        # Check if fixtures page exists
        has_fixtures = bool(response.css('a[href*="/fixtures/"], a[href$="/"]').get())
        loader.add_value('has_fixtures', has_fixtures)
        
        return loader.load_item()
    
    def _create_season_from_dropdown(self, season_url: str, season_text: str,
                                   base_url: str, league_id: str) -> Optional[SeasonItem]:
        """Create season item from dropdown option"""
        full_url = urljoin(base_url, season_url)
        
        # Extract season year from URL
        match = re.search(r'-(\d{4}-\d{4})', full_url)
        if not match:
            return None
        
        season_year = match.group(1)
        
        loader = SeasonLoader()
        loader.add_value('season_id', season_year)
        loader.add_value('season_name', season_text or f"{self.league_slug.upper()} {season_year}")
        loader.add_value('season_url', full_url)
        loader.add_value('league_id', league_id)
        loader.add_value('league_name', self.league_slug.upper())
        loader.add_value('is_current', False)
        loader.add_value('start_year', season_year)
        loader.add_value('end_year', season_year)
        loader.add_value('has_results', '/results/' in full_url)
        
        return loader.load_item()
    
    def _create_season_from_link(self, link: str, base_url: str,
                               league_id: str) -> Optional[SeasonItem]:
        """Create season item from archive link"""
        full_url = urljoin(base_url, link)
        
        # Extract season year
        match = re.search(rf'{self.league_slug}-(\d{{4}}-\d{{4}})', full_url)
        if not match:
            return None
        
        season_year = match.group(1)
        
        loader = SeasonLoader()
        loader.add_value('season_id', season_year)
        loader.add_value('season_name', f"{self.league_slug.upper()} {season_year}")
        loader.add_value('season_url', full_url)
        loader.add_value('league_id', league_id)
        loader.add_value('league_name', self.league_slug.upper())
        loader.add_value('is_current', False)
        loader.add_value('start_year', season_year)
        loader.add_value('end_year', season_year)
        loader.add_value('has_results', '/results/' in full_url)
        
        return loader.load_item()
    
    def _extract_seasons_from_scripts(self, response, league_id: str) -> List[SeasonItem]:
        """Extract seasons from JavaScript code"""
        seasons = []
        
        # Combine all scripts
        all_scripts = ' '.join(response.xpath('//script/text()').getall())
        
        # Pattern for seasons in scripts
        season_pattern = rf'{self.league_slug}-(\d{{4}}-\d{{4}})'
        found_seasons = re.findall(season_pattern, all_scripts)
        
        for season_year in set(found_seasons):  # Remove duplicates
            loader = SeasonLoader()
            loader.add_value('season_id', season_year)
            loader.add_value('season_name', f"{self.league_slug.upper()} {season_year}")
            loader.add_value('season_url', f"{self.league_url}-{season_year}/results/")
            loader.add_value('league_id', league_id)
            loader.add_value('league_name', self.league_slug.upper())
            loader.add_value('is_current', False)
            loader.add_value('start_year', season_year)
            loader.add_value('end_year', season_year)
            loader.add_value('has_results', True)
            
            seasons.append(loader.load_item())
        
        return seasons
    
    def _extract_league_id(self, response) -> Optional[str]:
        """Extract encoded league/tournament ID"""
        # Try multiple patterns
        patterns = [
            r'"id"\s*:\s*"([^"]+)"',  # JSON style
            r'tournament[/-]([a-zA-Z0-9]+)',  # URL pattern
            r'encodeEventId["\']?\s*[:=]\s*["\']([^"\']+)',  # Event ID pattern
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response.text)
            if match:
                return match.group(1)
        
        # Fallback: use league slug
        return self.league_slug
    
    def _extract_from_script(self, response, pattern: str) -> Optional[str]:
        """Extract value from script tags using regex"""
        all_scripts = ' '.join(response.xpath('//script/text()').getall())
        match = re.search(pattern, all_scripts)
        return match.group(1) if match else None
    
    def _determine_league_type(self, league_slug: str, response) -> str:
        """Determine the type of league"""
        # Check URL and content for clues
        if any(word in league_slug.lower() for word in ['cup', 'copa', 'coupe']):
            return 'cup'
        elif any(word in league_slug.lower() for word in ['champions', 'europa', 'libertadores']):
            return 'international'
        else:
            return 'domestic'