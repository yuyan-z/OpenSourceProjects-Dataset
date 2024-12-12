USE ospdataset;
CREATE TABLE IF NOT EXISTS repositories (
    id BIGINT PRIMARY KEY,
    user_id BIGINT,
    name VARCHAR(255),
    html_url VARCHAR(500),
    description LONGTEXT,
    topics TEXT,
    license VARCHAR(50),
    language VARCHAR(50),
    languages TEXT,
    created_at DATETIME,
    updated_at DATETIME, 
    size INT,
    stargazers_count INT,
    watchers_count INT,
    forks_count INT,
    contributors_count INT,
    commits_count INT,
    open_issues_count INT,
    close_issues_count INT,
    open_pulls_count INT,
    close_pulls_count INT
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    login VARCHAR(255),
    avatar_url TEXT,
    html_url TEXT,
    type VARCHAR(50),
    repositories_count INT,
    location VARCHAR(255),
    followers_count INT
) DEFAULT CHARSET=utf8mb4;

