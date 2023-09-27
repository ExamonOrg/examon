from .reader import Reader
from .content.sqlite3.sqlite3_reader import Sqlite3Reader
from .content.mongodb.mongodb_reader import MongoDbReader
from .content.in_memory.in_memory import InMemoryReader
from .files.local_file_system_reader import LocalFileSystemReader

from ...config import ExamonConfigDir
from ..read_write.mongodb.mongodb_client_factory import MongoDBClientConnectionFactory
from examon_core.examon_in_memory_db import ExamonInMemoryDatabase


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
            "memory": InMemoryReader(ExamonInMemoryDatabase.load()),
            "mongodb": MongoDbReader(driver=(
                MongoDBClientConnectionFactory.build(config_dir)
            )),
        }

        return Reader(
            content_modes[content_mode],
            LocalFileSystemReader() if file_mode == "local" else None
        )
