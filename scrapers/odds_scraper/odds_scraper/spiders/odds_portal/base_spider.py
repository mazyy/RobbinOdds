from abc import abstractmethod
from scrapy import Request, Spider

class BaseSpider(Spider):
    """Template method: crawl → parse_items → follow links → repeat."""

    custom_settings = {
        'CONCURRENT_REQUESTS': 4,
        'DOWNLOAD_DELAY': 0.5,
    }

    headers = dict()
    endpoint_headers = dict()

    def start_requests(self):
        for url in getattr(self, 'start_urls', []):
            yield Request(url, callback=self.parse, headers=self.headers)

    def parse(self, response, **kwargs):
        # 1) Extract domain‐specific items
        yield from self.parse_items(response)

        # 2) Discover next URLs to crawl
        for next_url in self.parse_next_link(response):
            yield response.follow(next_url, callback=self.parse, headers=self.headers)

    @abstractmethod
    def parse_items(self, response):
        """Extract and yield Item objects from this page."""
        return []

    @abstractmethod
    def parse_next_link(self, response):
        """Return list of URLs (or url fragments) to follow."""
        return []
