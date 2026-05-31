import json
import source.setup as setup
import sys

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
        setup.init(config, "P")
    elif OPTION == "--temporary" or OPTION == "-t":
        setup.init(config, "T")
    else:
        print("Invalid option: " + OPTION)
elif COMMAND == "down":
    if OPTION is None:
        setup.destroy()
    else:
        print("No option needed to destroy: " + OPTION)
elif COMMAND is None:
    print("No command specified.")
else:
    print("Invalid command: " + COMMAND)
