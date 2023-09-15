from typing_extensions import Protocol
from examon_core.examon_filter_options import ExamonFilterOptions
from examon_core.models.question import BaseQuestion


class FileReader(Protocol):
    def load(self, models: list) -> None:
        ...


class ContentReader(Protocol):
    def load(self, examon_filter: ExamonFilterOptions = None) -> list[BaseQuestion]:
        ...
