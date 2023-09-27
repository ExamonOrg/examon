import subprocess
import sys
import importlib.util
import logging

from examon.lib.config import SettingsManagerFactory


class PipInstaller:
    @staticmethod
    def install(examon_config_dir) -> SettingsManagerFactory:
        manager = SettingsManagerFactory.build(
            examon_config_dir.config_full_file_path()
        )
        logging.info(f"installing {len(manager.packages)} repos")
        for package in manager.packages:
            with open(f"/{examon_config_dir.examon_dir}/pip_install.log", "w") as outfile:
                cmd = [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    package["name"],
                    "--upgrade",
                ]
                logging.debug(cmd)
                subprocess.run(cmd, stdout=outfile)
        PipInstaller.import_packages(manager.active_packages)
        return manager

    @staticmethod
    def is_package_installed(package) -> bool:
        return importlib.util.find_spec(package) is None

    @staticmethod
    def import_packages(packages) -> None:
        logging.info(f"Importing Packages ({len(packages)})")
        for repo in packages:
            __import__(repo, fromlist=["*"])
