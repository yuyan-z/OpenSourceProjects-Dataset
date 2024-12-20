import json
import time

import requests
import jmespath

from utils import save_json, get_last_file_name, load_all_json, load_json, add_to_json

token = ''
HEADERS = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'token {token}'
}


def get_all_page(url, params):
    results = []
    page = 1
    while True:
        print(f'Getting page {page}')
        params["page"] = page
        response = requests.get(url, params=params, headers=HEADERS)

        if response.status_code != 200:
            raise Exception(f"Error: status code {response.status_code}")

        response_json = response.json()
        results.append(response_json)
        if len(response_json['items']) == 0:
            break
        else:
            page += 1

    return results


def get_repos_by_stars(stars=10000):
    url = 'https://api.github.com/search/repositories'
    params = {
        "q": f"is:public stars:>={stars}",
        "sort": "stars",
        "per_page": 100,
    }

    total_count = 0
    response = requests.get(url, params=params, headers=HEADERS)
    if response.status_code == 200:
        total_count = response.json()['total_count']
    print(f"Total repositories stars>={stars}: {total_count}")

    res = load_all_json("data/repository/")
    print(f"Count: {len(res)} / {total_count}")

    begin = stars
    last_file_name = get_last_file_name("data/repository/")
    last_file_name = last_file_name.replace(".json", "")
    if last_file_name:
        begin = int(last_file_name.split("_")[-1]) + 1

    end = begin + 1000 - 1

    try:
        print(f"Getting repositories with stars:{begin}..{end}")
        params["q"] = f"is:public stars:{begin}..{end}"
        response_json = get_all_page(url, params)
        repos = jmespath.search('[*].items[*]', response_json)
        repos = sum(repos, [])
        if len(repos) > 0:
            print(f"Number of repositories: {len(repos)}")
            save_json(repos, f"data/repository/stars_{begin}_{end}.json")
    except Exception as e:
        print(e)


def get_languages():
    repos = load_json("data/repositories.json")
    languages = load_json("data/languages.json")

    ids = jmespath.search('[*].id', languages)

    rs = [repo for repo in repos if repo["id"] not in ids]
    print('len rs', len(rs))

    print(f"Getting languages for repository...")
    for i, repo in enumerate(rs):
        print(f"{i}")
        languages_url = repo["languages_url"]
        response = requests.get(languages_url, headers=HEADERS)
        if response.status_code == 200:
            response_json = response.json()
            languages.append({"id": repo["id"], "languages": response_json})
            time.sleep(3)
        else:
            print(f"Error: status code {response.status_code}")
            print(len(languages))
            save_json(languages, "data/languages.json")
            t = int(response.headers['X-RateLimit-Reset']) - int(time.time())
            if t < 0: t = 0
            print(f"sleep: {t + 60}")
            time.sleep(t)
            # break
    save_json(languages, "data/languages.json")


if __name__ == "__main__":
    # # Get repositories
    # repos = get_repos_by_stars(10000)

    get_languages()




