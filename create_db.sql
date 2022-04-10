CREATE TABLE report_list ( 
	reportID INT NOT NULL PRIMARY KEY AUTO_INCREMENT, 
	type CHAR(50) NOT NULL, 
	timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
	latitude DOUBLE, 
	longitude DOUBLE, 
	reporter CHAR(100), 
	description CHAR(255)
);

CREATE TABLE source_list (
	sourceID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	type CHAR(50) NOT NULL,
	latitude DOUBLE,
	longitude DOUBLE,
	description CHAR(255)
);
