from hashlib import sha512
import json
from flaskr.db import get_db
import time

###### Brings in the hash, checks if block is full, if it is allows it to be mined, if successful adds it to chain
###### Both the individual blocks and chain are 2 SQL tables, individual_block & blockchain respectively 
###### They are related by 'block_id' in blockchain being tied to 'id' in individual_block  
###### func which takes in the hashes as a string and converts to list obj first 
###### prev block automatically started when old one ends 

class Block:

    def __init__(self, transactions, prev_hash, timestamp):
        """ Block constructor. """
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.timestamp = timestamp
        self.nonce = 0

    def compute_hash(self):
        """ Returns hash of block after convertnig
            to JSON string """
        block_json_str = json.dumps(self.__dict__, sort_keys=True)
        return sha512(block_json_str.encode()).hexdigest()    

class BlockChain:
    difficulty = 1 

    def __init__(self, top_of_chain_id, prev_hash, db):
        """ Block and Chain constructor.
            :param top_of_chain_id: id of the top chained block 
            :param prev_hash: hash of prev block 
            :param unconfirmed_transactions: current hashes in block 
            :param chained_status: status of block wrt chain, i.e. CHAINED or UNCHAINED 
            :param nonce: sets difficulty and prooves work has been done 
            :param db: loads current database. """

        self.top_of_chain_id = top_of_chain_id
        self.prev_hash = prev_hash
        self.unconfirmed_transactions = []
        self.chained_status = '' 
        self.filled_time = 0.0
        self.db = db
        self.load_block(db)
        self.block = Block(self.unconfirmed_transactions, self.prev_hash, self.filled_time)

    def load_block(self, db):
        """ Gets data of current block."""
        identity = self.top_of_chain_id + 1
        # db = get_db()
        current_block = db.execute(
            'SELECT hash1, chained_status, filled_time'
            ' FROM individual_block'
            ' WHERE id = ?',
            (identity,)
        ).fetchone()

        self.unconfirmed_transactions = json.loads(current_block[0])
        self.chained_status = current_block[1]
        self.filled_time = current_block[2]

    def proof_of_work(self):
        """ Tries diff values of nonce to get hash that satisfies criteria. """
        
        while not self.block.compute_hash().startswith('0' * self.difficulty):
            self.block.nonce += 1
            computed_hash = self.block.compute_hash()
        
        return computed_hash

    def add_block_to_chain(self, proof):
        """ Adds block to chain after verfication. verfication includes:
            * checking if proof or work is valid
            * check if prev_hash and hash of prev block in chain match """
        prev_hash_new_block = self.block.prev_hash

        if prev_hash_new_block != self.prev_hash:
            return False
        # compared with returned from 'proof_of_work'
        if not self.is_valid_proof(self.block, proof):
            return False

        # all checks out, add to chain
        # add stuff to update database
        self.block.hash = proof 

        return True

    def is_valid_proof(self, block, proof):
        """ Checks validty of block (work done) and if 
            it satisfies the difficulty."""
        return (proof.startswith('0' * self.difficulty) and
                proof == self.block.compute_hash())

    def mine(self):
        """ Mining process. If accepted, add to chain and update counter. """
        if len(self.unconfirmed_transactions) > 1:
            proof = self.proof_of_work()
            if not self.add_block_to_chain(proof):
                return False
            else:
                identity = self.top_of_chain_id + 1
                # db = get_db()
                self.db.execute(
                    'INSERT INTO blockchain (block_id, blocks_hash)'
                    ' VALUES (?, ?)',
                    (identity, self.block.hash)
                )
                self.db.commit()

                identity = self.top_of_chain_id + 1
                self.db.execute(
                    'UPDATE individual_block SET chained_status = ?, nonce = ?, prev_block_hash = ?'
                    ' WHERE id = ?',
                    ('CHAINED', self.block.nonce, self.prev_hash, identity)
                )
                self.db.commit()    
            return 'Mining successful. '  
        else:
            return 'Mining Unsuccessful. '      

    
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

    # if len(transactions_in_block) > 2 or blocks[0][2] != 'CHAINED':
    if len(transactions_in_block) > 1:
        next_block_intialisation(current_transaction_hash, db)
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

        if len(transactions_in_block) > 1:
            db.execute(
                'UPDATE individual_block SET filled_time = ?'
                ' WHERE id = ?',
                (time.time(), blocks[0][1])
            )
            db.commit()

def next_block_intialisation(transaction, db):
    """ Starts next block. """

    next_list = [transaction]
    json_next_list = json.dumps(next_list)
    # db = get_db()
    db.execute(
        'INSERT INTO individual_block (hash1, chained_status, nonce)'
        ' VALUES (?, ?, ?)',
        (json_next_list, 'UNCHAINED', 0)
    )
    db.commit()

def blockchain_init():
    """ Initialize mining operation. Returns the mining object
        inwhich the block obj is created. Allows the mining methods
        to be used on the created object. """
    
    db = get_db()
    blocks = db.execute(
        'SELECT block_id, blocks_hash'
        ' FROM blockchain'
        ' ORDER BY id DESC'
    ).fetchall()

    # top_of_chain_id = blocks[0][0]
    # top_of_chain_hash = blocks[0][1] 

    return BlockChain(blocks[0][0], blocks[0][1], db)



