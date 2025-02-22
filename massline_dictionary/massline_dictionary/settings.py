BOT_NAME = "massline_dictionary"

SPIDER_MODULES = ["massline_dictionary.spiders"]
NEWSPIDER_MODULE = "massline_dictionary.spiders"

USER_AGENT = "Massline Dictionary"

ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 32
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

CONCURRENT_REQUESTS = 256
CONCURRENT_REQUESTS_PER_DOMAIN = 256
RANDOMIZE_DOWNLOAD_DELAY = False
TELNETCONSOLE_ENABLED = False


ITEM_PIPELINES = {
    "massline_dictionary.pipelines.CustomImagePipeline": 100,
    "massline_dictionary.pipelines.MarkdownFilePipeline": 110,
}

ITEMS_OUTPUT_PATH = "output"
FILES_STORE = "output/images"
