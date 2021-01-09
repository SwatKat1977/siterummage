CREATE DATABASE siterummage;
USE siterummage;

CREATE TABLE domain
(
    id BIGINT AUTO_INCREMENT,
    name VARCHAR(300),

    PRIMARY KEY(id)
) DEFAULT CHARACTER SET utf8;

CREATE TABLE webpage
(
    id BIGINT AUTO_INCREMENT,
    name VARCHAR(5000),
    domain_id BIGINT,
    last_scanned DATETIME,
    read_successfully BOOLEAN,

    PRIMARY KEY(id),
    FOREIGN KEY(domain_id) REFERENCES domain(id)
) DEFAULT CHARACTER SET utf8;

CREATE TABLE webpage_metadata
(
    id BIGINT AUTO_INCREMENT,
    webpage_id BIGINT,
    title VARCHAR(4096),
    abstract VARCHAR(4096),

    PRIMARY KEY(id),
    FOREIGN KEY(webpage_id) REFERENCES webpage(id)
) DEFAULT CHARACTER SET utf8;

