DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS loan;
DROP TABLE IF EXISTS transactions;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created FLOAT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  amount FLOAT NOT NULL,
  status_of_request TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE loan (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  loan_author_id INTEGER NOT NULL,
  other_username TEXT NOT NULL,
  request_post_id INTEGER NOT NULL,
  pay_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  loan_amount FLOAT NOT NULL,
  money_type TEXT NOT NULL,
  FOREIGN KEY (loan_author_id) REFERENCES user (id)
);

CREATE TABLE transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  hashed_transac TEXT NOT NULL,
  amnt FLOAT NOT NULL
)