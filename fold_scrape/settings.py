# Scrapy settings for fold_scrape project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import logging
from logging.handlers import TimedRotatingFileHandler
import os
import glob ,time

# Function to delete old log files beyond 10 days
def delete_old_logs(log_dir, file_pattern="*.log", days=10):
    for log_file in glob.glob(os.path.join(log_dir, file_pattern)):
        file_creation_time = os.path.getctime(log_file)
        if (time.time() - file_creation_time) // (24 * 3600) >= days:
            os.remove(log_file)

# Directory to store log files
LOG_DIR = 'logs'

# Ensure the log directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Delete log files older than 10 days
delete_old_logs(LOG_DIR)

# Configure the logging settings
LOG_LEVEL = 'ERROR'  # Only log errors and above
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'

# Configure the logger
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)

# Timed rotating file handler for creating a new log file every day
log_file_handler = TimedRotatingFileHandler(
    filename=os.path.join(LOG_DIR, 'scrapy_log.log'),
    when='midnight',
    interval=1,
    backupCount=10  # Keep up to 10 backup log files
)
log_file_handler.setLevel(LOG_LEVEL)
log_file_handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATEFORMAT))
logger.addHandler(log_file_handler)


BOT_NAME = "fold_scrape"

SPIDER_MODULES = ["fold_scrape.spiders"]
NEWSPIDER_MODULE = "fold_scrape.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "fold_scrape (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "fold_scrape.middlewares.FoldScrapeSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "fold_scrape.middlewares.FoldScrapeDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

ITEM_PIPELINES = {
    'fold_scrape.pipelines.FoldScrapePipeline': 300,
}

