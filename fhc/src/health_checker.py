import requests
import time
from typing import Dict, Any, Tuple
from requests.exceptions import RequestException

class HealthChecker:
    def __init__(self):
        self.session = requests.Session()

    def check_endpoint(self, endpoint: Dict[str, Any]) -> Tuple[bool, float]:
        """
        Check the health of an endpoint.
        Returns: (is_up, response_time_ms)
        """
        start_time = time.time()
        
        try:
            response = self.session.request(
                method=endpoint['method'],
                url=endpoint['url'],
                headers=endpoint['headers'],
                json=endpoint.get('body'),
                timeout=5
            )
            
            response_time_ms = (time.time() - start_time) * 1000
            
            is_up = (200 <= response.status_code < 300) and (response_time_ms < 500)
            
            return is_up, response_time_ms
            
        except RequestException:
            return False, 0