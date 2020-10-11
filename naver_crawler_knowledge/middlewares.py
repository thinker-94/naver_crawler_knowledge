# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.spidermiddlewares.httperror import HttpError, logger
from scrapy.utils.python import without_none_values


# DefaultHeadersMiddleware(class) is handling http Header
# you can change header(http) data by settings.py -> DEFAULT_REQUEST_HEADERS
class DefaultHeadersMiddleware:

    def __init__(self, headers):
        self._headers = headers

    @classmethod
    def from_crawler(cls, crawler):
        headers = without_none_values(crawler.settings['DEFAULT_REQUEST_HEADERS'])
        return cls(headers.items())

    def process_request(self, request, spider):
        for k, v in self._headers:
            request.headers.setdefault(k, v)