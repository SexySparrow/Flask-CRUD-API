CREATE TABLE cargo (
	id serial PRIMARY KEY,
	transport_name VARCHAR ( 100 ) NOT NULL,
	transport_phone_number VARCHAR ( 10 ) NOT NULL,
	transport_truck_number VARCHAR ( 8 ) NOT NULL,
	transport_cargo_type VARCHAR ( 50 ) NOT NULL,
	transport_cargo_description VARCHAR ( 400 ) NOT NULL,
	transport_departure_time DATE NOT NULL,
	transport_departure_location VARCHAR ( 100 ) NOT NULL,
	transport_arrival_location VARCHAR ( 100 ) NOT NULL,
	transport_weight INT
);
