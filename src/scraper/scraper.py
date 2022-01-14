from itertools import chain
from scraper.spiders import AmazonSpider


def scrape(cells: int, domain: str):
    voltage = round(cells * 3.7, 1)
    amazon = AmazonSpider(domain, [f"{cells}s lipo", f"{voltage}v lipo"])
    # ... other spiders here
    return chain(amazon.products)  # chain products from all spiders
