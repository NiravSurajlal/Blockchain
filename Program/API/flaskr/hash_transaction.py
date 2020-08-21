from hashlib import sha512
import json
from flaskr.db import get_db
import time

class SingleTransaction:
    def __init__(self, post_id, giver_of_loan, reciever_of_loan, loan_amount, transaction_time):
        """ Single transaction hasher. 'Data' from TABLE LOAN. 
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

def ht_fxn():
    """ Callable fxn for hashing a transaction and storing it in the database. """

    db = get_db()
    transac = db.execute(
        'SELECT request_post_id, loan_author_id, other_username, loan_amount, pay_time'
        ' FROM loan'
        ' ORDER BY pay_time DESC'
    ).fetchall()

    transac_obj = SingleTransaction(transac[0][0], transac[0][1], transac[0][2], transac[0][3], time.time())
    hashed_transac = transac_obj.single_transaction_hasher()

    db.execute(
        'INSERT INTO transactions (hashed_transac, amnt)'
        ' VALUES (?, ?)',
        (str(hashed_transac), float(transac[0][3]))
    )       
    db.commit()