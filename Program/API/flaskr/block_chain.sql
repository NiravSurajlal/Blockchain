DROP TABLE IF EXISTS individual_block;
DROP TABLE IF EXISTS blockchain;

CREATE TABLE individual_block(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    block_author_id  INTEGER NOT NULL,
    transac FLOAT NOT NULL,
    transac_time TEXT NOT NULL,
    prev_hash TEXT NOT NULL,
    nonce INTEGER NOT NULL, 
    chained_status TEXT NOT NULL,
    my_hash TEXT NOT NULL,
)

CREATE TABLE blockchain(

)