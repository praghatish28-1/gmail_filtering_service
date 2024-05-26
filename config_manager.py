import os
import json
import logging

logger = logging.getLogger(__name__)

class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file

    def load_config(self):
        try:
            config_path = os.path.join(os.path.dirname(__file__), self.config_file)
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading config file: {e}")
            return {}

    def get_config(self, key):
        config = self.load_config()
        return config.get(key, None)
