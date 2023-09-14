from examon.lib.examon_engine_factory import ExamonEngineFactory
from examon.lib.reporting.results_manager import ResultsManager
from examon.view.formatter_options import FormatterOptions
from examon_core.examon_item_registry import ItemRegistryFilter
from examon.lib.config import SettingsManagerFactory, ConfigDirFactory
from examon.lib.pip_installer import PipInstaller
from examon.lib.storage.read.examon_reader_factory import ExamonReaderFactory
from .validate_config import ValidateConfig


class RunnerCli:
    @staticmethod
    def process_command(cli_args):
        config_dir = ConfigDirFactory.build()
        ValidateConfig.config_dir_exists(config_dir)

        settings_manager = SettingsManagerFactory.build(
            config_dir.config_full_file_path()
        )
        PipInstaller.import_packages(settings_manager.active_packages)
        max_questions = cli_args.max_questions

        item_registry_filter = ItemRegistryFilter(
            tags_any=RunnerCli.get_tags(cli_args),
            tags_all=RunnerCli.tags_as_array(cli_args.tags_mandatory),
            max_questions=int(max_questions) if max_questions is not None else None,
            difficulty_category=cli_args.difficulty,
        )

        examon_engine = ExamonEngineFactory.build(
            ExamonReaderFactory.load(
                config_dir,
                content_mode=settings_manager.content_mode,
                file_mode=settings_manager.file_mode,
            ).load(item_registry_filter), FormatterOptions()[cli_args.formatter]
        )

        if cli_args.dry_run:
            return
        examon_engine.run()

        if cli_args.file:
            results_manager = ResultsManager(
                examon_engine.responses,
                settings_manager.active_packages,
                item_registry_filter,
                file_name=cli_args.file,
            )
            results_manager.save_to_file()
            print(f"Results saved to {results_manager.full_path}")
        print(examon_engine.summary())

    @staticmethod
    def get_tags(cli_args):
        tags = []
        if cli_args.tags is not None:
            tag_str = cli_args.tags

            tags = RunnerCli.tags_as_array(tag_str)
        if cli_args.tag is not None:
            tags.append(cli_args.tag)

        return tags if len(tags) > 0 else None

    @staticmethod
    def tags_as_array(tag_str):
        if tag_str is None or tag_str == "":
            return None
        return [tag.strip() for tag in tag_str.split(",")]
