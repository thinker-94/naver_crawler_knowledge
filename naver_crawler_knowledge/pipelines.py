# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from __future__ import unicode_literals

import datetime

from scrapy.exporters import CsvItemExporter

import os
import time
from lazyme.string import color_print


from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class DuplicatesPipeline:

    def __init__(self):
        self.title = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['title'] in self.title:
            raise DropItem("Duplicate item found: %r" % item)
        else:
            self.title.add(adapter['title'])
            return item


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
        now = datetime.datetime.now()
        print(now)
        self.exporter.finish_exporting()
        self.file.close()

        color_print("\ncsv file saved in current project root dir\n" 
                    "location : " + self.file.name, color='red')

    # can do something for item
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
