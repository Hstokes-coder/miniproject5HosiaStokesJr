-- Database schema for the IT Help Desk.
-- Running `flask --app helpdesk init-db` executes this file.
-- WARNING: the DROP statements erase existing data, so only run init-db
-- when you want a fresh, empty database.

DROP TABLE IF EXISTS ticket;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL            -- stores a hash, never the plain password
);

CREATE TABLE ticket (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,         -- who submitted the ticket
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  priority TEXT NOT NULL DEFAULT 'Medium'
    CHECK (priority IN ('Low', 'Medium', 'High')),
  status TEXT NOT NULL DEFAULT 'Open'
    CHECK (status IN ('Open', 'In Progress', 'Closed')),
  FOREIGN KEY (user_id) REFERENCES user (id)
);
