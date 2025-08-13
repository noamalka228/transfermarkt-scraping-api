import logging
import scrapy
from typing import List
from footballers_scraper.items import FootballerItem

logger = logging.getLogger("footballers_scraper")
logging.getLogger("pymongo").setLevel(logging.WARNING)


class FootballerSpider(scrapy.Spider):
    name: str = "footballer"
    allowed_domains = ["transfermarkt.com", "www.transfermarkt.com",
                   "transfermarkt.us", "www.transfermarkt.us"]
    
    def __init__(self, start_url, **kwargs):
        super().__init__(**kwargs)
        self.start_urls: List[str] = [start_url]

    def parse(self, response):
        """
        @url https://transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop
        @returns items 1 25
        @returns request 1 50
        @scrapes name nationality market_value
        """
        logger.info(f"Started Parsing Page")
        players_css = response.css("tr.odd") + response.css("tr.even")
        for player in players_css:
            footballer = FootballerItem()
            footballer["name"] = player.css("td.hauptlink > a::text").get()
            footballer["nationality"] = player.css("td.zentriert > img::attr(title)").get()
            footballer["market_value"] = player.css("td.rechts.hauptlink > a::text").get()
            logger.info(f"Started handling {footballer['name']}")
            yield footballer

        next_page = response.css("li.tm-pagination__list-item.tm-pagination__list-item--icon-next-page > a::attr(href)").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            self.logger.info(f"Navigating to next page with URL {next_page_url}.")
            yield scrapy.Request(url=next_page_url, callback=self.parse)
