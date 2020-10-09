# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from __future__ import unicode_literals
from scrapy.exporters import JsonItemExporter, CsvItemExporter
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

duplicate = False


class DuplicatesPipeline:

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['duplicateFilterPass'] in self.ids_seen:
            item['duplicateFilterPass'] = False
            raise DropItem("Duplicate item found: %r" % item)
        else:
            item['duplicateFilterPass'] = True
            self.ids_seen.add(adapter['duplicateFilter'])
            return item


class CsvPipeline(object):
    def __init__(self):
        self.file = open("crawler_data.csv", 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        if duplicate:
            item['duplicateFilterPass'] = "fail(duplicated)"
        else:
            item['duplicateFilterPass'] = "success(not duplicated)"
        self.exporter.export_item(item)
        return item

# class JsonPipeline(object):
#     def __init__(self):
#         self.file = open("crawler_data.json", 'wb')
#         self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
#         self.exporter.start_exporting()
#
#     def close_spider(self, spider):
#         self.exporter.finish_exporting()
#         self.file.close()
#
#     def process_item(self, item, spider):
#         return item
