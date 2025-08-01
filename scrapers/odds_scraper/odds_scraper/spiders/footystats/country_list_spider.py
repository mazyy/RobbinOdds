from typing import Dict, Any, Optional
from .base_spider import FootyStatsBaseSpider
from ...items.footystats.country_list_items import (
    CountryListItem,
    validate_country_list_item,
    create_country_list_item
)

class CountryListSpider(FootyStatsBaseSpider):
    """
    Spider for FootyStats /country-list endpoint
    
    Extracts available countries with:
    - Country ID
    - ISO code  
    - Country name
    - ISO number
    
    Usage:
    scrapy crawl footystats_country_list -O countries.json
    scrapy crawl footystats_country_list -a api_key=your_key
    """
    
    name = "footystats_country_list"
    endpoint_name = "country-list"
    allowed_domains = ["api.football-data-api.com"]
    
    def parse_data_item(self, item_data: Dict[str, Any]) -> Optional[CountryListItem]:
        """
        Parse individual country from API response
        
        Args:
            item_data: Single country object from data[] array
            
        Returns:
            CountryListItem or None if invalid
        """
        # Validate country data
        if not validate_country_list_item(item_data):
            country_name = item_data.get('country', 'Unknown')
            self.logger.warning(f" Invalid country data: {country_name}")
            return None
        
        try:
            # Create country item using helper function
            country_item = create_country_list_item(item_data)
            
            # Log progress
            country_name = country_item.get('country', 'Unknown')
            country_id = country_item.get('id', 'Unknown') 
            self.logger.debug(f" Processed country: {country_name} (ID: {country_id})")
            
            return country_item
            
        except Exception as e:
            country_name = item_data.get('country', 'Unknown')
            self.logger.error(f" Error processing country {country_name}: {e}")
            return None
