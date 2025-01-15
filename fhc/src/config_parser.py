import yaml
from typing import List, Dict, Any
from urllib.parse import urlparse

class ConfigParser:
    @staticmethod
    def parse_config(file_path: str) -> List[Dict[str, Any]]:
        """Parse the YAML configuration file and return list of endpoints."""
        try:
            with open(file_path, 'r') as file:
                config = yaml.safe_load(file)
                
            if not isinstance(config, list):
                raise ValueError("Configuration must be a list of endpoints")

            for endpoint in config:
                if 'name' not in endpoint or 'url' not in endpoint:
                    raise ValueError("Each endpoint must have 'name' and 'url' fields")

                if not endpoint['name'].strip():
                    raise ValueError("Empty name field")
                
                try:
                    parsed_url = urlparse(endpoint['url'])
                    if not all([parsed_url.scheme, parsed_url.netloc]):
                        raise ValueError("Invalid URL format")
                except Exception:
                    raise ValueError("Invalid URL format")
                
                endpoint.setdefault('method', 'GET')
                endpoint.setdefault('headers', {})
                endpoint.setdefault('body', None)
                
            return config
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {e}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

    @staticmethod
    def extract_domain(url: str) -> str:
        """Extract domain from URL."""
        return urlparse(url).netloc