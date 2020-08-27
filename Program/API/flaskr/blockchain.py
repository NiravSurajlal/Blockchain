from hashlib import sha512
import json
from flaskr.db import get_db
import time

###### Brings in the hash, checks if block is full, if it is allows it to be mined, if successful adds it to chain
###### Both the individual blocks and chain are 2 SQL tables, individual_block & blockchain respectively 
###### They are related by 'block_id' in blockchain being tied to 'id' in individual_block  

def add_to_block():
    """ Takes in hash of transaction and adds to a block 
        IF the block is not full. Stores fulfilled time. """
    db = get_db()
    db.execute(
        'INSERT INTO individual_block (title, body, amount, status_of_request, author_id)'
        ' VALUES (?, ?, ?, ?, ?)',
        (title, body, amount, status_of_request, g.user['id'])
    )
    # commit to DB            
    db.commit()


def check_if_full():
    """ Checks if number of transaction in block is full. """
    pass

def time_completed():
    """ Gets time the block if competely full. """
    pass 

def blocks_counter():
    pass 