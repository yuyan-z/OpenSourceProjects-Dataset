import json
import os

import jmespath


def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")


def load_json(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding {f}: {e}")
    return data


def load_all_json(folder_path):
    data_list = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            data = load_json(file_path)
            data_list.extend(data)

    return data_list


def get_last_file_name(folder_path):
    last_file_name = ''
    lst = os.listdir(folder_path)
    if (len(lst) > 0):
        last_file_name = lst[-1]
    return last_file_name


def kstring_to_int(s):
    if s:
        if s.endswith('k'):
            return int(float(s[:-1]) * 1000)
        else:
            return int(s)
    else:
        return None


if __name__ == '__main__':
    # repositories = load_json("data/repositories.json")
    # items = load_json("data/items1.json")
    # html_urls = jmespath.search('[*].html_url', repositories)
    # items_urls = jmespath.search('[*].url', items)
    # urls = [url for url in html_urls if url not in items_urls]
    # print(len(urls))
    # print(urls)

    # save_json(urls, "data/urls.json")
    #
    items = load_json("data/items.json")
    print(len(items))
    #
    # seen_ids = set()
    # unique_data = []
    # for item in items:
    #     if item['url'] not in seen_ids:
    #         unique_data.append(item)
    #         seen_ids.add(item['url'])
    #
    # save_json(unique_data, "data/items1.json")

