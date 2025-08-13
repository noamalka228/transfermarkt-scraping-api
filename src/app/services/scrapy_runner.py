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
    logger.info("started waiting for deferred")
    def on_request(request, spider):
        logger.info("REQUEST → %s", request.url)

    def on_response(response, request, spider):
        logger.info("RESPONSE ← %s %s", response.status, response.url)

    def on_item(item):
        items.append(dict(item))

    def on_closed(spider, reason):
        logger.info("CLOSED: %s items=%d", reason, len(items))

    dispatcher.connect(on_request, signal=signals.request_scheduled)
    dispatcher.connect(on_response, signal=signals.response_received)
    dispatcher.connect(on_item, signal=signals.item_scraped)
    dispatcher.connect(on_closed, signal=signals.spider_closed)
    deferred_data = runner.crawl(FootballerSpider, start_url=start_url)
    logger.info("started waiting for deferred")
    await deferred_data.asFuture(asyncio.get_running_loop())
    logger.info(items)
    return items
