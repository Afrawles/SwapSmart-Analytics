DROP SCHEMA IF EXISTS swapsmart_schema CASCADE;

CREATE SCHEMA swapsmart_schema;

SET search_path TO swapsmart_schema,public;

-- Table creation

-- create clients table
DROP TABLE IF EXISTS swapsmart_schema.clients;

CREATE TABLE swapsmart_schema.clients (
    client_id BIGINT NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phone_number VARCHAR(50) NOT NULL,
    address VARCHAR(255) NOT NULL,
    status VARCHAR(15) NOT NULL,
    created_datetime VARCHAR(100) NOT NULL,
    update_datetime VARCHAR(100) NOT NULL,

    PRIMARY KEY(client_id)
    
);

-- create batteries table
DROP TABLE IF EXISTS swapsmart_schema.batteries;

CREATE TABLE swapsmart_schema.batteries (
    battery_id BIGINT NOT NULL,
    capacity BIGINT NOT NULL,
    status VARCHAR(15) NOT NULL,
    created_datetime VARCHAR(100) NOT NULL,
    update_datetime VARCHAR(100) NOT NULL,

    PRIMARY KEY(battery_id)
    
);

-- create bikes table
DROP TABLE IF EXISTS swapsmart_schema.bikes;

CREATE TABLE swapsmart_schema.bikes (
    bike_id BIGINT NOT NULL,
    client_id BIGINT NOT NULL REFERENCES clients (client_id),
    status VARCHAR(15) NOT NULL,
    created_datetime VARCHAR(100) NOT NULL,
    update_datetime VARCHAR(100) NOT NULL,

    PRIMARY KEY(bike_id)
    
);


-- create table stations

DROP TABLE IF EXISTS swapsmart_schema.stations;

CREATE TABLE swapsmart_schema.stations (
    station_id BIGINT NOT NULL,
    station_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(50) NOT NULL,
    address VARCHAR(255) NOT NULL,
    status VARCHAR(15) NOT NULL,
    created_datetime VARCHAR(100) NOT NULL,
    update_datetime VARCHAR(100) NOT NULL,

    PRIMARY KEY(station_id)
);

-- create attendants table
DROP TABLE IF EXISTS swapsmart_schema.attendants;

CREATE TABLE swapsmart_schema.attendants (
    attendant_id BIGINT NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phone_number VARCHAR(50) NOT NULL,
    address VARCHAR(255) NOT NULL,
    status VARCHAR(15) NOT NULL,
    created_datetime VARCHAR(100) NOT NULL,
    update_datetime VARCHAR(100) NOT NULL,

    PRIMARY KEY(attendant_id)
    
);

-- create transaction table
DROP TABLE IF EXISTS swapsmart_schema.transactions;

CREATE TABLE swapsmart_schema.transactions (
    transaction_id BIGSERIAL,
    timestamp VARCHAR(100) NOT NULL,
    client_id BIGINT NOT NULL REFERENCES clients (client_id),
    battery_given_out BIGINT NOT NULL REFERENCES batteries (battery_id),
    battery_received BIGINT NOT NULL REFERENCES batteries (battery_id),
    bike_id BIGINT NOT NULL REFERENCES bikes (bike_id),
    station_id BIGINT NOT NULL REFERENCES stations (station_id),
    attendant_id BIGINT NOT NULL REFERENCES attendants (attendant_id),
    battery_given_soc BIGINT NOT NULL,
    battery_received_soc BIGINT NOT NULL,
    battery_usage_diff BIGINT NOT NULL,
    discount VARCHAR(20) NOT NULL,
    transaction_amount NUMERIC(10,2) NOT NULL,

    PRIMARY KEY (transaction_id),
    CONSTRAINT unique_client_timestamp UNIQUE (client_id, timestamp)
);