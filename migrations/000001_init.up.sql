CREATE TABLE IF NOT EXISTS channels(
    id            INT PRIMARY KEY,
    username      TEXT UNIQUE,
    title         TEXT,
    description   TEXT
);

CREATE TABLE IF NOT EXISTS posts(
    id          SERIAL,
    post_id     INT,
    channel_id  INT,
    date        TIMESTAMP,
    message     TEXT,
    media_url   TEXT
);