CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS dds;
CREATE SCHEMA IF NOT EXISTS mart;

CREATE TABLE IF NOT EXISTS raw.transactions (
	transaction_id varchar(50),
	user_id integer,
	amount NUMERIC(12, 2),
	currency varchar(10),
	merchant varchar(100),
	status varchar(20),
	event_time timestamp,
	loaded_at timestamp DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS raw.currency_rates(
	currency varchar(10),
	rate NUMERIC(10,4),
	SCALE integer,
	rate_date date,
	loaded_at TIMESTAMP DEFAULT current_timestamp,
	PRIMARY KEY (currency, rate_date)
);