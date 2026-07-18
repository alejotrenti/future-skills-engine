CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

CREATE TABLE IF NOT EXISTS gold.skill_trends (

    id SERIAL PRIMARY KEY,

    skill TEXT NOT NULL,

    category TEXT,

    users_count INTEGER,

    rank INTEGER,

    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE IF NOT EXISTS gold.skill_growth (

    id SERIAL PRIMARY KEY,

    skill TEXT NOT NULL,

    category TEXT,

    have_worked INTEGER,

    want_to_work INTEGER,

    growth_score DOUBLE PRECISION,

    rank INTEGER,

    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE IF NOT EXISTS silver.github_repositories (

    repository_id BIGINT PRIMARY KEY,

    technology TEXT,

    repo_name TEXT,

    full_name TEXT,

    owner TEXT,

    description TEXT,

    language TEXT,

    stars INTEGER,

    forks INTEGER,

    watchers INTEGER,

    open_issues INTEGER,

    license TEXT,

    topics TEXT,

    created_at TIMESTAMP,

    updated_at TIMESTAMP,

    pushed_at TIMESTAMP

);

CREATE TABLE IF NOT EXISTS gold.github_skill_momentum (

    id SERIAL PRIMARY KEY,

    technology TEXT,

    repo_count INTEGER,

    total_stars BIGINT,
    total_forks BIGINT,

    avg_stars FLOAT,
    avg_forks FLOAT,

    recent_1y_count INTEGER,
    active_repo_count INTEGER,

    stars_score FLOAT,
    forks_score FLOAT,
    repo_score FLOAT,

    recent_score FLOAT,
    active_score FLOAT,

    momentum_score FLOAT,

    rank INTEGER,

    computed_at TIMESTAMP,
    version TEXT
);

CREATE TABLE IF NOT EXISTS gold.github_topic_trends (

    id SERIAL PRIMARY KEY,

    topic TEXT,

    repo_count INTEGER,

    total_stars BIGINT,
    total_forks BIGINT,

    avg_stars FLOAT,
    avg_forks FLOAT,

    recent_1y_count INTEGER,
    active_repo_count INTEGER,

    stars_score FLOAT,
    forks_score FLOAT,
    repo_score FLOAT,

    recent_score FLOAT,
    active_score FLOAT,

    trend_score FLOAT,

    rank INTEGER,

    computed_at TIMESTAMP,
    version TEXT
);