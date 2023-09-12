from pathlib import Path
import os
import shutil
from sqlalchemy import create_engine
import pymongo

from .content.sqlite3.sqlite3_writer import Sqlite3Writer
from .content.mongodb.mongodb_writer import MongoDbWriter
from .files.local_file_system_writer import LocalFileSystemDriver
from .files.null_file_writer import NullFileDriver
from .writer import Writer
from ..read_write.naming_strategies import SimpleFilenameStrategy
from ..read_write.sql_db import QuestionQuery


class ExamonWriterFactory:
    @staticmethod
    def build(content_mode, file_mode, examon_config_dir, models) -> Writer:
        if file_mode != "null":
            if content_mode == "sqlite3":
                return ExamonWriterFactory.build_sqlite3_local_file_system(
                    examon_config_dir.config_full_file_path(),
                    examon_config_dir.sqlite3_full_path(),
                    models,
                )
            elif content_mode == "mongodb":
                return ExamonWriterFactory.build_mongodb_local_file_system(
                    examon_config_dir.config_full_file_path(), models
                )
        if file_mode == "null":
            if content_mode == "sqlite3":
                return ExamonWriterFactory.build_sqlite3(
                    examon_config_dir.sqlite3_full_path(), models
                )
            elif content_mode == "mongodb":
                return ExamonWriterFactory.build_mongodb(models)

    @staticmethod
    def build_mongodb(models) -> Writer:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        filename_strategy = SimpleFilenameStrategy("null:///")

        return Writer(
            MongoDbWriter(
                client=client,
                filename_strategy=filename_strategy,
                models=models,
                collection_name="questions",
                database_name="examon",
            ),
            NullFileDriver(),
        )

    @staticmethod
    def build_mongodb_local_file_system(files_dir, models) -> Writer:
        ExamonWriterFactory.mkdirs(files_dir)
        filename_strategy = SimpleFilenameStrategy(files_dir)
        client = pymongo.MongoClient("mongodb://localhost:27017/")

        return Writer(
            MongoDbWriter(
                client=client,
                filename_strategy=filename_strategy,
                models=models,
                collection_name="questions",
                database_name="examon",
            ),
            LocalFileSystemDriver(models=models, filename_strategy=filename_strategy),
        )

    @staticmethod
    def build_sqlite3_local_file_system(files_dir, db_name, models) -> Writer:
        ExamonWriterFactory.mkdirs(files_dir)

        # TODO move to config factory init
        if not os.path.isfile(db_name):
            root_dir = os.path.abspath(os.curdir)
            shutil.copyfile(f"{root_dir}/resources/examon.db", db_name)

        engine = create_engine(f"sqlite+pysqlite:///{db_name}", echo=True)

        # TODO move this to sqlite3 driver
        ids = QuestionQuery(engine).question_unique_ids()
        models = [model for model in models if model.unique_id not in ids]

        filename_strategy = SimpleFilenameStrategy(files_dir)
        return Writer(
            Sqlite3Writer(
                engine=engine, models=models, filename_strategy=filename_strategy
            ),
            LocalFileSystemDriver(models=models, filename_strategy=filename_strategy),
        )

    # TODO move to config factory init
    @staticmethod
    def mkdirs(files_dir):
        if not os.path.isfile(files_dir):
            Path(files_dir).mkdir(parents=True, exist_ok=True)
