from hashlib import sha512
import json
from flaskr.db import get_db
import time

class SingleTransaction:
    def __init__(self, post_id, giver_of_loan, reciever_of_loan, loan_amount, transaction_time):
        """ Single transaction hasher. 'Data' from TABLE single_transaction and stroes hash in it. 
            :param post_id: unique 'post_id'
            :param giver_of_loan: 'username'
            :param reciever_of_loan: 'other_username' 
            :param loan_amount: 'loan_amount'
            :param transaction_time: 'pay_time' """

        self.post_id = post_id
        self.giver_of_loan = giver_of_loan
        self.reciever_of_loan = reciever_of_loan
        self.loan_amount = loan_amount
        self.transaction_time = transaction_time 
    
    def single_transaction_hasher(self):
        """ Returns hash of block after convertnig
            to JSON string """

        transaction_json_string = json.dumps(self.__dict__, sort_keys=True)
        return sha512(transaction_json_string.encode()).hexdigest()

def hash_transac_fxn():
    """ Callable fxn for hashing a transaction and storing it in the database. """

    db = get_db()
    transac = db.execute(
        'SELECT request_post_id, loan_giver_id, loan_reciever_username, loan_amount, id'
        ' FROM single_transaction'
        ' ORDER BY payment_time DESC'
    ).fetchall()

    transac_obj = SingleTransaction(transac[0][0], transac[0][1], transac[0][2], transac[0][3], time.time())
    hashed_transac = transac_obj.single_transaction_hasher()
    id_ = int(transac[0][4])
    # db.execute(
    #     'INSERT INTO transactions (hashed_transac, amnt, transaction_id)'
    #     ' VALUES (?, ?, ?)',
    #     (str(hashed_transac), float(transac[0][3]), transac[0][5])
    # )       
    # db.commit()

    db.execute(
        'UPDATE single_transaction SET hashed_transac = ?'
        ' WHERE id = ?',
        (str(hashed_transac), id_)
    )
    db.commit()

def genesis_block():
    """ Creates the gensis block for the blockchain. """

    db = get_db()
    db.execute(
        'INSERT INTO genesis_block (loan_giver_id, loan_reciever_username, request_post_id, payment_time, loan_amount, money_type, hashed_transac)'
        ' VALUES (?, ?, ?, ?, ?, ?, ?)',
        (0, 'MERCHANTREPUBLIC', 0, time.time(), 0, 'PAYMENT', 'UNHASHED')
    )
    db.commit()

    db = get_db()
    transac = db.execute(
        'SELECT request_post_id, loan_giver_id, loan_reciever_username, loan_amount, id'
        ' FROM genesis_block'
    ).fetchall()

    transac_obj = SingleTransaction(transac[0][0], transac[0][1], transac[0][2], transac[0][3], time.time())
    hashed_transac = transac_obj.single_transaction_hasher()
    id_ = 1

    db.execute(
        'UPDATE genesis_block SET hashed_transac = ?'
        ' WHERE id = ?',
        (str(hashed_transac), id_)
    )
    db.commit()
    

    # creates individual block from genesis
    # 0 for all other hashes supposed to be in block
    db = get_db()
    db.execute(
        'INSERT INTO individual_block (hash1, hash2, prev_block_hash, filled_time, chained_status, no_in_block)'
        ' VALUES (?, ?, ?, ?, ?, ?)',
        (hashed_transac, '0', '0', time.time(), 'UNCHAINED', 1)
    )
    db.commit()

    # add to the actual chain
    db = get_db()
    db.execute(
        'INSERT INTO blockchain (block_id, blocks_hash)'
        ' VALUES (?, ?)',
        (1, 'need_to_do')
    )
    db.commit()

    db.execute(
        'UPDATE individual_block SET chained_status = ?'
        ' WHERE id = ?',
        ('CHAINED', 1)
    )
    db.commit()
