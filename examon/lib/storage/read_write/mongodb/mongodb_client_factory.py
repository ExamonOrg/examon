import pymongo
import os
from pymongo.server_api import ServerApi
from ....config import ExamonConfigDir, SettingsManagerFactory


# https://pymongo.readthedocs.io/en/stable/examples/authentication.html
class MongoDBClientConnectionFactory:
    @staticmethod
    def build(examon_config_dir: ExamonConfigDir) -> pymongo.MongoClient:
        settings_manager = SettingsManagerFactory.build(examon_config_dir.config_full_file_path())
        mclient = pymongo.MongoClient(settings_manager.mongodb_uri(), server_api=ServerApi('1'))
        return mclient

    @staticmethod
    def build_from_env() -> pymongo.MongoClient:
        try:
            domain = os.environ['MONGODB_DOMAIN']
            user = os.environ['MONGODB_USER']
            protocol = os.environ['MONGODB_PROTOCOL']
            password = os.environ['MONGODB_PASSWORD']
        except KeyError as e:
            raise Exception(f"Missing environment variables for MongoDB: {e}")
        uri = f"{protocol}://{user}:{password}@{domain}/?retryWrites=true&w=majority"
        client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
        return client
