from examon_core.examon_filter_options import ExamonFilterOptions

from ...protocols import ContentReader


class InMemoryReader(ContentReader):
    def __init__(self, models):
        self.models = models

    def load(self, examon_filter: ExamonFilterOptions = None):
        return self.models
