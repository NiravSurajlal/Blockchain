DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS single_transaction;
DROP TABLE IF EXISTS genesis_block; 
DROP TABLE IF EXISTS individual_block;
DROP TABLE IF EXISTS blockchain;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  amount FLOAT NOT NULL,
  status_of_request TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE single_transaction (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  loan_giver_id INTEGER NOT NULL,
  loan_reciever_username TEXT NOT NULL,
  request_post_id INTEGER NOT NULL,
  payment_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  loan_amount FLOAT NOT NULL,
  money_type TEXT NOT NULL,
  hashed_transac TEXT NOT NULL,
  FOREIGN KEY (loan_giver_id) REFERENCES user (id)
);

CREATE TABLE genesis_block (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  loan_giver_id INTEGER NOT NULL,
  loan_reciever_username TEXT NOT NULL,
  request_post_id INTEGER NOT NULL,
  payment_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  loan_amount FLOAT NOT NULL,
  money_type TEXT NOT NULL,
  hashed_transac TEXT NOT NULL
);

CREATE TABLE individual_block (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  hash1 TEXT,
  hash2 TEXT,
  prev_block_hash TEXT,
  filled_time FLOAT,
  chained_status TEXT, 
  no_in_block INTEGER NOT NULL
);

CREATE TABLE blockchain (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  block_id INTEGER NOT NULL,
  blocks_hash TEXT, 
  FOREIGN KEY (block_id) REFERENCES individual_block (id)
);
