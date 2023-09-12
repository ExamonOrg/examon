import os
from examon.lib.config.config_dir_factory import ConfigDirFactory
from examon.lib.config.config_dir_factory import JsonConfigStore
from examon.lib.config.config_dir import ExamonConfigDir


class JsonConfigStoreFactory:

    def test_persist_default_config(self):
        cwd = os.getcwd()
        config_dir = ExamonConfigDir(
            settings_file="config.json",
            sqlite3_db_file="examon.db",
            files_dir="files",
            results_dir="results",
            examon_dir=f"{cwd}/tests/tmp2/.examon",
        )
        ConfigDirFactory.clean(config_dir)
        ConfigDirFactory.init_everything(config_dir)
        JsonConfigStore.persist_default_config(config_dir.config_full_file_path())
