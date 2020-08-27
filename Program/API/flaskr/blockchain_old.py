from hashlib import sha512
import json
import time
import pdb   # pdb.set_trace()

class Block:
    def __init__(self, index, transac, timestamp, prev_hash):
        """ Block constructor
            :param index: unique block ID = post id
            :param transac: transaction amount
            :param timestamp: Time generation of payment
            :param previous_hash: Previous block's hash of which this is a part off """
        self.index = index
        self.transac = transac
        self.timestamp = timestamp
        self.prev_hash = prev_hash
        self.nonce = 0

    def hasher(self):
        """ Returns hash of block after convertnig
            to JSON string """
        block_json_str = json.dumps(self.__dict__, sort_keys=True)
        return sha512(block_json_str.encode()).hexdigest()
    
class Blockchain:
    #Proof of work difficulty
    difficulty = 2
    
    def __init__(self):
        """ Blockchain constructor """
        self.unconfirmed_transactions = []
        self.chain = []
        self.genesis_block()
        
    def genesis_block(self):
        """ Generates the index 0 
        block and appends it to chain """
        gb = Block(0, [], time.time(), "0")            # Block obj
        gb.hash = gb.hasher()                          # Created Attribute
        self.chain.append(gb)
        
    @property
    def last_block(self):
        """ Retrieves last block & returns an object of class 'Block'.
            Will always have at least one (genesis) """
        return self.chain[-1]
        
    def add_block(self, block, proof):
        """ Func which adds block to chain after verification
            * Checks if proof is valid.
            * Checks if prev_hash of block matches latest block. """
        previous_hash = self.last_block.hash
        
        if previous_hash != block.prev_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        """ Check if block_hash is valid & satisfies difficulty """
        return (block_hash.startswith('0'*Blockchain.difficulty) and block_hash == block.hasher())

    def proof_of_work(self, block):
        """ Tries diff vals of nonce to get 
            hash that satisfies difficulty """
        block.nonce = 0 
        
        computed_hash = block.hasher()
        while not computed_hash.startswith('0'*Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.hasher()
        
        return computed_hash
    
    def add_new_transaction(self, transac):
        self.unconfirmed_transactions.append(transac)
    
    def mine(self):
        """ Interface to add pending transactions to 
            blockchain by adding to block and figuring
            proof of work """
        if not self.unconfirmed_transactions:
            return False
        # should add a loop here to iterate through each unconfirmed transaction? 
        # or maybe have groups of transactions? 
        new_block = Block(self.last_block.index+1, self.unconfirmed_transactions, time.time(), self.last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index

def test_hashes(current_blockchain):
    """ Func to test the hashes in the chain """
    for i in current_blockchain.chain:
        print(i.hash)
    return current_blockchain.chain[-1].hash

def get_transac(current_blockchain, searching_hash):
    """ Func to get block and its data back.
        Takes in a hash and returns the block on the chain. """
    for i in current_blockchain.chain:
        if i.hash == searching_hash:
            return i

def testing_function():
    """ Tests blockchain.
        : Adds transaction and mines it.
        : Adds to a block then to the chain (with genesis).
        : Returns the hashes and a timestamp of block.
        : Repeats a block with 3 transactions. """
        
    new = Blockchain()

    new.add_new_transaction(4000)
    new.mine()
    latest_block = test_hashes(new)

    block = get_transac(new, latest_block)

    print(block.transac)
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block.timestamp)))    

    new.add_new_transaction(4000)
    new.add_new_transaction(5000)
    new.add_new_transaction(6000)
    new.mine()
    latest_block = test_hashes(new)

    block = get_transac(new, latest_block)
    print(block.transac)
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block.timestamp)))