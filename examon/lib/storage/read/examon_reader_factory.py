from .reader import Reader
from .content.sqlite3.sqlite3_reader import Sqlite3Reader
from .content.mongodb.mongodb_reader import MongoDbReader
from .content.in_memory.in_memory import InMemoryReader
from .files.local_file_system_reader import LocalFileSystemReader

from ...config import ExamonConfigDir
from examon_core.examon_item_registry import ExamonItemRegistry, ItemRegistryFilter
import pymongo


class ExamonReaderFactory:

    @staticmethod
    def load(examon_config_dir: ExamonConfigDir,
             content_mode: str = 'sqlite3',
             file_mode: str = 'memory',
             examon_filter: ItemRegistryFilter = ItemRegistryFilter()) -> list:
        content_reader_driver = None
        file_reader_driver = None

        if content_mode == 'sqlite3' and file_mode == 'local':
            file_reader_driver = LocalFileSystemReader()
            content_reader_driver = Sqlite3Reader(
                db_file=examon_config_dir.sqlite3_full_path()
            )
        elif content_mode == 'sqlite3':
            content_reader_driver = Sqlite3Reader(
                db_file=examon_config_dir.sqlite3_full_path()
            )
        elif content_mode == 'memory':
            content_reader_driver = InMemoryReader(ExamonItemRegistry.registry())
        elif content_mode == 'mongodb':
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            content_reader_driver = MongoDbReader(driver=client)

        reader = Reader(content_reader_driver, file_reader_driver)
        return reader.load(examon_filter)
