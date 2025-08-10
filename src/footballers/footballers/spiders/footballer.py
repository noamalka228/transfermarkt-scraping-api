import scrapy
from footballers.footballers.items import FootballerItem


class FootballerSpider(scrapy.Spider):
    name = "footballer"
    allowed_domains = ["transfermarkt.com"]
    start_urls = ["https://transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop"]

    def parse(self, response):
        """
        @url https://transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop
        @returns items 1 25
        @returns request 1 50
        @scrapes name nationality market_value
        """
        players_css = response.css("tr.odd") + response.css("tr.even")
        for player in players_css:
            footballer = FootballerItem()
            footballer["name"] = player.css("td.hauptlink > a::text").get()
            footballer["nationality"] = player.css("td.zentriert > img::attr(title)").get()
            footballer["market_value"] = player.css("td.rechts.hauptlink > a::text").get()
            yield footballer

        next_page = response.css("li.tm-pagination__list-item.tm-pagination__list-item--icon-next-page > a::attr(href)").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            self.logger.info(f"Navigating to next page with URL {next_page_url}.")
            yield scrapy.Request(url=next_page_url, callback=self.parse)