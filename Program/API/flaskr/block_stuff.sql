DROP TABLE IF EXISTS individual_block;
DROP TABLE IF EXISTS blockchain;
DROP TABLE IF EXISTS genesis_block; 

CREATE TABLE individual_block (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  hash1 TEXT,
  hash2 TEXT,
  prev_block_hash TEXT,
  filled_time FLOAT,
  chained_status TEXT, 
  no_in_block INTEGER NOT NULL,
);

CREATE TABLE blockchain (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  block_id INTEGER NOT NULL,
  blocks_hash TEXT, 
  FOREIGN KEY (block_id) REFERENCES individual_block (id)
);

CREATE TABLE genesis_block (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  loan_giver_id INTEGER NOT NULL,
  loan_reciever_username TEXT NOT NULL,
  request_post_id INTEGER NOT NULL,
  payment_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  loan_amount FLOAT NOT NULL,
  money_type TEXT NOT NULL,
  hashed_transac TEXT NOT NULL,
);


