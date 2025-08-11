# https://transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop
import asyncio
from scrapy import signals
from typing import List, Dict
from pydispatch import dispatcher
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from footballers.footballers.spiders.footballer import FootballerSpider

runner = CrawlerRunner(get_project_settings())

items: List[Dict] = []

async def run_spider(start_url: str) -> List[Dict]:
    # connect signal to collect results
    dispatcher.connect(_item_scraped, signal=signals.item_scraped)
    await runner.crawl(FootballerSpider, start_url=start_url).asFuture(asyncio.get_running_loop())
    return items

def _item_scraped(item):
    items.append(dict(item))
