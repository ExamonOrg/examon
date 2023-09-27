from pathlib import Path
import os
from sqlalchemy import create_engine
import pymongo

from .content.sqlite3.sqlite3_writer import Sqlite3Writer
from .content.mongodb.mongodb_writer import MongoDbWriter
from .files.local_file_system_writer import LocalFileSystemDriver
from .files.null_file_writer import NullFileDriver
from .writer import Writer
from ..read_write.naming_strategies import SimpleFilenameStrategy
from ..read_write.sql_db import QuestionQuery
from ..read_write.mongodb.mongodb_client_factory import MongoDBClientConnectionFactory


class ExamonWriterFactory:
    @staticmethod
    def build(content_mode, file_mode, examon_config_dir, models) -> Writer:
        engine = create_engine(
            f"sqlite+pysqlite:///{examon_config_dir.sqlite3_full_path()}",
            echo=True
        )

        file_driver_mapping = {
            "null": NullFileDriver(),
            "local": LocalFileSystemDriver(
                models=models, filename_strategy=SimpleFilenameStrategy(
                    examon_config_dir.code_files_full_path()
                )
            ),
        }

        if content_mode == "sqlite3":
            ids = QuestionQuery(engine).question_unique_ids()
            models = [model for model in models if model.unique_id not in ids]

        content_driver_mapping = {
            "sqlite3": Sqlite3Writer(
                engine=engine,
                models=models, filename_strategy=SimpleFilenameStrategy(
                    examon_config_dir.code_files_full_path()
                )
            ),
            "mongodb": ExamonWriterFactory._get_mongodb_writer(examon_config_dir, models)
        }

        ExamonWriterFactory.mkdirs(examon_config_dir.code_files_full_path())

        return Writer(
            content_driver_mapping[content_mode],
            file_driver_mapping[file_mode],
        )

    @staticmethod
    def _get_mongodb_writer(examon_config_dir, models):
        return MongoDbWriter(
            client=(MongoDBClientConnectionFactory.build(examon_config_dir)),
            filename_strategy=(SimpleFilenameStrategy("null:///")),
            models=models,
            collection_name="questions",
            database_name="examon",
        )

    # TODO move to config factory init
    @staticmethod
    def mkdirs(files_dir):
        if not os.path.isfile(files_dir):
            Path(files_dir).mkdir(parents=True, exist_ok=True)
