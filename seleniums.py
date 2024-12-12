import random
import time

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from utils import load_json, add_to_json, string_to_int

ua = UserAgent()
options = Options()
options.add_argument(f"user-agent={ua.random}")
driver = webdriver.Chrome(options)
driver.implicitly_wait(0.5)


def crawl_user_page():
    repos = load_json("data/repositories.json")
    for i, repo in enumerate(repos):
        print(f"{i}")
        url = repo["owner"]["html_url"]
        driver.get(url)

        repo_elem = driver.find_element(By.XPATH, "//a[contains(@href, 'repositories')]//span")
        wait = WebDriverWait(driver, timeout=10)
        wait.until(lambda d: repo_elem.is_displayed())
        n_repo = string_to_int(repo_elem.text)
        item = {"id": repo["id"], "repositories_count": n_repo}
        print(item)
        add_to_json(item, "data/user_pages.json")

        sleep_time = random.randint(0, 4)
        time.sleep(sleep_time)


def crawl_issues_page():
    repo_items = load_json("data/repo_items.json")
    none_items = [d for d in repo_items if d.get("n_issue_closed") is None]
    print(len(none_items))

    for i, item in enumerate(none_items):
        issue_url = item["url"] + "/issues"
        driver.get(issue_url)

        try:
            closed_elem = driver.find_element(By.XPATH, "//a[contains(@href, 'closed')]")
            wait = WebDriverWait(driver, timeout=40)
            wait.until(lambda d: closed_elem.is_displayed())
            n_issue_closed = closed_elem.text
            n_issue_closed = n_issue_closed.split()[1]
            n_issue_closed = string_to_int(n_issue_closed)
        except:
            n_issue_closed = None

        d = {"url": item["url"], "n_issue_closed": n_issue_closed}
        print(d)
        add_to_json(d, "data/issues.json")

        sleep_time = random.randint(0, 4)
        time.sleep(sleep_time)


def craw_issue():
    wait = WebDriverWait(driver, timeout=40)
    repos = load_json("data/repositories.json")
    c = "issue-item-module__defaultNumberDescription--GXzri"
    for repo in repos:
        url = repo["html_url"] + "/issues/?q=is%3Aissue%20sort%3Acomments-desc"
        driver.get(url)

        try:
            elem = driver.find_element(By.XPATH, f'//ul[@data-testid="list"]//span[@class="{c}"]')
            wait.until(lambda d: elem.is_displayed())
            issue_id = elem.text.split()[0]
            issue_id = issue_id.replace("#", '')
            issue_id = int(issue_id)
        except:
            try:
                elem = driver.find_element(By.XPATH, f'//div[@aria-label="Issues"]/div/div[1]')
                issue_id = elem.get_attribute("id")
                issue_id = issue_id.split('_')[1]
                issue_id = int(issue_id)
            except:
                issue_id = None

        d = {"id": repo["id"], "issue_id": issue_id}
        print(d)
        add_to_json(d, "data/issue_ids.json")
        sleep_time = random.randint(0, 4)
        time.sleep(sleep_time)



if __name__ == "__main__":
    craw_issue()