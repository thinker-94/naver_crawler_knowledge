# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from __future__ import unicode_literals
from scrapy.exporters import CsvItemExporter
from scrapy.exceptions import DropItem

import os
import time

# because avoid duplicate by title made DuplicatesPipeline class (2020-10-11)
# it save title in set(type) item['variable] and find duplicate title
class DuplicatesPipeline:

    def __init__(self):
        self.title = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['title'] in self.title:
            raise DropItem("Duplicate item found: %r" % item)
        else:
            # when title is not found in set, then item['title] add in set
            self.title.add(adapter['title'])
            return item


# CsvPipeline class exports crawled items by .csv format
class CsvPipeline(object):

    def __init__(self):
        self.file = None
        self.exporter = None

    def open_spider(self, spider):
        folderName = "SearchWordDataCSV"
        fileName = ','.join(spider.wordList)

        if not os.path.exists(folderName):
            os.makedirs(folderName)
            print("\ncreated folder to save data (project root dir)\nName : " + folderName)
            print("\nThank you for using my crawler ^^")
            print("executed after 5 second")
            time.sleep(5)

        print("\n********START********")
        self.file = open(folderName + "/" + fileName + ".csv", 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

        print("\ncsv file saved in current project root dir\n" 
                    "location : " + self.file.name)

    # can do something for item
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
