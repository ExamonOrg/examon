from examon.lib.storage.write.files.local_file_system_writer import LocalFileSystemDriver
from examon.lib.storage.write.examon_writer_factory import ExamonWriterFactory
from examon.lib.storage.write.content.mongodb.mongodb_writer import MongoDbWriter
from examon.lib.storage.write.files.null_file_writer import NullFileDriver
from examon.lib.storage.write.content.sqlite3.sqlite3_writer import Sqlite3Writer

from helpers import Helpers


class TestExamonWriterFactory:
    def test_build_mongodb_null(self):
        config_dir = Helpers.setup_directories()
        result = ExamonWriterFactory.build('mongodb', 'null', config_dir, [])
        assert result.content_writer.__class__ == MongoDbWriter
        assert result.file_writer.__class__ == NullFileDriver

    def test_build_mongodb_local(self):
        config_dir = Helpers.setup_directories()
        result = ExamonWriterFactory.build('mongodb', 'local', config_dir, [])
        assert result.content_writer.__class__ == MongoDbWriter
        assert result.file_writer.__class__ == LocalFileSystemDriver

    def test_build_sqlite3_local(self):
        config_dir = Helpers.setup_directories()
        result = ExamonWriterFactory.build('sqlite3', 'local', config_dir, [])
        assert result.content_writer.__class__ == Sqlite3Writer
        assert result.file_writer.__class__ == LocalFileSystemDriver
