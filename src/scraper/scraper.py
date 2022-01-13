from scraper.spiders.amazon_spider import AmazonSpider

# TODO track scraper performance and if the scrape was bad recommend upgrading to the latest version

def scrape(cells: int, domain: str):
    voltage = cells * 3.7
    amazon = AmazonSpider(domain)
    amazon.crawl([f"{cells}s lipo", f"{voltage}v lipo"])
    pass
