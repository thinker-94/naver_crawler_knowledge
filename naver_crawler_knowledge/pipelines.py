# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from __future__ import unicode_literals
from scrapy.exporters import CsvItemExporter
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter

import os
import time

# this class is for remove duplicated data
# avoid duplicate by title
# save title in set(type) then search set(type) to find duplicated title
class DuplicatesPipeline:

    def __init__(self):
        self.title = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['title'] in self.title:
            DropItem(item)
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
            print("\ncreated folder to save data (your current directory)\nName : " + folderName)
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
        print(item['title'])
        self.exporter.export_item(item)
        return item
