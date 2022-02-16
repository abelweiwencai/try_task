DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS comment;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE comment (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  parent_id INTEGER not null,
  content TEXT NOT NULL,
  depth INTEGER not null default 0,
  depth_id INTEGER not null default 0,
  path TEXT NOT NULL default '/',
  parent_path TEXT NOT NULL default '/',
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (author_id) REFERENCES user (id)
);