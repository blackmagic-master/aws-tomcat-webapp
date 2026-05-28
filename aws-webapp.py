import json
import src
import src.setup

config_file = open('config.json', 'r')
config = json.load(config_file)
config_file.close()

src.setup.init(config)