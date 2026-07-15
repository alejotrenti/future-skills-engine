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