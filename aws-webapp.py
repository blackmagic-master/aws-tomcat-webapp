import json
import source.setup as setup

config_file = open('config.json', 'r')
config = json.load(config_file)
config_file.close()

setup.init(config)