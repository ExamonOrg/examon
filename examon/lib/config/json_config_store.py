import os.path
import os
import json
import logging
from .settings_manager import SettingsManager

DEFAULT_FILE_MODE = "local"
DEFAULT_CONTENT_MODE = "sqlite3"
DEFAULT_MODULES = ["examon_beginners_package", "examon_pcep_package"]


class JsonConfigStore:

    @staticmethod
    def persist(package_manager, full_file_path: str) -> None:
        with open(full_file_path, "w") as json_config:
            json_config.write(json.dumps(package_manager.as_dict(), indent=4))
        logging.info(f"config saved to {full_file_path}")

    @staticmethod
    def persist_default_config(full_file_path: str) -> None:
        settings_manager = SettingsManager(
            content_mode=DEFAULT_CONTENT_MODE,
            file_mode=DEFAULT_FILE_MODE,
            packages=[{"name": p} for p in DEFAULT_MODULES],
            active_packages=DEFAULT_MODULES
        )

        if not os.path.isfile(full_file_path):
            JsonConfigStore.persist(settings_manager, full_file_path)
