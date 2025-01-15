import pytest
from src.monitor import Monitor
from unittest.mock import patch, MagicMock, call

@pytest.fixture
def sample_config(tmp_path):
    config = tmp_path / "test_config.yaml"
    config.write_text("""
- name: test endpoint
  url: https://test.com/api
    """)
    return str(config)

def test_monitor_initialization(sample_config):
    monitor = Monitor(sample_config)
    assert len(monitor.endpoints) == 1
    assert monitor.endpoints[0]['name'] == 'test endpoint'
    assert monitor.endpoints[0]['url'] == 'https://test.com/api'

def test_empty_config(tmp_path):
    """Test handling of empty config file."""
    config = tmp_path / "empty_config.yaml"
    config.write_text("[]")
    
    monitor = Monitor(str(config))
    monitor.run_health_checks()
    assert len(monitor.stats) == 0

def test_multiple_endpoints_same_domain(tmp_path):
    """Test multiple endpoints from the same domain."""
    config = tmp_path / "same_domain.yaml"
    config.write_text("""
- name: endpoint1
  url: https://example.com/api1
- name: endpoint2
  url: https://example.com/api2
    """)
    
    monitor = Monitor(str(config))
    
    mock_health_checker = MagicMock()
    mock_health_checker.check_endpoint.side_effect = [(True, 100), (False, 600)]
    monitor.health_checker = mock_health_checker
    
    monitor.run_health_checks()
    
    assert mock_health_checker.check_endpoint.call_count == 2
    
    assert monitor.stats['example.com']['up'] == 1
    assert monitor.stats['example.com']['total'] == 2
    assert monitor.get_availability_percentage('example.com') == 50

def test_consecutive_failures(tmp_path):
    """Test behavior with consecutive failures."""
    config = tmp_path / "test_config.yaml"
    config.write_text("""
- name: test endpoint
  url: https://test.com/api
    """)
    
    monitor = Monitor(str(config))
    
    mock_health_checker = MagicMock()
    mock_health_checker.check_endpoint.return_value = (False, 0)
    monitor.health_checker = mock_health_checker
    
    for _ in range(3):
        monitor.run_health_checks()
    
    assert monitor.stats['test.com']['up'] == 0
    assert monitor.stats['test.com']['total'] == 3
    assert monitor.get_availability_percentage('test.com') == 0
        