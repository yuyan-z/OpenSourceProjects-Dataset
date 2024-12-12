import pymysql
import json
from datetime import datetime

from utils import load_json


def insert_repos(connection, data):
    # try:
    #
    # except:
    #     print("Error")
    with connection.cursor() as cursor:
        sql = """
        INSERT INTO repositories (
            id, user_id, name, html_url, description, topics, license, language, languages, 
            created_at, updated_at, size, stargazers_count, watchers_count, forks_count, 
            contributors_count, commits_count, open_issues_count, close_issues_count, 
            open_pulls_count, close_pulls_count
        ) VALUES (
            %(id)s, %(user_id)s, %(name)s, %(html_url)s, %(description)s, %(topics)s, %(license)s, 
            %(language)s, %(languages)s, %(created_at)s, %(updated_at)s, %(size)s, %(stargazers_count)s, 
            %(watchers_count)s, %(forks_count)s, %(contributors_count)s, %(commits_count)s, 
            %(open_issues_count)s, %(close_issues_count)s, %(open_pulls_count)s, %(close_pulls_count)s
        )"""

        for d in data:
            d['topics'] = json.dumps(d['topics'])
            d['languages'] = json.dumps(d['languages'])
            d['created_at'] = datetime.strptime(d['created_at'], "%Y-%m-%dT%H:%M:%SZ")
            d['updated_at'] = datetime.strptime(d['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
            cursor.execute(sql, d)
        connection.commit()

def insert_user(connection, data):
    with connection.cursor() as cursor:
        sql = """
        INSERT INTO users (
            id, login, avatar_url, html_url, type, repositories_count, location, followers_count
        ) VALUES (
            %(id)s, %(login)s, %(avatar_url)s, %(html_url)s, %(type)s, %(repositories_count)s, %(location)s, %(followers_count)s
        )
        ON DUPLICATE KEY UPDATE
            login = VALUES(login),
            avatar_url = VALUES(avatar_url),
            html_url = VALUES(html_url),
            type = VALUES(type),
            repositories_count = VALUES(repositories_count),
            location = VALUES(location),
            followers_count = VALUES(followers_count);
        """

        for d in data:
            cursor.execute(sql, d)

        connection.commit()

if __name__ == "__main__":
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        database='ospdataset',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    # repos = load_json("final_data/repositories.json")
    # insert_repos(connection, repos)
    # users = load_json("final_data/users.json")
    # insert_user(connection, users)
    # connection.close()



