# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import SearchWordItem


class SearchWordSpider(scrapy.Spider):
    name = "SearchWordSpider"

    def __init__(self, word, **kwargs):
        super().__init__(**kwargs)
        self.word = word
        self.download_delay = 5

    def start_requests(self):

        for page in range(1):
            params = {'kin_start': (page * 10) + 1}
            url = "https://search.naver.com/search.naver?where=kin&kin_display=10&query={}&sm=tab_pge&kin_start={}".format(
                self.word, params['kin_start'])
            request = scrapy.Request(url, self.parse)
            request.meta['params'] = params
            yield request

    def parse(self, response, **kwargs):
        item = SearchWordItem()

        for resultArea in response.xpath(r'//*[@id="elThumbnailResultArea"]/li'):
            title = resultArea.xpath(r'dl/dt/a')[0].extract()
            title = re.sub(r'<.*?>', '', title)
            print("#### title : %s" % title)

            content = resultArea.xpath(r'dl/dd[2]')[0].extract()
            content = re.sub(r'<.*?>', '', content)
            print("#### content : %s" % content)

            questionContent = resultArea.xpath(r'dl/dd[1]/text()')[0].extract()
            questionContent = re.sub(r'([0-9]{4}.[0-9]{2}.[0-9]{2}).*', r'\1', questionContent).replace('.', '-')
            print("#### question Date : %s" % questionContent)

            answerContent = resultArea.xpath(r'dl/dd[3]')[0].extract()
            answerContent = re.sub(r'<.*?>', '', answerContent)
            print("#### answer : %s" % answerContent)

            item['Title'] = title
            item['QuestionContent'] = content
            item['AnswerContent'] = answerContent

            yield item
