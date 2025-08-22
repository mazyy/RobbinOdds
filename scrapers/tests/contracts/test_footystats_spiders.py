"""
Test contracts for FootyStats spiders using TDD approach.

This module provides base test infrastructure and common utilities
for testing FootyStats API spiders with mock responses.
"""

import pytest
import json
import os
from unittest.mock import Mock, patch
from scrapy.http import HtmlResponse, Request, TextResponse
from scrapy.utils.test import get_crawler
from datetime import datetime


class FootyStatsTestBase:
    """Base test class for FootyStats spiders with common utilities"""
    
    @pytest.fixture
    def sample_responses(self):
        """Load sample JSON responses for testing"""
        json_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 'resources', 'footystats', 'sample_responses.json'
        )
        with open(json_path, 'r') as f:
            return json.load(f)
    
    @pytest.fixture
    def mock_settings(self):
        """Mock spider settings"""
        return {
            'FOOTYSTATS_API_KEY': 'test_api_key',
            'FOOTYSTATS_BASE_URL': 'https://api.football-data-api.com',
            'USER_AGENT': 'Mozilla/5.0 (Test Spider)'
        }
    
    def create_json_response(self, url: str, data: dict, status: int = 200) -> TextResponse:
        """Create a mock JSON response"""
        request = Request(url=url)
        return TextResponse(
            url=url,
            body=json.dumps(data).encode('utf-8'),
            encoding='utf-8',
            request=request,
            status=status,
            headers={'Content-Type': 'application/json'}
        )
    
    def create_html_response(self, url: str, html_file: str) -> HtmlResponse:
        """Create a mock HTML response from saved file"""
        html_path = os.path.join(
            os.path.dirname(__file__),
            '..', 'resources', 'footystats', html_file
        )
        
        with open(html_path, 'rb') as f:
            body = f.read()
        
        request = Request(url=url)
        return HtmlResponse(
            url=url,
            body=body,
            encoding='utf-8',
            request=request
        )
    
    def assert_item_fields(self, item, required_fields: list, item_type: str):
        """Assert that item contains required fields"""
        assert item is not None, f"{item_type} item should not be None"
        
        for field in required_fields:
            assert field in item, f"Field '{field}' missing from {item_type} item"
            assert item[field] is not None, f"Field '{field}' should not be None in {item_type} item"
    
    def assert_item_types(self, item, field_types: dict, item_type: str):
        """Assert that item fields have correct types"""
        for field, expected_type in field_types.items():
            if field in item and item[field] is not None:
                assert isinstance(item[field], expected_type), \
                    f"Field '{field}' in {item_type} should be {expected_type}, got {type(item[field])}"
    
    def get_spider_instance(self, spider_class, **kwargs):
        """Get spider instance with mock crawler"""
        crawler = get_crawler(spider_class)
        spider = spider_class.from_crawler(crawler, **kwargs)
        return spider


class TestFootyStatsAPIResponse:
    """Test API response processing utilities"""
    
    def test_sample_responses_valid_json(self):
        """Test that sample responses file contains valid JSON"""
        json_path = os.path.join(
            os.path.dirname(__file__),
            '..', 'resources', 'footystats', 'sample_responses.json'
        )
        
        assert os.path.exists(json_path), "Sample responses file should exist"
        
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        assert isinstance(data, dict), "Sample responses should be a dictionary"
        
        # Check that key endpoints are present
        expected_endpoints = [
            'league_table', 'match_details', 'league_matches', 
            'team', 'league_teams', 'country_list', 'league_list'
        ]
        
        for endpoint in expected_endpoints:
            assert endpoint in data, f"Endpoint '{endpoint}' missing from sample responses"
            assert 'response' in data[endpoint], f"Response data missing for '{endpoint}'"
    
    def test_response_structure_consistency(self):
        """Test that all sample responses have consistent structure"""
        json_path = os.path.join(
            os.path.dirname(__file__),
            '..', 'resources', 'footystats', 'sample_responses.json'
        )
        
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        for endpoint_name, endpoint_data in data.items():
            # Each endpoint should have these keys
            assert 'endpoint' in endpoint_data, f"'{endpoint_name}' missing endpoint URL"
            assert 'parameters' in endpoint_data, f"'{endpoint_name}' missing parameters"
            assert 'response' in endpoint_data, f"'{endpoint_name}' missing response"
            
            # Parameters should include API key
            assert 'key' in endpoint_data['parameters'], f"'{endpoint_name}' missing API key parameter"


class MockAPIResponseTest:
    """Test mock API response creation"""
    
    def test_create_json_response(self):
        """Test JSON response creation"""
        base = FootyStatsTestBase()
        test_data = {'test': 'data', 'number': 123}
        test_url = 'https://api.test.com/endpoint'
        
        response = base.create_json_response(test_url, test_data)
        
        assert response.url == test_url
        assert response.status == 200
        
        parsed_data = json.loads(response.text)
        assert parsed_data == test_data
    
    def test_create_json_response_with_error_status(self):
        """Test JSON response creation with error status"""
        base = FootyStatsTestBase()
        test_data = {'error': 'Not found'}
        test_url = 'https://api.test.com/endpoint'
        
        response = base.create_json_response(test_url, test_data, status=404)
        
        assert response.status == 404
        parsed_data = json.loads(response.text)
        assert parsed_data == test_data


# Import test modules for specific spiders
# These will be created in separate files
__all__ = [
    'FootyStatsTestBase', 
    'TestFootyStatsAPIResponse', 
    'MockAPIResponseTest'
]