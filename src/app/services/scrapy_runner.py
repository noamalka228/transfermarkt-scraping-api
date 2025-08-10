from crochet import setup, wait_for
setup()  # starts Twisted reactor in a thread (safe to call once)

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from pydispatch import dispatcher
from scrapy import signals
from typing import List, Dict
from footballers.footballers.spiders.footballer import FootballerSpider

runner = CrawlerRunner(get_project_settings())

@wait_for(timeout=60.0)  # block until done (timeout optional)
def run_spider(start_url: str) -> List[Dict]:
    items: List[Dict] = []

    def _item_scraped(item):
        items.append(dict(item))

    # connect signal to collect results
    dispatcher.connect(_item_scraped, signal=signals.item_scraped)

    d = runner.crawl(FootballerSpider, start_url=start_url)
    d.addBoth(lambda _: items)  # return collected items when crawl finishes
    return d  # Crochet turns this Deferred into a normal return value
