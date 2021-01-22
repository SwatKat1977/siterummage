CREATE DATABASE siterummage;
USE siterummage;

CREATE TABLE webpage
(
    id BIGINT AUTO_INCREMENT,
    domain VARCHAR(300) NOT NULL,
    url_path VARCHAR(5000) NOT NULL,
    last_scanned TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    read_successful BOOLEAN NOT NULL,
    page_hash VARCHAR(32) NOT NULL,
    PRIMARY KEY(id)
) DEFAULT CHARACTER SET utf8;

CREATE TABLE webpage_metadata
(
    id BIGINT AUTO_INCREMENT,
    webpage_id BIGINT NOT NULL,
    title VARCHAR(4096) NOT NULL,
    abstract VARCHAR(4096) NOT NULL,

    PRIMARY KEY(id),
    FOREIGN KEY(webpage_id) REFERENCES webpage(id)
) DEFAULT CHARACTER SET utf8;
