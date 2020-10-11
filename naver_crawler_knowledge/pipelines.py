# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from __future__ import unicode_literals

from scrapy.exporters import CsvItemExporter

import os
import time
from lazyme.string import color_print


# duplicate = False


# to filter duplicated data
# class DuplicatesPipeline:
#
#     def __init__(self):
#         self.ids_seen = set()
#
#     def process_item(self, item, spider):
#         adapter = ItemAdapter(item)
#         if adapter['duplicateFilterPass'] in self.ids_seen:
#             item['duplicateFilterPass'] = False
#             raise DropItem("Duplicate item found: %r" % item)
#         else:
#             item['duplicateFilterPass'] = True
#             self.ids_seen.add(adapter['duplicateFilter'])
#             return item


class CsvPipeline(object):

    def __init__(self):
        self.file = None
        self.exporter = None

    def open_spider(self, spider):
        folderName = "SearchWordDataCSV"
        fileName = ','.join(spider.wordList) + "[page:" + str(spider.page) + "]"

        if not os.path.exists(folderName):
            os.makedirs(folderName)
            color_print("\ncreated folder to save data (project root dir)\nName : " + folderName, color='red')
            color_print("\nThank you for using my crawler ^^", color='blue')
            color_print("executed after 5 second")
            time.sleep(5)
            color_print("\n********START********", color='red')
        self.file = open(folderName + "/" + fileName + ".csv", 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

        color_print("\ncsv file saved in current project root dir\n" 
                    "location : " + self.file.name, color='red')

    # can do something for item
    def process_item(self, item, spider):
        # print(item['title'])
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
