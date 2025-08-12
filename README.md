This project is meant to deliver an easy way to scrape data about football from transfermarkt.com.

##Using Poetry
The package manager is poetry.
If you want to run scrapy-based commands just run as followed:
`poetry run scrapy {your-command-here}`

For exmple, if you want to crawl something (make sure to be inside the scraper directory):
`scrapy crawl footballer -a start_url="https://transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop"`


To run the API simply run from project's root:
`uvicorn app.main:app --reload --app-dir ./src`