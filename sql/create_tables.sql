-- create_tables.sql  |  gerado a partir dos models SQLModel (dialeto MySQL 8)

CREATE TABLE users (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	name VARCHAR(120) NOT NULL, 
	email VARCHAR(160) NOT NULL, 
	password_hash VARCHAR(120) NOT NULL, 
	`role` ENUM('admin','operator','viewer') NOT NULL, 
	created_at DATETIME NOT NULL, 
	PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_users_email ON users (email);

CREATE TABLE cabins (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	user_id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	location VARCHAR(255) NOT NULL, 
	type ENUM('terrestre','espacial') NOT NULL, 
	installed_at DATETIME NOT NULL, 
	status ENUM('active','maintenance','inactive') NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE crops (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	cabin_id INTEGER NOT NULL, 
	species ENUM('alface','manjericao','rucula','microgreen','salsa','tomate_cereja') NOT NULL, 
	planted_at DATE NOT NULL, 
	status ENUM('germinacao','crescimento','maduro','colhido','perdido') NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(cabin_id) REFERENCES cabins (id)
);

CREATE TABLE sensors (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	cabin_id INTEGER NOT NULL, 
	type ENUM('temp_ar','umid_solo','ph','ec','luminosidade','co2','camera_visao') NOT NULL, 
	unit VARCHAR(20) NOT NULL, 
	status ENUM('active','offline','error') NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(cabin_id) REFERENCES cabins (id)
);
CREATE INDEX ix_sensors_cabin_id ON sensors (cabin_id);

CREATE TABLE alerts (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	cabin_id INTEGER NOT NULL, 
	sensor_id INTEGER, 
	severity ENUM('info','warning','critical') NOT NULL, 
	message VARCHAR(255) NOT NULL, 
	triggered_at DATETIME NOT NULL, 
	resolved BOOL NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(cabin_id) REFERENCES cabins (id), 
	FOREIGN KEY(sensor_id) REFERENCES sensors (id)
);
CREATE INDEX ix_alerts_cabin_id ON alerts (cabin_id);

CREATE TABLE readings (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	sensor_id INTEGER NOT NULL, 
	value NUMERIC(10, 2) NOT NULL, 
	read_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(sensor_id) REFERENCES sensors (id)
);
CREATE INDEX ix_readings_read_at ON readings (read_at);
CREATE INDEX ix_readings_sensor_id ON readings (sensor_id);
