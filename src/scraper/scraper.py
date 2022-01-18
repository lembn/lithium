from itertools import chain
from scraper.spiders import AmazonSpider
from scraper.spiders.spider import Spider

# TODO: precaulculate the number of items (using `pages` * items per page) to make prog bar
def scrape(cells: int, domain: str, pages: int) -> tuple(int, chain):
    voltage = round(cells * 3.7, 1)
    # TODO: add other spiders to support more sites
    spiders: list[Spider] = [AmazonSpider]
    product_generators = [spider(domain, [f"{cells}s lipo", f"{voltage}v lipo"], pages).products for spider in spiders]
    pages = [spider.PPA * pages for spider in spiders]
    # chain products from all spiders
    return sum(pages), chain(*product_generators)
