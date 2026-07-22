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

CREATE TABLE gold.research_trends (

    id SERIAL PRIMARY KEY,

    technology TEXT,

    unique_papers INT,

    research_mentions INT,

    papers_last_year INT,

    papers_last_90_days INT,

    category_count INT,

    unique_papers_score FLOAT,

    yearly_score FLOAT,

    recent_score FLOAT,

    diversity_score FLOAT,

    research_score FLOAT,

    rank INT,

    computed_at TIMESTAMP,

    version TEXT
);

CREATE TABLE IF NOT EXISTS gold.research_growth (
    id SERIAL PRIMARY KEY,
    technology VARCHAR(100) NOT NULL,
    total_papers INTEGER DEFAULT 0,
    papers_last_year INTEGER DEFAULT 0,
    papers_previous_year INTEGER DEFAULT 0,
    growth_rate DECIMAL(10, 4),
    growth_multiplier DECIMAL(10, 2),
    papers_last_90_days INTEGER DEFAULT 0,
    active_months INTEGER DEFAULT 0,
    growth_rate_score DECIMAL(10, 2),
    recent_score DECIMAL(10, 2),
    volume_score DECIMAL(10, 2),
    consistency_score DECIMAL(10, 2),
    growth_score DECIMAL(10, 2),
    rank INTEGER,
    computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    version VARCHAR(20)
);

CREATE INDEX idx_growth_rank ON gold.research_growth(rank);
CREATE INDEX idx_growth_score ON gold.research_growth(growth_score DESC);