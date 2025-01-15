import pytest
from src.config_parser import ConfigParser

@pytest.fixture
def sample_yaml(tmp_path):
    config = tmp_path / "test_config.yaml"
    config.write_text("""
- name: test endpoint
  url: https://test.com
  method: GET
  headers:
    user-agent: test-monitor
- name: minimal endpoint
  url: https://example.com
    """)
    return str(config)

def test_parse_config_valid(sample_yaml):
    parser = ConfigParser()
    config = parser.parse_config(sample_yaml)
    
    assert len(config) == 2
    assert config[0]['name'] == 'test endpoint'
    assert config[0]['url'] == 'https://test.com'
    assert config[0]['method'] == 'GET'
    assert config[0]['headers'] == {'user-agent': 'test-monitor'}
    
    assert config[1]['method'] == 'GET'
    assert config[1]['headers'] == {}
    assert config[1]['body'] is None

def test_parse_config_invalid_file():
    parser = ConfigParser()
    with pytest.raises(FileNotFoundError):
        parser.parse_config("nonexistent.yaml")

def test_parse_config_missing_required_fields(tmp_path):
    config = tmp_path / "invalid.yaml"
    config.write_text("""
- url: https://test.com
    """)
    
    parser = ConfigParser()
    with pytest.raises(ValueError, match="Each endpoint must have 'name' and 'url' fields"):
        parser.parse_config(str(config))

def test_extract_domain():
    parser = ConfigParser()
    assert parser.extract_domain("https://test.com/path") == "test.com"
    assert parser.extract_domain("https://sub.test.com/path") == "sub.test.com"

def test_invalid_url(tmp_path):
    """Test handling of invalid URLs."""
    config = tmp_path / "invalid_url.yaml"
    config.write_text("""
- name: test endpoint
  url: not-a-valid-url
    """)
    
    parser = ConfigParser()
    with pytest.raises(ValueError, match="Invalid URL format"):
        parser.parse_config(str(config))

def test_empty_required_fields(tmp_path):
    """Test handling of empty required fields."""
    config = tmp_path / "empty_fields.yaml"
    config.write_text("""
- name: ""
  url: https://test.com
    """)
    
    parser = ConfigParser()
    with pytest.raises(ValueError, match="Empty name field"):
        parser.parse_config(str(config))
