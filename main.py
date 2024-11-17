import requests

from utils import save_json


def get_repositories():
    url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
    headers = {'Accept': 'application/vnd.github.v3+json'}
    response = requests.get(url, headers=headers)
    print(f"Status code: {response.status_code}")
    response_json = response.json()
    return response_json


if __name__ == "__main__":
    data = get_repositories()
    print(f"Total repositories: {data['total_count']}")
    save_json(data, "repositories_python.json")
