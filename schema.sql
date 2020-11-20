CREATE DATABASE kasino;
USE kasino;
CREATE TABLE player
(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    username VARCHAR(200) NOT NULL,
    level INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT level_ck CHECK (level IN (1, 2, 3)),
    UNIQUE KEY unique_username (username)
);
CREATE TABLE history
(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    player_id INT,
    level INT,
    nb_try INT,
    bet INT,
    gain INT,
    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT level_history_ck CHECK (level IN (1, 2, 3)),
    INDEX par_ind (player_id),
    FOREIGN KEY (player_id)
        REFERENCES player(id)
        ON DELETE CASCADE
);