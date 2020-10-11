"""
naver_crawler_knowledge crawler setting file
"""

BOT_NAME = 'naver_crawler_knowledge'

NEWSPIDER_MODULE = 'naver_crawler_knowledge.spiders'
SPIDER_MODULES = ['naver_crawler_knowledge.spiders']

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 26

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 0

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = True

# exported data(csv, txt ..) encoding type
FEED_EXPORT_ENCODING = 'utf-8'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 ' \
             'Mobile Safari/537.36'

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'date': 'Fri, 09 Oct 2020 02:29:53 GMT',
    'content-type': 'application/json;charset=UTF-8',
    'cache-control': 'no-cache',
    'expires': 'Thu, 01 Jan 1970 00:00:00 GMT',
    'p3p': 'CP="ALL CURa ADMa DEVa TAIa OUR BUS IND PHY ONL UNI PUR FIN COM NAV INT DEM CNT STA POL HEA PRE LOC OTC',
    'referrer-policy': 'unsafe-url',
    'server': 'nfront',
    'x-requested-with': 'XMLHttpRequest'
}

RANDOM_UA_ENABLED = True
RANDOM_UA_DEFAULT_TYPE = 'mobile'
# always change user-agent
RANDOM_UA_OVERWRITE = False


# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # make UserAgent(HTTP HEADER data) random
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    'scrapy_random_useragent_pro.middleware.RandomUserAgentMiddleware': 100,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'naver_crawler_knowledge.pipelines.DuplicatesPipeline': 400,
    'naver_crawler_knowledge.pipelines.CsvPipeline': 300,
}

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = False
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

"""
bottom setting is not considered to use (2020-10-9)
"""

# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# HTTPCACHE_IGNORE_HTTP_CODES = []