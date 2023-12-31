from examon_core.examon_in_memory_db import ExamonInMemoryDatabase

from examon.lib.config import JsonConfigStore, ConfigDirFactory, SettingsManagerFactory
from examon.lib.storage.write.examon_writer_factory import ExamonWriterFactory
from examon.lib.pip_installer import PipInstaller
from .validate_config import ValidateConfig


class PackageManagerCli:
    @staticmethod
    def process_command(cli_args):
        config = ConfigDirFactory.build()
        path = config.config_full_file_path()
        sub_command = cli_args.sub_command

        if sub_command == "init":
            ConfigDirFactory.init_everything()
            return

        ValidateConfig.config_dir_exists(config)

        package_manager = SettingsManagerFactory.build(path)
        if sub_command in ["add", "remove", "add_active", "remove_active"]:
            if sub_command == "add":
                package_manager.add(cli_args.name, cli_args.pip_url)
            elif sub_command == "remove":
                package_manager.remove(cli_args.name)
            elif sub_command == "add_active":
                package_manager.add_active(cli_args.name)
            elif sub_command == "remove_active":
                package_manager.remove_active(cli_args.name)
            JsonConfigStore.persist(package_manager, path)
            return

        if sub_command == "list":
            PackageManagerCli.print_packages(package_manager)
        elif sub_command == "install":
            PipInstaller.install(config)
            PipInstaller.import_packages(
                [package["name"] for package in package_manager.packages]
            )
            ExamonWriterFactory.build(
                content_mode=package_manager.content_mode,
                file_mode=package_manager.file_mode,
                examon_config_dir=config,
                models=ExamonInMemoryDatabase.load(),
            ).run()

        else:
            print("Invalid subcommand (add, remove, install, list, init)")

    @staticmethod
    def print_packages(package_manager):
        print("")
        print("All:")
        for repo in package_manager.packages:
            print(repo["name"])
        print("")
        print("Active:")
        for repo in package_manager.active_packages:
            print(repo)
        print("")
