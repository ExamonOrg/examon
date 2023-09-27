from examon_core.examon_filter_options import ExamonFilterOptions
from examon_core.models.question import BaseQuestion

from ....read_write.question_adapter_factory import build
from ...protocols import ContentReader


class MongoDbReader(ContentReader):
    def __init__(self, driver=None) -> None:
        self.driver = driver

    def load(self, examon_filter_options: ExamonFilterOptions = None) -> list[BaseQuestion]:
        query = {}

        if examon_filter_options is not None and examon_filter_options.tags_any is not None:
            query["tags"] = {"$in": examon_filter_options.tags_any}

        if examon_filter_options is not None and examon_filter_options.difficulty_category is not None:
            query["metrics.categorised_difficulty"] = "Easy"

        if examon_filter_options is not None and examon_filter_options.tags_all is not None:
            query["tags"] = {"$all": examon_filter_options.tags_any}

        records = self.driver["examon"]["questions"].find(query)
        return [build(result) for result in records]
