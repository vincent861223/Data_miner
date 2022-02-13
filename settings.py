import json
import os


def _get_absolute_path(relative_path):
    script_path = os.path.dirname(__file__)  # <-- absolute dir the script is in
    abs_path = os.path.join(script_path, relative_path)

    return abs_path

class Settings:
    # keep tracks of all configurations - we may have different configs for different repositories
    _all_configs = None

    _file = "./config.json"

    def __init__(self):
        self.config = Settings._all_configs

        self.load()
        
    def load(self):
        # Loads the file only once
        if Settings._all_configs is not None:
            return
        
        with open(self._file) as config_file:
            self.config = json.loads(config_file.read())
            Settings._all_configs = self.config

    def get_repository_name(self):
        return self.config["repo_name"]

    def get_repository_file_path(self):
        return _get_absolute_path(self.config["repository_file"])

    def get_output_folder_path(self):
        return _get_absolute_path(self.config["output_folder"])

    def get_log_file_path(self):
        return _get_absolute_path(self.config["log_file"])

    def get_smell_detector_path(self):
        return _get_absolute_path(self.config["smell_detector"])
