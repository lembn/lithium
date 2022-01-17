import re
from data.battery import Battery
from lxml.html import fromstring
from scraper.spiders.spider import Spider


class AmazonSpider(Spider):
    def crawl(self, url, page):
        html = fromstring(self.get(f"{url}&page={page}"))
        for product in html.xpath("//div[@data-asin]"):
            if (
                len(product.get("data-asin")) > 0
                and product.get("data-asin") not in self.asins
            ):
                battery = self.scrape(product.get("data-asin"))
                if not battery:
                    continue
                yield battery

        page += 1
        if (
            self.can_recurse(page)
            and len(html.xpath('//li[@class="a-disabled a-last"]')) == 0
        ):
            yield from self.crawl(url, page)

    # TODO: at the moment we ignore batteries that dont fit our parsing format. improve this
    def scrape(self, asin):
        self.asins.append(asin)
        url = f"{self.url}/dp/{asin}"
        try:
            parsed_html = fromstring(self.get(url))
            about_list = parsed_html.xpath('//div[@id="feature-bullets"]/ul')[0]
            return Battery(
                asin,
                re.search("\d+(?=m(a|A)h)", about_list.text_content()).group(),
                re.search("\d+(?=g)", about_list.text_content()).group(),
                url,
                about_list.xpath('//span[@class="a-price"]/span')[0].text_content(),
            )
        except:
            pass
