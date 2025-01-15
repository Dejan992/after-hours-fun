# HTTP Endpoint Health Monitor

A robust Python application that monitors HTTP endpoints and tracks their availability percentage. Built as part of the Fetch Site Reliability Engineering take-home assessment.

## Overview

This application monitors a set of HTTP endpoints specified in a YAML configuration file. It performs health checks every 15 seconds and maintains availability statistics for each domain. An endpoint is considered "UP" if it returns a 2xx status code and responds within 500ms.

### Features
- YAML-based configuration
- Concurrent health checks
- Domain-based availability tracking
- Real-time console reporting
- Graceful error handling
- Comprehensive test coverage

## Requirements

- Python 3.8+
- pip (Python package installer)

## Installation

1. Clone the repository:
```
bash
git clone <repository-url>
cd after-hours-fun
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Create a YAML configuration file (or use the provided example in `config/endpoints.yaml`):
```yaml
- name: fetch index page
  url: https://fetch.com/
  method: GET
  headers:
    user-agent: fetch-synthetic-monitor

- name: fetch careers page
  url: https://fetch.com/careers
  headers:
    user-agent: fetch-synthetic-monitor
```

2. Run the monitor:
```bash
python main.py config/endpoints.yaml
```

3. The program will output availability percentages every 15 seconds:
```
fetch.com has 67% availability percentage
www.fetchrewards.com has 50% availability percentage
```

## Configuration File Format

The YAML configuration file should contain a list of endpoints with the following schema:

| Field | Type | Required | Description | Default |
|-------|------|----------|-------------|---------|
| name | string | Yes | Description of the endpoint | - |
| url | string | Yes | The HTTP(S) endpoint URL | - |
| method | string | No | HTTP method (GET, POST, etc.) | GET |
| headers | object | No | HTTP headers to include | {} |
| body | string | No | JSON-encoded request body | null |

## Architecture

The application is structured into three main components:

1. **Config Parser** (`src/config_parser.py`)
   - Validates and parses YAML configuration
   - Extracts domain information
   - Sets default values for optional fields

2. **Health Checker** (`src/health_checker.py`)
   - Performs HTTP requests
   - Measures response times
   - Determines endpoint status (UP/DOWN)

3. **Monitor** (`src/monitor.py`)
   - Coordinates health checks
   - Maintains availability statistics
   - Handles reporting and main loop

## Testing

The project includes comprehensive test coverage. To run tests:

```bash
pytest tests/
```

Key test scenarios include:
- Configuration parsing and validation
- HTTP request handling and timing
- Availability percentage calculations
- Error cases and edge conditions

## Design Decisions

1. **In-Memory Storage**
   - Uses Python's `defaultdict` for efficient statistics tracking
   - No persistent storage (as per requirements)
   - Thread-safe for the current single-threaded implementation

2. **Error Handling**
   - Graceful handling of network errors
   - Clear error messages for configuration issues
   - Continues monitoring despite individual endpoint failures

3. **Code Structure**
   - Modular design for easy testing and maintenance
   - Clear separation of concerns
   - Type hints for better code clarity

## Future Improvements

Potential enhancements that could be added:

1. Concurrent health checks for better performance
2. More detailed reporting (response times, error types)
3. Configurable thresholds (timeout, check interval)
4. Web interface for monitoring
5. Metrics export (Prometheus, etc.)

## Contributing

While this is an assessment project, contributions would typically be welcome. Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request
