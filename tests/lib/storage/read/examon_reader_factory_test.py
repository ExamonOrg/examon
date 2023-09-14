from examon.lib.storage.read.examon_reader_factory import ExamonReaderFactory
from examon.lib.storage.read.content.sqlite3.sqlite3_reader import Sqlite3Reader
from examon.lib.storage.read.files.local_file_system_reader import LocalFileSystemReader
from examon.lib.storage.read.content.mongodb.mongodb_reader import MongoDbReader

from helpers import Helpers


class TestExamonReaderFactory:
    def test_build_no_args(self):
        config_dir = Helpers.setup_directories()
        result = ExamonReaderFactory.load(config_dir=config_dir)
        assert result.content_reader.__class__ == Sqlite3Reader
        assert result.file_reader is None

    def test_build_with_args(self):
        config_dir = Helpers.setup_directories()
        result = ExamonReaderFactory.load(
            content_mode='mongodb',
            config_dir=config_dir,
            file_mode='local')
        assert result.content_reader.__class__ == MongoDbReader
        assert result.file_reader.__class__ == LocalFileSystemReader
