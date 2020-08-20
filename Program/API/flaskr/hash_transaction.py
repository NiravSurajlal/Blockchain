from hashlib import sha512
import json

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
        return sha512(transaction_json_string.encode()).hexdigest

def ht_fxn(post_id, giver_of_loan, reciever_of_loan, loan_amount, transaction_time):
    transac_obj = SingleTransaction(post_id, giver_of_loan, reciever_of_loan, loan_amount, transaction_time)
    return transac_obj  