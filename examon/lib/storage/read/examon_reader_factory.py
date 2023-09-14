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
    def load(
            config_dir=ExamonConfigDir,
            content_mode: str = "sqlite3",
            file_mode: str = "memory"
    ) -> Reader:
        content_modes = {
            "sqlite3": Sqlite3Reader(
                db_file=config_dir.sqlite3_full_path()
            ),
            "memory": InMemoryReader(ExamonItemRegistry.registry()),
            "mongodb": MongoDbReader(driver=(
                pymongo.MongoClient("mongodb://localhost:27017/")
            )),
        }

        return Reader(
            content_modes[content_mode],
            LocalFileSystemReader() if file_mode == "local" else None
        )
