BOT_NAME = "scraper"

SPIDER_MODULES = ["src.scraper.spiders"]
NEWSPIDER_MODULE = "src.scraper.spiders"


ROBOTSTXT_OBEY = False
# REDIRECT_ENABLED = True
DUPEFILTER_DEBUG = True  # permite solicitudes duplicadas

LOG_LEVEL = "INFO"  # INFO OR ERROR OR DEBUG
DOWNLOAD_DELAY = 0.8
DOWNLOAD_TIMEOUT = 360
TELNETCONSOLE_ENABLED = False
USER_AGENT = "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188"

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

COOKIES_ENABLED = True

# Pipelines: Mientras más bajo el número, más temprano se ejecuta
# ITEM_PIPELINES = {
#     "src.scraper.pipelines.StartBuscacursosPipeline": 300,
# }

LOG_STDOUT = True

####################################################
# Playwright settings: En caso de que se quiera incluir js
####################################################
# PLAYWRIGHT_ABORT_REQUEST = "src.scraper.utils.should_abort_request"

# DOWNLOAD_HANDLERS = {
#     "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
#     "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
# }
# PLAYWRIGHT_CONCURRENCY = 10
# PLAYWRIGHT_MAX_CONTEXTS = 8
# PLAYWRIGHT_MAX_PAGES_PER_CONTEXT = 8
# PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 400000
