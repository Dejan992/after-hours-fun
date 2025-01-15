import time
from typing import Dict, List, Any
from collections import defaultdict
from .config_parser import ConfigParser
from .health_checker import HealthChecker

class Monitor:
    def __init__(self, config_path: str):
        self.config_parser = ConfigParser()
        self.health_checker = HealthChecker()
        self.endpoints = self.config_parser.parse_config(config_path)
        
        self.stats = defaultdict(lambda: {'up': 0, 'total': 0})
        
    def run_health_checks(self):
        """Run a single cycle of health checks for all endpoints."""
        for endpoint in self.endpoints:
            domain = self.config_parser.extract_domain(endpoint['url'])
            is_up, _ = self.health_checker.check_endpoint(endpoint)
            
            self.stats[domain]['total'] += 1
            if is_up:
                self.stats[domain]['up'] += 1

    def get_availability_percentage(self, domain: str) -> int:
        """Calculate availability percentage for a domain."""
        if domain not in self.stats or self.stats[domain]['total'] == 0:
            return 0
        return round((self.stats[domain]['up'] / self.stats[domain]['total']) * 100)

    def print_availability(self):
        """Print availability percentage for each domain."""
        for domain in self.stats:
            percentage = self.get_availability_percentage(domain)
            print(f"{domain} has {percentage}% availability percentage")

    def run(self):
        """Main monitoring loop."""
        try:
            while True:
                self.run_health_checks()
                self.print_availability()
                time.sleep(15)
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")