import yaml
import os.path

class ConfigReader:
    def __init__(self):
        config_path=os.path.join(os.path.dirname(__file__),"..","Config","config.yaml")   #../Config/config.yaml not to use because it will not work in all OS
        with open(config_path,'r') as file:
            self._data=yaml.safe_load(file)

    def get(self):
        return self._data
