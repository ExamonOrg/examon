import json
from .settings_manager import SettingsManager


class SettingsManagerFactory:
    @staticmethod
    def build(full_file_path: str) -> SettingsManager:
        with open(full_file_path, "r") as f:
            data = json.load(f)

        manager = SettingsManager(
            packages=data["packages"]["all"],
            active_packages=data["packages"]["active"],
            content_mode=data["content_mode"],
            file_mode=data["file_mode"]
        )

        if "mongodb_config" in data:
            manager.mongodb_config = data["mongodb_config"]

        return manager
