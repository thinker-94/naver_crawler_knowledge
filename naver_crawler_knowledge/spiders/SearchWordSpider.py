# -*- coding: utf-8 -*-

"""
made by thinker (kim young suk) for HamoniKR (https://github.com/hamonikr) opensource OS
i used scrapy framework (https://scrapy.org/) for crawling
please contact me if this code have problem or any (94thinker@gmail.com)
i enjoy to solve your problem, thank you for using my code
"""
import sys

import scrapy
from pyprnt import prnt

from ..items import SearchWordItem
import json

# this module can be used to print python(dict) type data well organized, it helps to analyze how to parse data
import pyprnt

# according to chrome browser naver client developer requests using ajax with this form data
# this data type is python type(dict)
FORM_DIC = {'query': '',
            'answer': '',
            'period': 'qna',
            'sort': 'none',
            'resultMode': 'json',
            'section': 'qna',
            'page': '',
            'pageOffset': '1',
            'isPrevPage': 'false'}

# url is used to request(http) naver knowledge mobile page
# mobile page is receiving json format data, it is easy to parse because naver knowledge api is well organized
url = "https://m.kin.naver.com/mobile/search/searchList.nhn"

# get item(variables) from items.py
# can store data by item(variable)
item = SearchWordItem()


class SearchWordSpider(scrapy.Spider):
    name = "SearchWordSpider"

    def __init__(self, words, page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # to make args to list i used split(method)
        self.wordList = words.split(',')
        # to use for loop page(type(str)) have to be type(int)
        # but i think maybe there is better way (not converting to int)
        self.page = int(page)

    # request(http) data to naver knowledge api server
    # if you send 1 request(http) you will get 20 page data
    # naver web developers receives api data by form
    # FormRequest(scrapy module) is used to request(http) form data
    # Generally form data is used for input (ex. id, password ...)
    def start_requests(self):

        for PageNumber in range(self.page):
            # put page number into FORM_DIC to request naver knowledge api by page number
            for word in self.wordList:
                FORM_DIC['page'] = str(PageNumber)
                FORM_DIC['query'] = word
                # if requests continue callback method will execute
                request = scrapy.FormRequest(url=url, formdata=FORM_DIC, callback=self.parse, meta={'ua': 'mobile'})
                yield request

    def parse(self, response, **kwargs):
        # convert type to -> type(dict)
        # used json module because response data is json format
        # ResponseToDict is type(dict) data Contains 20 page
        ResponseToDict = json.loads(response.text)

        # for loop can make naver knowledge one page according to ResponseToDict['countPerPage']
        # onPage contains 20 question data [2020/10/11]
        for onePage in range(1, ResponseToDict['countPerPage']):
            item['id'] = hash(ResponseToDict['lists'][onePage]['docId'])
            item['searchWord'] = ResponseToDict['lists'][onePage]['highlightTag']
            item['title'] = ResponseToDict['lists'][onePage]['title']
            item['questionText'] = ResponseToDict['lists'][onePage]['contents']
            yield item
