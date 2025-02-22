import scrapy
from scrapy.spiders import CrawlSpider


class MasslineSpider(CrawlSpider):
    name = "massline"
    allowed_domains = ["massline.org"]

    def start_requests(self):
        yield scrapy.Request(
            url="https://massline.org/Dictionary/index.htm",
            callback=self.parse_entries
        )

    def parse_entries(self, response):
        entries = response.xpath(
            """//blockquote/blockquote/font["size='+1'"]/a/@href"""
        ).extract()
        for entry in entries:
            yield scrapy.Request(
                url=response.urljoin(entry),
                callback=self.parse_dictionary_page
            )

    def parse_dictionary_page(self, response):
        seen_titles = set()
        for entry in response.xpath('//p[@class="hang"]'):
            title = "".join(entry.xpath(".//b//text()").getall()).strip()
            if not title:
                title = "".join(entry.xpath(".//text()").getall()).strip()
            if title and title not in seen_titles:
                seen_titles.add(title)
                entry_html = entry.get()
                for sib in entry.xpath("following-sibling::*"):
                    tag = sib.root.tag.lower()
                    if tag == "p" and "hang" in (sib.xpath("@class").get() or ""):
                        break
                    if tag == "hr":
                        break
                    if sib.xpath('.//a[contains(., "Dictionary Home Page")]'):
                        break
                    entry_html += sib.get()
                imgs = (
                    response.selector.__class__(text=entry_html)
                    .xpath("//img/@src")
                    .extract()
                )
                imgs = [response.urljoin(url) for url in imgs]

                yield {
                    "title": title,
                    "body": entry_html,
                    "image_urls": imgs,
                }
