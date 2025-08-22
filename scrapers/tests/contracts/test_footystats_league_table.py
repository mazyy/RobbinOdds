"""
Test contracts for FootyStats League Table Spider using TDD approach.

This module tests the league table spider with mock API responses,
validating data extraction, item creation, and error handling.
"""

import pytest
import json
from unittest.mock import Mock, patch
from scrapy.http import Request

# Import the spider and items to test
try:
    from odds_scraper.spiders.footystats.league_table_spider import FootyStatsLeagueTableSpider
    from odds_scraper.items.footystats.league_table_items import LeagueTableItem
except ImportError:
    # Fallback for testing without full project structure
    FootyStatsLeagueTableSpider = None
    LeagueTableItem = None

from test_footystats_spiders import FootyStatsTestBase


class TestFootyStatsLeagueTableSpider(FootyStatsTestBase):
    """Test contracts for League Table Spider"""
    
    @pytest.fixture
    def spider(self):
        """Initialize spider with test parameters"""
        if FootyStatsLeagueTableSpider is None:
            pytest.skip("Spider not available for testing")
        
        return self.get_spider_instance(
            FootyStatsLeagueTableSpider,
            season_id='2012',
            api_key='test_key'
        )
    
    @pytest.fixture
    def mock_league_table_response(self, sample_responses):
        """Create mock league table API response"""
        endpoint_data = sample_responses['league_table']
        return self.create_json_response(
            url=endpoint_data['endpoint'],
            data=endpoint_data['response']
        )
    
    def test_spider_initialization(self, spider):
        """Test spider initializes with correct parameters"""
        assert spider.season_id == '2012'
        assert spider.api_key == 'test_key'
        assert spider.name == 'footystats_league_table'
    
    def test_spider_requires_season_id(self):
        """Test spider raises error without season_id parameter"""
        if FootyStatsLeagueTableSpider is None:
            pytest.skip("Spider not available for testing")
        
        with pytest.raises(ValueError, match="season_id is required"):
            self.get_spider_instance(FootyStatsLeagueTableSpider, api_key='test')
    
    def test_spider_requires_api_key(self):
        """Test spider raises error without api_key parameter"""
        if FootyStatsLeagueTableSpider is None:
            pytest.skip("Spider not available for testing")
        
        with pytest.raises(ValueError, match="api_key is required"):
            self.get_spider_instance(FootyStatsLeagueTableSpider, season_id='2012')
    
    def test_start_requests_generation(self, spider):
        """Test spider generates correct start requests"""
        requests = list(spider.start_requests())
        
        assert len(requests) == 1
        request = requests[0]
        
        assert isinstance(request, Request)
        assert 'api.football-data-api.com' in request.url
        assert 'season_id=2012' in request.url
        assert 'key=test_key' in request.url
        assert request.callback == spider.parse
    
    def test_parse_league_table_data(self, spider, mock_league_table_response):
        """Test extraction of league table data from API response"""
        items = list(spider.parse(mock_league_table_response))
        
        # Should yield exactly one item per team
        assert len(items) == 1
        item = items[0]
        
        # Verify item type
        if LeagueTableItem:
            assert isinstance(item, LeagueTableItem)
        
        # Verify required fields are present
        required_fields = [
            'team_id', 'name', 'position', 'played', 
            'wins', 'draws', 'losses', 'points'
        ]
        self.assert_item_fields(item, required_fields, 'LeagueTable')
        
        # Verify field values match sample data
        assert item['team_id'] == 251
        assert item['name'] == 'Sheffield United'
        assert item['position'] == 1
        assert item['points'] == 26
        assert item['played'] == 11
    
    def test_parse_team_statistics(self, spider, mock_league_table_response):
        """Test extraction of optional team statistics"""
        items = list(spider.parse(mock_league_table_response))
        item = items[0]
        
        # Check statistics fields if present
        stats_fields = [
            'shots_per_match', 'shots_on_target_per_match',
            'possession_percentage', 'pass_accuracy',
            'yellow_cards', 'red_cards'
        ]
        
        for field in stats_fields:
            if field in item:
                assert isinstance(item[field], (int, float)), \
                    f"Statistics field '{field}' should be numeric"
    
    def test_parse_goal_statistics(self, spider, mock_league_table_response):
        """Test extraction of goal-related statistics"""
        items = list(spider.parse(mock_league_table_response))
        item = items[0]
        
        # Verify goal statistics
        assert item['goals_for'] == 23
        assert item['goals_against'] == 7
        assert item['goal_difference'] == 16
        
        # Goal difference should equal goals_for - goals_against
        calculated_diff = item['goals_for'] - item['goals_against']
        assert item['goal_difference'] == calculated_diff
    
    def test_parse_form_data(self, spider, mock_league_table_response):
        """Test extraction of recent form data"""
        items = list(spider.parse(mock_league_table_response))
        item = items[0]
        
        if 'form' in item:
            form = item['form']
            assert isinstance(form, list)
            assert len(form) <= 5  # Should not exceed last 5 matches
            
            # Each form entry should be a valid result
            valid_results = ['W', 'D', 'L']
            for result in form:
                assert result in valid_results
    
    def test_parse_metadata_fields(self, spider, mock_league_table_response):
        """Test that metadata fields are correctly set"""
        items = list(spider.parse(mock_league_table_response))
        item = items[0]
        
        # Check metadata fields
        assert 'scraped_at' in item
        assert 'schema_version' in item
        assert 'spider_name' in item
        
        # Verify spider name
        if 'spider_name' in item:
            assert spider.name in item['spider_name']
    
    def test_handle_empty_response(self, spider):
        """Test graceful handling of empty API response"""
        empty_response = self.create_json_response(
            'https://api.test.com/league-tables',
            []  # Empty array
        )
        
        items = list(spider.parse(empty_response))
        assert len(items) == 0
    
    def test_handle_malformed_response(self, spider):
        """Test handling of malformed JSON response"""
        malformed_response = self.create_json_response(
            'https://api.test.com/league-tables',
            {'error': 'Invalid request'}
        )
        
        # Should not crash, might yield zero items or handle gracefully
        items = list(spider.parse(malformed_response))
        # Assert no exceptions were raised (test passes if we get here)
        assert isinstance(items, list)
    
    def test_handle_missing_required_fields(self, spider):
        """Test handling of response with missing required fields"""
        incomplete_data = [{
            'id': 251,
            'name': 'Sheffield United',
            # Missing position, points, etc.
        }]
        
        incomplete_response = self.create_json_response(
            'https://api.test.com/league-tables',
            incomplete_data
        )
        
        items = list(spider.parse(incomplete_response))
        # Should handle missing fields gracefully
        # Either skip the item or provide default values
        if len(items) > 0:
            item = items[0]
            assert 'team_id' in item
            assert 'name' in item
    
    def test_field_type_validation(self, spider, mock_league_table_response):
        """Test that extracted fields have correct data types"""
        items = list(spider.parse(mock_league_table_response))
        item = items[0]
        
        # Define expected field types
        field_types = {
            'team_id': int,
            'position': int,
            'played': int,
            'wins': int,
            'draws': int,
            'losses': int,
            'points': int,
            'goals_for': int,
            'goals_against': int,
            'goal_difference': int,
            'name': str,
            'clean_name': str,
            'short_name': str
        }
        
        self.assert_item_types(item, field_types, 'LeagueTable')
    
    def test_api_url_construction(self, spider):
        """Test that API URL is constructed correctly"""
        # Get the URL from start_requests
        requests = list(spider.start_requests())
        url = requests[0].url
        
        # Verify URL components
        assert 'api.football-data-api.com' in url
        assert 'league-tables' in url
        assert 'season_id=2012' in url
        assert 'key=test_key' in url
    
    def test_parse_with_statistics_parameter(self, spider, sample_responses):
        """Test parsing with include=stats parameter"""
        # Create response with statistics included
        response_with_stats = self.create_json_response(
            'https://api.football-data-api.com/league-tables?include=stats',
            sample_responses['league_table']['response']
        )
        
        items = list(spider.parse(response_with_stats))
        item = items[0]
        
        # Should include statistics fields when available
        if 'stats' in sample_responses['league_table']['response'][0]:
            stats_fields = ['shots_per_match', 'possession_percentage', 'pass_accuracy']
            for field in stats_fields:
                if field in item:
                    assert isinstance(item[field], (int, float))


# Integration test for the complete workflow
class TestLeagueTableSpiderIntegration(FootyStatsTestBase):
    """Integration tests for league table spider workflow"""
    
    def test_complete_spider_workflow(self, sample_responses):
        """Test complete spider workflow from request to item"""
        if FootyStatsLeagueTableSpider is None:
            pytest.skip("Spider not available for testing")
        
        spider = self.get_spider_instance(
            FootyStatsLeagueTableSpider,
            season_id='2012',
            api_key='test_key'
        )
        
        # Mock the API response
        api_response = self.create_json_response(
            'https://api.football-data-api.com/league-tables',
            sample_responses['league_table']['response']
        )
        
        # Process the response
        items = list(spider.parse(api_response))
        
        # Verify we got items
        assert len(items) > 0
        
        # Verify item structure
        item = items[0]
        assert 'team_id' in item
        assert 'name' in item
        assert 'position' in item
        assert 'points' in item
        
        # Verify metadata
        assert 'scraped_at' in item
        assert 'schema_version' in item


if __name__ == '__main__':
    pytest.main([__file__, '-v'])