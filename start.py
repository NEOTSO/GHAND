from scrapy import cmdline

cmdline.execute('scrapy crawl hongxing1 -o result.json'.split())
# cmdline.execute('scrapy crawl httpbin'.split())