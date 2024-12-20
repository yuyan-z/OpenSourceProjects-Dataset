# OpenSourceProjects-Dataset
Here's the link to our project on GitHub: https://github.com/yuyan-z/OpenSourceProjects-Dataset

## Data Acquiring with API
1. Get repositories. For example, we are interested in repositories with stars greater than 10000. 
```get_repos_by_stars(stars=10000)```

2. Extract the languages_urls in the repositories results, get languages for each repositories. 
```get_languages()```

## Data Acquiring with Scrapy
3. Use ```GithubSpider``` to craw the repository page and its owner page, extract data commits_count, contributors_count, user followers_count, user location.

4. Use ```GithubSpider2``` to craw the pulls page and issues page, extract data pull_open_count, pull_closed_count, issue_closed_count

## Data Acquiring with Selenium
5. Use ```crawl_user_page()``` to extract user repositories_count

6. Use ```crawl_issues_page``` to extract issues data

## Data Storing with MySQL
7. Use ```script.sql``` to create tables

8. Insert data to tables with ```mysqls.py```