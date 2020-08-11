Program and Application Outline

This program aims to allow loans between individuals where the transactions are all decentralized. 

The program will run like:
	Opening screen with login/register
		|_ Register allows person to make an unused username (email) and password then goes to login in screen
		|_ Login allows user to login
			|_ must see all requests for loans on the platform and allow selection
				|_ after selection, take to full page with company and loan outline
					|_ allow user to submit a payment to the requester's account
						|_ requester and loaner get emails with transaction details
		
__________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

File Scructure

Blockchain
	|_ Program
		|_ Instance
			|_ Database documents (files)
		|_ flaskr
			|_ templates
				|_ auth
					|_ register.html
					|_ login.html
				|_ transac
					|_ transaction.html
				|_ base.html
			|_ static
				|_  style.css
			|_ __init__.py
			|_ auth.py
				|_ import: 
				|_ def register()
				|_ def login()
				|_ def ld_lggd_in_usr()
				|_ def logout()
				|_ def login_required(view)
			|_ database.py
				|_ import:
				|_ def init_db()
				|_ def get_db()
				|_ def close_db(e=None)
				|_ def init_db_cmmd()
				|_ def init_app(app)
			|_ blocksc.py
				|_ import: 
					|_ from hashlib import sha256
					|_ json
					|_ time
				|_ class Block(index, transaction, timestamp, prev_hash)
					|_ def hasher()
				|_ class Blockchain
					|_ def genesis_block()
					|_ def last_block()
					|_ def add_block(block, proof)
					|_ def is_valid_proof(block, block_hash)
					|_ def proof_of_work(block)
					|_ def add_new_transaction(transaction)
					|_ def mine()
					|_ def test_hashes(current_bockchain)
					|_ def get_transac(curent_blockchain, searching_hash)
					
			|_ schema.sql
			
__________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________			
					
