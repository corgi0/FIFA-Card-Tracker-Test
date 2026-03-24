CREATE DATABASE FifaCardTracker;

CREATE TABLE Players(
    id INT PRIMARY KEY,
    sticker_number VARCHAR,
    player_name VARCHAR,
    team VARCHAR,
    position VARCHAR,
    birth_year INT
);

CREATE TABLE Users(
    username VARCHAR PRIMARY KEY,
    account_password VARCHAR,
);

CREATE TABLE UserCards(
    username VARCHAR NOT NULL,
    player_id INT,
    PRIMARY KEY (username, player_id),
    FOREIGN KEY (username) REFERENCES Users(username),
    FOREIGN KEY (player_id) REFERENCES Players(id),
);