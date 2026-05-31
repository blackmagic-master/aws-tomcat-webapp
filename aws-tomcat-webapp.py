import json
import source.run as run
import sys
import requests


def main():
    config_file = open('config.json', 'r')
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


try:
    res = requests.get("http://www.google.com")
    if res.status_code == 200:
        main()
except:
    print("No internet connection, cannot proceed.")