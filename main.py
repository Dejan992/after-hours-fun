import sys
import os
from src.monitor import Monitor

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_config_file>")
        sys.exit(1)

    config_path = sys.argv[1]
    if not os.path.exists(config_path):
        print(f"Error: Config file not found: {config_path}")
        sys.exit(1)

    try:
        monitor = Monitor(config_path)
        monitor.run()
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()