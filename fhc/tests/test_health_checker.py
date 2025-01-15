import pytest
from src.health_checker import HealthChecker
from unittest.mock import patch, MagicMock
import requests

@pytest.fixture
def health_checker():
    return HealthChecker()

@pytest.fixture
def sample_endpoint():
    return {
        'name': 'test endpoint',
        'url': 'https://test.com',
        'method': 'GET',
        'headers': {'user-agent': 'test'},
        'body': None
    }

def test_successful_health_check(health_checker, sample_endpoint):
    with patch('requests.Session.request') as mock_request:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_request.return_value = mock_response
        
        with patch('time.time') as mock_time:
            mock_time.side_effect = [0, 0.1]
            is_up, response_time = health_checker.check_endpoint(sample_endpoint)
        
        assert is_up is True
        assert response_time < 500

def test_slow_response(health_checker, sample_endpoint):
    with patch('requests.Session.request') as mock_request:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_request.return_value = mock_response
        
        with patch('time.time') as mock_time:
            mock_time.side_effect = [0, 0.6]
            is_up, response_time = health_checker.check_endpoint(sample_endpoint)
        
        assert is_up is False
        assert response_time >= 500

def test_error_response(health_checker, sample_endpoint):
    with patch('requests.Session.request') as mock_request:
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_request.return_value = mock_response
        
        with patch('time.time') as mock_time:
            mock_time.side_effect = [0, 0.1]
            is_up, _ = health_checker.check_endpoint(sample_endpoint)
        
        assert is_up is False

def test_connection_error(health_checker, sample_endpoint):
    with patch('requests.Session.request') as mock_request:
        mock_request.side_effect = requests.exceptions.RequestException
        
        is_up, _ = health_checker.check_endpoint(sample_endpoint)
        assert is_up is False

def test_timeout_response(health_checker, sample_endpoint):
    """Test behavior when request times out."""
    with patch('requests.Session.request') as mock_request:
        mock_request.side_effect = requests.exceptions.Timeout
        
        is_up, response_time = health_checker.check_endpoint(sample_endpoint)
        
        assert is_up is False
        assert response_time == 0

def test_connection_error(health_checker, sample_endpoint):
    """Test behavior when connection fails."""
    with patch('requests.Session.request') as mock_request:
        mock_request.side_effect = requests.exceptions.ConnectionError
        
        is_up, response_time = health_checker.check_endpoint(sample_endpoint)
        
        assert is_up is False
        assert response_time == 0

def test_invalid_status_code(health_checker, sample_endpoint):
    """Test various non-2xx status codes."""
    status_codes = [301, 404, 500, 503]
    
    for status_code in status_codes:
        with patch('requests.Session.request') as mock_request:
            mock_response = MagicMock()
            mock_response.status_code = status_code
            mock_request.return_value = mock_response
            
            with patch('time.time') as mock_time:
                mock_time.side_effect = [0, 0.1]
                is_up, response_time = health_checker.check_endpoint(sample_endpoint)
            
            assert is_up is False
            assert response_time < 500
