# -*- coding: utf-8 -*-

"""
made by thinker (kim young suk) for HamoniKR (https://github.com/hamonikr) opensource OS
i used scrapy framework (https://scrapy.org/) for crawling
please contact me if this code have problem or any (94thinker@gmail.com)
enjoy to solve your problem, thank you for using my code
(* to avoid NAVER crawler defender i changed some scrapy framework code if you want send e-mail)
"""

import scrapy

from naver_crawler_knowledge.items import SearchWordItem
import json

# according to chrome browser NAVER client developer requests using ajax with this form data
# this data type is python type(dict)
FORM_DIC = {'query': '',
            'answer': '',
            'period': 'qna',
            'sort': 'none',
            'resultMode': 'json',
            'section': 'qna',
            'page': '900',
            'pageOffset': '1',
            'isPrevPage': 'false'}

# url is used to request(http) NAVER knowledge mobile page
# mobile page is receiving json format data, it is easy to parse because NAVER knowledge api is well organized
url = "https://m.kin.naver.com/mobile/search/searchList.nhn"

# get item(variables) from items.py
# can store data by item(variable)
item = SearchWordItem()

class SearchWordSpider(scrapy.Spider):
    # scrapy know this crawler by name(variable) and can executed
    name = "SearchWordSpider"
    # get some arguments from users (ex. words, page, delay ...)
    def __init__(self, words, page, delay, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # to make args to list i used split(method)
        self.wordList = words.split(',')
        # to use for loop page(str) have to be type(int)
        # but i think maybe there is better way (not converting to int)
        self.pageNum = int(page)
        # controls request delay(second)
        # use super class variable
        self.download_delay = int(delay)

    # request(http) data to NAVER knowledge api server
    # if you send 1 request(http) then 20 question data will return
    def start_requests(self):
        for pageNum in range(self.pageNum):
            # put page number into FORM_DIC to request NAVER knowledge api by page number
            for word in self.wordList:
                FORM_DIC['page'] = str(pageNum)
                FORM_DIC['query'] = word
                # NAVER web developers receives api data by form
                # FormRequest(scrapy module) is used to request(http) form data
                # Generally form data is used for input (ex. id, password ...)
                # if requests continue callback method will execute
                request = scrapy.FormRequest(url=url, formdata=FORM_DIC, callback=self.parse, meta={'ua': 'mobile'})
                yield request

    # parsing data from response
    # response come from start_request(method)
    # i parsed python type(dic) it is easy to get data
    def parse(self, response, **kwargs):
        # convert type to -> type(dict)
        # used json module because response data is json format
        # qDic(valuable) is type(dict) data Contains 20 item(question data in NAVER Knowledge Api)
        qDic = json.loads(response.text)

        # for loop can make NAVER knowledge one page according to qDic['countPerPage']
        # onPage contains 20 question data [2020/10/11]
        for onePage in range(1, qDic['countPerPage']):
            item['title'] = qDic['lists'][onePage]['title']
            item['questionText'] = qDic['lists'][onePage]['contents']
            yield item
