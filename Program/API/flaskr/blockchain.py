from hashlib import sha512
import json
from flaskr.db import get_db
import time

###### Brings in the hash, checks if block is full, if it is allows it to be mined, if successful adds it to chain
###### Both the individual blocks and chain are 2 SQL tables, individual_block & blockchain respectively 
###### They are related by 'block_id' in blockchain being tied to 'id' in individual_block  
###### func which takes in the hashes as a string and converts to list obj first 
###### prev block automatically started when old one ends 

class BlockChaining:
    def __init__(self, top_of_chain_id, prev_hash):
        """ Block and Chain constructor.
            :param top_of_chain_id: id of the top chained block 
            :param prev_hash: hash of prev block 
            :param unconfirmed_transactions: current hashes in block 
            :param chained_status: status of block wrt chain, i.e. CHAINED or UNCHAINED. """
        self.top_of_chain_id = top_of_chain_id
        self.prev_hash = prev_hash
        self.unconfirmed_transactions = []
        self.chained_status = '' 

    def load_block(self):
        """ Gets data of current block."""
        identity = self.top_of_chain_id + 1
        db = get_db()
        current_block = db.execute(
            'SELECT hash1, chained_status'
            ' FROM individual_block'
            ' WHERE id = ?',
            (identity,)
        ).fetchone()

        self.unconfirmed_transactions = json.loads(current_block[0])
        self.chained_status = current_block[1]


    
def add_to_block(current_transaction_hash):
    """ Takes in hash of transaction and adds to a block 
        IF the block is not full. Stores fulfilled time. """
    db = get_db()

    blocks = db.execute(
        'SELECT hash1, id, chained_status '
        ' FROM individual_block'
        ' ORDER BY id DESC'
    ).fetchall()

    transactions_in_block = json.loads(blocks[0][0])

    # CHAINED does not work for genesis block 

    if len(transactions_in_block) > 2 or blocks[0][2] != 'CHAINED':
        next_block_intialisation()
    else: 
        # appending works 
        transactions_in_block.append(current_transaction_hash)
        json_transactions_in_block = json.dumps(transactions_in_block)

        db.execute(
            'UPDATE individual_block SET hash1 = ?, chained_status = ?'
            ' WHERE id = ?',
            (json_transactions_in_block, 'UNCHAINED', blocks[0][1])
        )
        db.commit()

def next_block_intialisation():
    """ Starts next block. """
    next_list = []
    json_next_list = json.dumps(next_list)
    db = get_db()
    db.execute(
        'INSERT INTO individual_block (hash1, chained_status)'
        ' VALUES (?, ?)',
        (json_next_list, 'UNCHAINED')
    )
    db.commit()


def blockchaining():
    """ Initialize mining operation. """
    
    db = get_db()
    blocks = db.execute(
        'SELECT block_id, blocks_hash'
        ' FROM blockchain'
        ' ORDER BY id DESC'
    ).fetchall()

    # top_of_chain_id = blocks[0][0]
    # top_of_chain_hash = blocks[0][1] 

    return BlockChaining(blocks[0][0], blocks[0][1])



