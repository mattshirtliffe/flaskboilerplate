CREATE TABLE user (
	id INTEGER NOT NULL, 
	username VARCHAR(80), 
	email VARCHAR(120), 
	password VARCHAR(255), 
	active BOOLEAN, 
	authenticated BOOLEAN, 
	anonymous BOOLEAN, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	UNIQUE (email), 
	UNIQUE (password), 
	CHECK (active IN (0, 1)), 
	CHECK (authenticated IN (0, 1)), 
	CHECK (anonymous IN (0, 1))
);
CREATE TABLE entries (
	id INTEGER NOT NULL, 
	title VARCHAR, 
	text VARCHAR, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
