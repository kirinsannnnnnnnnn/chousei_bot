-- query to create weight table.
CREATE TABLE weight_table (
	log_id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id TEXT,
	user_weight REAL,
	logged_date INTEGER);
