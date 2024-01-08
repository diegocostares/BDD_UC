import scrapy
from scrapy.selector import Selector

from .items import StartBuscacursosItem


class StartBuscacursosPipeline:
    def process_item(self, item, spider):
        if isinstance(item, StartBuscacursosItem):
            pass
        return item
