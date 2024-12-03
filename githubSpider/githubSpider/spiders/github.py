import time

import scrapy
import jmespath
import sys

from utils import kstring_to_int, load_json


class GithubSpider(scrapy.Spider):
    name = "github"
    allowed_domains = ["github.com"]

    # repositories = load_json("D:\OpenSourceProjects-Dataset\data\\urls.json")
    # start_urls = jmespath.search('[*].html_url', repositories)

    start_urls = ["https://github.com/freeCodeCamp/freeCodeCamp"]
    # start_urls = ["https://github.com/labuladong/fucking-algorithm"]
    # start_urls = ["https://github.com/labuladong"]
    # start_urls = ["https://github.com/freeCodeCamp"]

    def parse(self, response):
        # with open(file='results.html', mode='w', encoding='utf-8') as f:
        #     f.write(response.text)
        # if response.status != 200:
        #     sys.exit()

        commits = response.css('#history-icon-button-tooltip::attr(aria-label)').get()
        if commits:
            commits = int(commits.split()[0].replace(',', ''))
        else:
            commits = None

        contributors_elem = response.css('h2 a[href*="contributors"]')
        contributors = contributors_elem.css('span::text').get()
        if (contributors == "5,000+"):
            contributors = response.css('div.mt-3 a[href*="contributors"]::text').get()
            contributors = contributors.split()[1]
            contributors = int(contributors.replace(',', '')) + 14
        elif contributors:
            contributors = int(contributors.replace(',', ''))
        else:
            contributors = None

        owner_url = "https://github.com" + response.css('a[rel="author"]::attr(href)').get()

        data = {
            "url": response.url,
            "commits": commits,
            "contributors": contributors
        }
        yield scrapy.Request(owner_url, callback=self.parse_owner, meta=data)


    def parse_owner(self, response):
        # if response.status != 200:
        #     sys.exit()

        followers_elem = response.css('a[href*="followers"]')
        followers = followers_elem.css('span::text').get()
        followers = kstring_to_int(followers)

        location_elem = response.css("svg.octicon-location + *")
        location = location_elem.css('span::text').get()

        # repositories = response.css('span.Counter::text').get()

        item = {
            "url": response.meta.get("url"),
            "commits": response.meta.get("commits"),
            "contributors": response.meta.get("contributors"),
            "owner": {
                "followers": followers,
                "location": location
            }
        }

        yield item






