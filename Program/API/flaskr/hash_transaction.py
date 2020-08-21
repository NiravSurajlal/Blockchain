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