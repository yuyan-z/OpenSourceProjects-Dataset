import requests

from utils import save_json



def get_repositories(params):
    url = 'https://api.github.com/search/repositories'
    headers = {'Accept': 'application/vnd.github+json'}
    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error: status code {response.status_code}")

    response_json = response.json()
    return response_json


if __name__ == "__main__":
    try:
        params = {
            "q": "is:public stars:>=100",
            "sort": "stars"
        }
        repositories = get_repositories(params)
        print(f"Total repositories: {repositories['total_count']}")
        save_json(repositories, "data/repositories.json")
    except Exception as e:
        print(e)

