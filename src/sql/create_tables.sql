CREATE DATABASE IF NOT EXISTS phonepe;
USE phonepe;

-- Aggregate Tables
CREATE TABLE aggr_transaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT NOT NULL,
    quarter INT NOT NULL,
    state VARCHAR(100),
    trans_type VARCHAR(50),
    trans_count BIGINT,
    trans_amount DECIMAL(20,2)
);

CREATE TABLE aggr_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT NOT NULL,
    quarter INT NOT NULL,
    state VARCHAR(100),
    registered_user BIGINT,
    app_opens BIGINT,
    device_brand VARCHAR(50),
    device_count BIGINT,
    device_percentage DECIMAL(20,2)
);

CREATE TABLE aggr_insurance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT NOT NULL,
    quarter INT NOT NULL,
    state VARCHAR(100),
    insurance_type VARCHAR(50),
    insurance_count BIGINT,
    insurance_amount DECIMAL(20,2)
);

-- Map Level Tables
CREATE TABLE map_transaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT NOT NULL,
    quarter INT NOT NULL,
    state VARCHAR(100),
    district VARCHAR(100),
    trans_type VARCHAR(50),
    trans_count BIGINT,
    trans_amount DECIMAL(20,2)
);

CREATE TABLE map_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT NOT NULL,
    quarter INT NOT NULL,
    state VARCHAR(100),
    district VARCHAR(100),
    registered_user BIGINT,
    app_opens BIGINT
);

CREATE TABLE map_insurance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT NOT NULL,
    quarter INT NOT NULL,
    state VARCHAR(100),
    insurance_type VARCHAR(50),
    insurance_count BIGINT,
    insurance_amount DECIMAL(20,2)
);


-- Top Level Tables 
CREATE TABLE top_transaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT NOT NULL,
    quarter INT NOT NULL,
    state VARCHAR(100),
    district VARCHAR(100),
    pincode VARCHAR(20),
    trans_type VARCHAR(50),
    trans_count BIGINT,
    trans_amount DECIMAL(20,2)
);

CREATE TABLE top_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT NOT NULL,
    quarter INT NOT NULL,
    state VARCHAR(100),
    district VARCHAR(100),
    pincode VARCHAR(20),
    registered_user BIGINT
);

CREATE TABLE top_insurance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT NOT NULL,
    quarter INT NOT NULL,
    state VARCHAR(100),
    district VARCHAR(100),
    pincode VARCHAR(20),
    insurance_type VARCHAR(50),
    insurance_count BIGINT,
    insurance_amount DECIMAL(20,2)
);