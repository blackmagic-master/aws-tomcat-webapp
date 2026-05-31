import json
import aws_tomcat_webapp.source.run as run
import sys
import requests
from pathlib import Path

version = "1.0.1"

def start():
    config_path = Path(__file__).parent / "config.json"
    config_file = open(config_path, 'r')
    config = json.load(config_file)
    config_file.close()

    COMMAND = None
    OPTION = None

    try:
        COMMAND = sys.argv[1]
    except IndexError:
        pass
    try:
        OPTION = sys.argv[2]
    except IndexError:
        pass

    if COMMAND == "up":
        if OPTION == "--permanent" or OPTION == "-p":
            run.init(config, "P")
        elif OPTION == "--temporary" or OPTION == "-t":
            run.init(config, "T")
        else:
            print("Invalid option: " + OPTION)
    elif COMMAND == "down":
        if OPTION is None:
            run.destroy(config)
        else:
            print("No option needed to destroy: " + OPTION)
    elif COMMAND is None:
        print("No command specified.")
    else:
        print("Invalid command: " + COMMAND)

def main():
    try:
        res = requests.get("https://www.google.com", timeout=10)
        if res.status_code == 200:
            start()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()