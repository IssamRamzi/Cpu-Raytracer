import json
import os

class ConfigLoader:
    def __init__(self, path):
        assert path.endswith(".json"), "Supports only json files"
        assert os.path.exists(path), f"Config file not found: {path}"
        
        self.path = path
        self.config = {}
        self._load()

    def _load(self):
        with open(self.path, "r") as f:
            self.config = json.load(f)

    def get_camera(self):
        return self.config.get("camera", None)

    def get_materials(self):
        return self.config.get("materials", [])

    def get_primitives(self):
        return self.config.get("primitives", [])
