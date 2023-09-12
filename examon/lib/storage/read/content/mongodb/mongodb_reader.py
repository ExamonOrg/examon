from examon_core.examon_item_registry import ItemRegistryFilter
from examon_core.models.question import BaseQuestion

from ....read_write.question_adapter_factory import build
from ...protocols import ContentReader


class MongoDbReader(ContentReader):
    def __init__(self, driver=None) -> None:
        self.driver = driver

    def load(self, examon_filter: ItemRegistryFilter = None) -> list[BaseQuestion]:
        query = {}

        if examon_filter is not None and examon_filter.tags_any is not None:
            query["tags"] = {"$in": examon_filter.tags_any}

        if examon_filter is not None and examon_filter.difficulty_category is not None:
            query["metrics.categorised_difficulty"] = "Easy"

        if examon_filter is not None and examon_filter.tags_all is not None:
            query["tags"] = {"$all": examon_filter.tags_any}

        records = self.driver["examon"]["questions"].find(query)
        return [build(result) for result in records]
