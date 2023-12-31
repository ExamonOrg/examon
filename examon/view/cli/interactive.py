from examon_core.examon_in_memory_db import ExamonInMemoryDatabase
from examon_core.examon_filter_options import ExamonFilterOptions
from simple_term_menu import TerminalMenu

from examon.lib.pip_installer import PipInstaller
from examon.lib.config.config_dir_factory import ConfigDirFactory
from examon.lib.examon_engine_factory import ExamonEngineFactory
from examon.lib.storage.read.examon_reader_factory import ExamonReaderFactory
from examon.lib.reporting.results_manager import ResultsManager
from examon.view.formatter_options import FormatterOptions

from ...lib.storage.write.examon_writer_factory import ExamonWriterFactory
from ...lib.utils.logging import decorator_timer

ASCII_ART = """
              ,--.
              |
              |-   . , ,-: ;-.-. ,-. ;-.
              |     X  | | | | | | | | |
              `--' ' ` `-` ' ' ' `-' ' '
        """


class InteractiveCLI:
    DEFAULT_PACKAGES = ["examon_beginners_package", "examon_pcep_package"]

    @staticmethod
    @decorator_timer

    def process_command():
        print(ASCII_ART)
        examon_config_dir = ConfigDirFactory.init_everything(ConfigDirFactory.build())

        manager = PipInstaller.install(examon_config_dir)
        writer = ExamonWriterFactory.build(
            manager.content_mode,
            manager.file_mode,
            examon_config_dir,
            ExamonInMemoryDatabase.load(),
        )
        writer.run()

        examon_engine, results_manager = InteractiveCLI.run_quiz(
            examon_config_dir,
            manager,
            ExamonFilterOptions(
                tags_any=(InteractiveCLI.get_tags(tags=["PCEP", "beginner"]))
            ),
        )
        full_results_file_path = f"{examon_config_dir.results_full_path()}/{ResultsManager.default_filename()}"
        results_manager.save_to_file(full_results_file_path)
        print(f"Results saved to {full_results_file_path}")

        print(examon_engine.summary())

    @staticmethod
    def get_tags(tags=ExamonInMemoryDatabase.unique_tags()):
        available_tags = list(filter(None, tags))
        selected_tags = None
        if len(available_tags) > 0:
            terminal_menu = TerminalMenu(
                available_tags,
                title="Please select the question tags",
                multi_select=True,
                show_multi_select_hint=True,
            )
            terminal_menu.show()
            selected_tags = [*terminal_menu.chosen_menu_entries]
        return selected_tags

    @staticmethod
    def run_quiz(examon_config_dir, manager, registry_filter):
        examon_engine = ExamonEngineFactory.build(
            ExamonReaderFactory.load(
                config_dir=examon_config_dir,
                content_mode=manager.content_mode,
                file_mode=manager.file_mode,
            ).load(registry_filter), FormatterOptions()["terminal256"]
        )
        examon_engine.run()
        results_manager = ResultsManager(
            examon_engine.responses, manager.active_packages, registry_filter
        )
        return examon_engine, results_manager
