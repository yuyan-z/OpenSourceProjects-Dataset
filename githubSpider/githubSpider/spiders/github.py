import scrapy
import jmespath
import sys

from utils import string_to_int, load_json


class GithubSpider(scrapy.Spider):
    name = "github"
    allowed_domains = ["github.com"]

    # repos = load_json("D:\OpenSourceProjects-Dataset\data\\repositories.json")
    # start_urls = jmespath.search('[*].html_url', repos)

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
            commits = string_to_int(commits.split()[0])
        else:
            commits = None

        contributors_elem = response.css('h2 a[href*="contributors"]')
        contributors = contributors_elem.css('span::text').get()
        if (contributors == "5,000+"):
            contributors = response.css('div.mt-3 a[href*="contributors"]::text').get()
            contributors = contributors.split()[1]
            contributors = string_to_int(contributors) + 14
        elif contributors:
            contributors = string_to_int(contributors)
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
        # with open(file='results.html', mode='w', encoding='utf-8') as f:
        #     f.write(response.text)
        # if response.status != 200:
        #     sys.exit()

        followers_elem = response.css('a[href*="followers"]')
        followers = followers_elem.css('span::text').get()
        followers = string_to_int(followers)

        location_elem = response.css("svg.octicon-location + *")
        location = location_elem.css('span::text').get()

        # repos = response.css('span.Counter::text').get()

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

class GithubSpider2(scrapy.Spider):
    name = "github2"
    allowed_domains = ["github.com"]

    # repos = load_json("D:\OpenSourceProjects-Dataset\data\\repositories.json")
    # urls = jmespath.search('[*].html_url', repos)
    # start_urls = [u + '/pulls' for u in urls]

    start_urls = ["https://github.com/freeCodeCamp/freeCodeCamp/pulls"]
    # start_urls = ["https://github.com/openai/whisper/pulls"]

    def parse(self, response):
        if response.status != 200:
            sys.exit()

        n_pull_open = response.css('a[href*="Aopen"]').get()
        if n_pull_open:
            n_pull_open = n_pull_open.split('\n')[-2].strip()
            n_pull_open = n_pull_open.split()[0]
            n_pull_open = string_to_int(n_pull_open)
        else:
            n_pull_open = None

        n_pull_closed = response.css('a[href*="Aclosed"]').get()
        if n_pull_closed:
            n_pull_closed = n_pull_closed.split('\n')[-2].strip()
            n_pull_closed = n_pull_closed.split()[0]
            n_pull_closed = string_to_int(n_pull_closed)
        else:
            n_pull_closed = None

        data = {
            "url": response.url.replace('/pulls', ''),
            "n_pull_open": n_pull_open,
            'n_pull_closed': n_pull_closed
        }

        issue_url = response.url.replace('/pulls', '/issues')

        yield scrapy.Request(issue_url, callback=self.parse_issues, meta=data)

    def parse_issues(self, response):
        if response.status != 200:
            sys.exit()

        n_issue_closed = response.css('a[href*="Aclosed"]').get()
        if n_issue_closed:
            n_issue_closed = n_issue_closed.split('\n')[-2].strip()
            n_issue_closed = n_issue_closed.split()[0]
            n_issue_closed = string_to_int(n_issue_closed)
        else:
            n_issue_closed = None

        item = {
            'url': response.meta.get("url"),
            'n_pull_open': response.meta.get("n_pull_open"),
            'n_pull_closed': response.meta.get("n_pull_closed"),
            'n_issue_closed': n_issue_closed
        }

        yield item
