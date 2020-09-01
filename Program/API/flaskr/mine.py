from flask import ( Blueprint, flash, g, redirect, render_template, 
                    request, session, url_for )
from flaskr.db import get_db                    
from flaskr.auth import login_required
from flaskr.blockchain import blockchain_init

bp = Blueprint('mine', __name__, url_prefix='/mine')

@bp.route('/check_count')
def check_count():
    """ Displays the current number of blocks and the current
        highest in chain."""

    block_no, block_chain_no = block_data()

    return render_template('mine/check_count.html', block_no = block_no, block_chain_no = block_chain_no)

def block_data():
    """ Checks the block and blockchain top numbers."""
    db = get_db()
    blocks = db.execute(
        'SELECT id'
        ' FROM individual_block'
        ' ORDER BY id DESC'
    ).fetchall()

    block_chains = db.execute(
        'SELECT id'
        ' FROM blockchain'
        ' ORDER BY id DESC'
    ).fetchall()

    return blocks[0][0], block_chains[0][0]     

@bp.route('/run_operation')
@login_required
def run_operation():
    """ Allows a mining operation to start and addition to chain."""
    block_no, block_chain_no = block_data()
    if block_no > block_chain_no:
        # returns Blockchain class with Block class 
        block_operation = blockchain_init()
        status = block_operation.mine()
        return render_template('mine/run_operation.html', status = status)
    else:
        return render_template('blog/unavailable.html')


