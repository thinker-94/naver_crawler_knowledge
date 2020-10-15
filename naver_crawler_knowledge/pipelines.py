# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from __future__ import unicode_literals
from scrapy.exporters import CsvItemExporter
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter
from bs4 import BeautifulSoup

import os
import time


# this class is for remove duplicated data
# avoid duplicate by title
# save title in set(type) then search set(type) to find duplicated title
class DuplicatesPipeline:

    def __init__(self):
        self.text = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['text'] in self.text:
            DropItem(item)
        else:
            # when title is not found in set, then item['title] add in set
            self.text.add(adapter['text'])
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
        # remove html text
        htmlText = item['text']
        soup = BeautifulSoup(htmlText, 'html.parser')
        noHtmlText = soup.get_text()
        item['text'] = noHtmlText

        # make model label
        wordListCount = len(spider.wordList)
        label = []
        # TODO. fix for loop (because of readability)
        for i in range(0, wordListCount):
            label.append("0")
        label[spider.wordIndex] = "1"
        label = ','.join(label)
        print(label)

        self.exporter.export_item(item)
        return item
