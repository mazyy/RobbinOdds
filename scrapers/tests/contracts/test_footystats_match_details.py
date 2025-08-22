"""
Test contracts for FootyStats Match Details Spider using TDD approach.

This module tests the match details spider with mock API responses,
validating comprehensive match statistics extraction and data processing.
"""

import pytest
import json
from unittest.mock import Mock, patch
from scrapy.http import Request

# Import the spider and items to test
try:
    from odds_scraper.spiders.footystats.match_details_spider import FootyStatsMatchDetailsSpider
    from odds_scraper.items.footystats.match_details_items import MatchDetailsItem
except ImportError:
    # Fallback for testing without full project structure
    FootyStatsMatchDetailsSpider = None
    MatchDetailsItem = None

from test_footystats_spiders import FootyStatsTestBase


class TestFootyStatsMatchDetailsSpider(FootyStatsTestBase):
    """Test contracts for Match Details Spider"""
    
    @pytest.fixture
    def spider(self):
        """Initialize spider with test parameters"""
        if FootyStatsMatchDetailsSpider is None:
            pytest.skip("Spider not available for testing")
        
        return self.get_spider_instance(
            FootyStatsMatchDetailsSpider,
            match_id='579101',
            api_key='test_key'
        )
    
    @pytest.fixture
    def mock_match_response(self, sample_responses):
        """Create mock match details API response"""
        endpoint_data = sample_responses['match_details']
        return self.create_json_response(
            url=endpoint_data['endpoint'],
            data=endpoint_data['response']
        )
    
    def test_spider_initialization(self, spider):
        """Test spider initializes with correct parameters"""
        assert spider.match_id == '579101'
        assert spider.api_key == 'test_key'
        assert spider.name == 'footystats_match_details'
    
    def test_spider_requires_match_id(self):
        """Test spider raises error without match_id parameter"""
        if FootyStatsMatchDetailsSpider is None:
            pytest.skip("Spider not available for testing")
        
        with pytest.raises(ValueError, match="match_id is required"):
            self.get_spider_instance(FootyStatsMatchDetailsSpider, api_key='test')
    
    def test_start_requests_generation(self, spider):
        """Test spider generates correct start requests"""
        requests = list(spider.start_requests())
        
        assert len(requests) == 1
        request = requests[0]
        
        assert isinstance(request, Request)
        assert 'api.football-data-api.com' in request.url
        assert 'match_id=579101' in request.url
        assert 'key=test_key' in request.url
        assert request.callback == spider.parse
    
    def test_parse_basic_match_info(self, spider, mock_match_response):
        """Test extraction of basic match information"""
        items = list(spider.parse(mock_match_response))
        
        assert len(items) == 1
        item = items[0]
        
        # Verify item type
        if MatchDetailsItem:
            assert isinstance(item, MatchDetailsItem)
        
        # Verify basic match fields
        required_fields = [
            'match_id', 'home_team_id', 'away_team_id', 
            'season', 'status'
        ]
        self.assert_item_fields(item, required_fields, 'MatchDetails')
        
        # Verify field values match sample data
        assert item['match_id'] == 579101
        assert item['home_team_id'] == 251
        assert item['away_team_id'] == 145
        assert item['season'] == '2019/2020'
        assert item['status'] == 'complete'
    
    def test_parse_goal_statistics(self, spider, mock_match_response):
        """Test extraction of goal-related statistics"""
        items = list(spider.parse(mock_match_response))
        item = items[0]
        
        # Verify goal counts
        assert item['home_goal_count'] == 3
        assert item['away_goal_count'] == 0
        assert item['total_goal_count'] == 3
        
        # Verify goal timing arrays
        if 'home_goals' in item:
            assert isinstance(item['home_goals'], list)
            assert len(item['home_goals']) == 3
            assert '17' in item['home_goals']
            assert '43' in item['home_goals']
            assert '44' in item['home_goals']
        
        if 'away_goals' in item:
            assert isinstance(item['away_goals'], list)
            assert len(item['away_goals']) == 0
    
    def test_parse_match_statistics_team_a(self, spider, mock_match_response):
        """Test extraction of team A (home) match statistics"""
        items = list(spider.parse(mock_match_response))
        item = items[0]
        
        # Verify team A statistics
        team_a_stats = {
            'team_a_corners': 7,
            'team_a_shots_on_target': 7,
            'team_a_shots_off_target': 7,
            'team_a_shots': 14,
            'team_a_fouls': 8,
            'team_a_possession': 45,
            'team_a_yellow_cards': 1,
            'team_a_red_cards': 0,
            'team_a_offsides': 1
        }
        
        for field, expected_value in team_a_stats.items():
            if field in item:
                assert item[field] == expected_value, \
                    f"Field '{field}' should be {expected_value}, got {item[field]}"
    
    def test_parse_match_statistics_team_b(self, spider, mock_match_response):
        """Test extraction of team B (away) match statistics"""
        items = list(spider.parse(mock_match_response))
        item = items[0]
        
        # Verify team B statistics
        team_b_stats = {
            'team_b_corners': 6,
            'team_b_shots_on_target': 0,
            'team_b_shots_off_target': 6,
            'team_b_shots': 6,
            'team_b_fouls': 12,
            'team_b_possession': 55,
            'team_b_yellow_cards': 2,
            'team_b_red_cards': 0,
            'team_b_offsides': 0
        }
        
        for field, expected_value in team_b_stats.items():
            if field in item:
                assert item[field] == expected_value, \
                    f"Field '{field}' should be {expected_value}, got {item[field]}"
    
    def test_parse_totals_calculation(self, spider, mock_match_response):
        """Test that total statistics are correctly calculated/extracted"""
        items = list(spider.parse(mock_match_response))
        item = items[0]
        
        # Verify total corner count
        assert item['total_corner_count'] == 13
        
        # Verify possession adds up to 100%
        if 'team_a_possession' in item and 'team_b_possession' in item:
            total_possession = item['team_a_possession'] + item['team_b_possession']
            assert total_possession == 100, f"Total possession should be 100%, got {total_possession}"
    
    def test_parse_match_officials(self, spider, mock_match_response):
        """Test extraction of match officials information"""
        items = list(spider.parse(mock_match_response))
        item = items[0]
        
        # Verify officials
        officials_fields = {
            'referee_id': 715,
            'coach_a_id': 497,
            'coach_b_id': 197
        }
        
        for field, expected_value in officials_fields.items():
            if field in item:
                assert item[field] == expected_value
    
    def test_parse_venue_information(self, spider, mock_match_response):
        """Test extraction of venue information"""
        items = list(spider.parse(mock_match_response))
        item = items[0]
        
        # Verify venue information
        if 'stadium_name' in item:
            assert item['stadium_name'] == 'Bramall Lane (Sheffield)'
        
        if 'stadium_location' in item:
            assert item['stadium_location'] == 'Sheffield, England'
    
    def test_parse_betting_odds_1x2(self, spider, mock_match_response):
        """Test extraction of 1X2 betting odds"""
        items = list(spider.parse(mock_match_response))
        item = items[0]
        
        # Verify 1X2 odds
        odds_1x2 = {
            'odds_ft_1': 2.4,   # Home win
            'odds_ft_x': 3.15,  # Draw
            'odds_ft_2': 3.35   # Away win
        }
        
        for field, expected_value in odds_1x2.items():
            if field in item:
                assert abs(item[field] - expected_value) < 0.01, \
                    f"Odds field '{field}' should be {expected_value}, got {item[field]}"
    
    def test_parse_betting_odds_over_under(self, spider, mock_match_response):
        """Test extraction of over/under betting odds"""
        items = list(spider.parse(mock_match_response))
        item = items[0]
        
        # Verify over/under odds
        over_under_odds = {
            'odds_ft_over05': 1.09,
            'odds_ft_over15': 1.48,
            'odds_ft_over25': 2.45,
            'odds_ft_under15': 2.65,
            'odds_ft_under25': 1.56
        }
        
        for field, expected_value in over_under_odds.items():
            if field in item:
                assert abs(item[field] - expected_value) < 0.01, \
                    f"O/U odds field '{field}' should be {expected_value}, got {item[field]}"
    
    def test_parse_btts_odds(self, spider, mock_match_response):
        """Test extraction of Both Teams to Score odds"""
        items = list(spider.parse(mock_match_response))
        item = items[0]
        
        # Verify BTTS odds
        if 'btts_yes' in item:
            assert abs(item['btts_yes'] - 1.95) < 0.01
        
        if 'btts_no' in item:
            assert abs(item['btts_no'] - 1.85) < 0.01
    
    def test_parse_match_timing(self, spider, mock_match_response):
        """Test extraction of match timing information"""
        items = list(spider.parse(mock_match_response))
        item = items[0]
        
        # Verify timing fields
        timing_fields = {
            'date_unix': 1573927200,
            'finished_unix': 1573934400,
            'game_week': 11,
            'round_id': 50055
        }
        
        for field, expected_value in timing_fields.items():
            if field in item:
                assert item[field] == expected_value
    
    def test_field_type_validation(self, spider, mock_match_response):
        """Test that extracted fields have correct data types"""
        items = list(spider.parse(mock_match_response))
        item = items[0]
        
        # Define expected field types
        field_types = {
            'match_id': int,
            'home_team_id': int,
            'away_team_id': int,
            'home_goal_count': int,
            'away_goal_count': int,
            'total_goal_count': int,
            'team_a_corners': int,
            'team_b_corners': int,
            'team_a_possession': (int, float),
            'team_b_possession': (int, float),
            'odds_ft_1': (int, float),
            'odds_ft_x': (int, float),
            'odds_ft_2': (int, float),
            'season': str,
            'status': str,
            'stadium_name': str
        }
        
        self.assert_item_types(item, field_types, 'MatchDetails')
    
    def test_handle_missing_optional_fields(self, spider):
        """Test handling of response with missing optional fields"""
        minimal_data = {
            'id': 579101,
            'homeID': 251,
            'awayID': 145,
            'status': 'complete',
            'homeGoalCount': 3,
            'awayGoalCount': 0
            # Missing many optional fields like odds, possession, etc.
        }
        
        minimal_response = self.create_json_response(
            'https://api.test.com/match',
            minimal_data
        )
        
        items = list(spider.parse(minimal_response))
        assert len(items) == 1
        
        item = items[0]
        # Should have basic fields
        assert item['match_id'] == 579101
        assert item['home_team_id'] == 251
        assert item['away_team_id'] == 145
    
    def test_handle_invalid_match_data(self, spider):
        """Test handling of invalid match data"""
        invalid_data = {
            'id': 'invalid_id',  # Should be integer
            'homeID': None,      # Required field is None
            'status': 'complete'
        }
        
        invalid_response = self.create_json_response(
            'https://api.test.com/match',
            invalid_data
        )
        
        items = list(spider.parse(invalid_response))
        # Should handle invalid data gracefully - either skip or handle with defaults
        assert isinstance(items, list)
    
    def test_parse_metadata_fields(self, spider, mock_match_response):
        """Test that metadata fields are correctly set"""
        items = list(spider.parse(mock_match_response))
        item = items[0]
        
        # Check metadata fields
        assert 'scraped_at' in item
        assert 'schema_version' in item
        assert 'spider_name' in item
        
        # Verify spider name
        if 'spider_name' in item:
            assert spider.name in item['spider_name']


class TestMatchDetailsSpiderAdvanced(FootyStatsTestBase):
    """Advanced test scenarios for match details spider"""
    
    def test_parse_live_match_data(self, sample_responses):
        """Test parsing of live/ongoing match data"""
        if FootyStatsMatchDetailsSpider is None:
            pytest.skip("Spider not available for testing")
        
        # Create live match data
        live_match_data = sample_responses['match_details']['response'].copy()
        live_match_data['status'] = 'live'
        live_match_data['finished_unix'] = None
        
        spider = self.get_spider_instance(
            FootyStatsMatchDetailsSpider,
            match_id='579101',
            api_key='test_key'
        )
        
        live_response = self.create_json_response(
            'https://api.test.com/match',
            live_match_data
        )
        
        items = list(spider.parse(live_response))
        assert len(items) == 1
        
        item = items[0]
        assert item['status'] == 'live'
    
    def test_parse_postponed_match(self, sample_responses):
        """Test parsing of postponed match data"""
        if FootyStatsMatchDetailsSpider is None:
            pytest.skip("Spider not available for testing")
        
        # Create postponed match data
        postponed_data = {
            'id': 579102,
            'homeID': 251,
            'awayID': 145,
            'status': 'postponed',
            'homeGoalCount': 0,
            'awayGoalCount': 0
        }
        
        spider = self.get_spider_instance(
            FootyStatsMatchDetailsSpider,
            match_id='579102',
            api_key='test_key'
        )
        
        postponed_response = self.create_json_response(
            'https://api.test.com/match',
            postponed_data
        )
        
        items = list(spider.parse(postponed_response))
        assert len(items) == 1
        
        item = items[0]
        assert item['status'] == 'postponed'
        assert item['home_goal_count'] == 0
        assert item['away_goal_count'] == 0


class TestMatchDetailsSpiderIntegration(FootyStatsTestBase):
    """Integration tests for match details spider workflow"""
    
    def test_complete_workflow_with_comprehensive_data(self, sample_responses):
        """Test complete workflow with all possible data fields"""
        if FootyStatsMatchDetailsSpider is None:
            pytest.skip("Spider not available for testing")
        
        spider = self.get_spider_instance(
            FootyStatsMatchDetailsSpider,
            match_id='579101',
            api_key='test_key'
        )
        
        # Use comprehensive sample data
        response = self.create_json_response(
            'https://api.football-data-api.com/match',
            sample_responses['match_details']['response']
        )
        
        items = list(spider.parse(response))
        assert len(items) == 1
        
        item = items[0]
        
        # Verify comprehensive data extraction
        expected_categories = [
            'match_id', 'home_team_id', 'away_team_id',  # Basic info
            'home_goal_count', 'away_goal_count',        # Goals
            'team_a_shots', 'team_b_shots',              # Statistics
            'odds_ft_1', 'odds_ft_x', 'odds_ft_2',       # Odds
            'scraped_at', 'schema_version'               # Metadata
        ]
        
        for field in expected_categories:
            assert field in item, f"Expected field '{field}' missing from comprehensive item"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])