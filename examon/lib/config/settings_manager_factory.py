import json
from .settings_manager import SettingsManager


class SettingsManagerFactory:
    @staticmethod
    def build(full_file_path: str) -> SettingsManager:
        with open(full_file_path, "r") as f:
            data = json.load(f)

        return SettingsManager(
            packages=data["packages"]["all"],
            active_packages=data["packages"]["active"],
            content_mode=data["content_mode"],
            file_mode=data["file_mode"],
        )
