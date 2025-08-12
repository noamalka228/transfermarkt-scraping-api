import logging
import pymongo
from hashlib import sha256
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter

logger = logging.getLogger("footballers_scraper")

class MongoPipeline:
    COLLECTION_NAME = "footballer"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item_id = self.compute_item_id(item)
        if self.db[self.COLLECTION_NAME].find_one({"_id": item_id}):
            raise DropItem(f"Player {item['name']} have already been processed, skipping...")
        else:
            item["_id"] = item_id
            self.db[self.COLLECTION_NAME].insert_one(ItemAdapter(item).asdict())
            logger.info(f"Saved player {item['name']} in DB.")
            return item
        
    def compute_item_id(self, item):
        unique_id = item["name"] + item["nationality"]
        return sha256(unique_id.encode("utf-8")).hexdigest()