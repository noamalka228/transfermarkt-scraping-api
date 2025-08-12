import os
os.environ.setdefault("SCRAPY_SETTINGS_MODULE", "footballers_scraper.settings")
import asyncio
import logging
from scrapy import signals
from typing import List, Dict
from pydispatch import dispatcher
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from footballers_scraper.spiders.footballer import FootballerSpider

logger = logging.getLogger("Scraping API")
runner = CrawlerRunner(get_project_settings())

items: List[Dict] = []

async def run_spider(start_url: str) -> List[Dict]:
    # connect signal to collect results
    dispatcher.connect(lambda item: items.append(dict(item)), signal=signals.item_scraped)
    logger.info(f"started crawling data for url: {start_url}")
    deferred_data = runner.crawl(FootballerSpider, start_url=start_url)
    logger.info("started waiting for deferred")
    await deferred_data.asFuture(asyncio.get_running_loop())
    logger.info(items)
    return items
