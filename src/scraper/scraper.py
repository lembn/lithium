from itertools import chain
from scraper.spiders import AmazonSpider

# TODO: precaulculate the number of items (using `pages` * items per page) to make prog bar
def scrape(cells: int, domain: str, pages: int) -> chain:
    voltage = round(cells * 3.7, 1)
    amazon = AmazonSpider(domain, [f"{cells}s lipo", f"{voltage}v lipo"], pages)
    # TODO: add other spiders to support more sites
    return chain(amazon.products)  # chain products from all spiders
