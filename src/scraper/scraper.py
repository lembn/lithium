from itertools import chain
from scraper.spiders import AmazonSpider
from scraper.spiders.spider import Spider


def scrape(cells: int, domain: str, pages: int, compound: str) -> tuple[int, chain]:
    voltage = round(cells * 3.7, 1)
    spiders: list[Spider] = [AmazonSpider]
    product_generators = [
        spider(
            domain, [f"{cells}s {compound}", f"{voltage}v {compound}"], pages
        ).products
        for spider in spiders
    ]
    pages = [spider.PPA * pages for spider in spiders]
    # chain products from all spiders
    return sum(pages), chain(*product_generators)
