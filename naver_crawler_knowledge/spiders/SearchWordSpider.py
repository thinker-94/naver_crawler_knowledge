# -*- coding: utf-8 -*-
import scrapy
from pyprnt import prnt

from ..items import SearchWordItem

import json
import pyprnt

FORM_DIC = {'query': 'java',
            'answer': '',
            'period': 'qna',
            'sort': 'none',
            'resultMode': 'json',
            'section': 'qna',
            'page': '1',
            'pageOffset': '1',
            'isPrevPage': 'false'}

url = "https://m.kin.naver.com/mobile/search/searchList.nhn"


class SearchWordSpider(scrapy.Spider):
    name = "SearchWordSpider"

    def __init__(self, word, page, **kwargs):
        super().__init__(**kwargs)
        FORM_DIC['query'] = word
        self.page = int(page)

    def start_requests(self):
        for i in range(self.page):
            FORM_DIC['page'] = str(i)
            yield scrapy.FormRequest(url=url, formdata=FORM_DIC, callback=self.parse)

    def parse(self, response, **kwargs):
        # request(http) data to naver knowledge api server
        # naver web developers receives api data by form
        # FormRequest(method) is used to request(http) form data

        # get item(variables) from items.py
        # can store data by item(variable)
        item = SearchWordItem()

        # type(scrapy.http.response.text.TextResponse) convert type to -> type(str)
        responseString = response.text

        # type(scrapy.http.response.text.TextResponse) convert type to -> type(dict)
        # use json module because response data is json format
        ResponseToDict = json.loads(responseString)
        # print type(dict) pretty
        # prnt(ResponseToDict)

        for i in range(0, ResponseToDict['countPerPage']):
            print("============ title =========")
            print(ResponseToDict['lists'][i]['title'])
            print("============ content =========")
            print(ResponseToDict['lists'][i]['contents'])
            print("\n\n")

            item['duplicateFilterPass'] = ResponseToDict['lists'][i]['title']
            item['title'] = ResponseToDict['lists'][i]['title']
            item['questionContent'] = ResponseToDict['lists'][i]['contents']
            yield item

