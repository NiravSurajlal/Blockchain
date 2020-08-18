from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('info', __name__, url_prefix='/info')

@bp.route('/mypages')
@login_required
def mypages():
    """ Displays account transactions. """

    db = get_db()
    loans = db.execute(
        'SELECT l.id, loan_author_id, other_username, request_post_id, pay_time, username, loan_amount, money_type'
        ' FROM loan l JOIN user u ON l.loan_author_id = u.id'
        ' ORDER BY pay_time DESC'
    ).fetchall()

    loans_list = []
    for i in loans:
        if i['username'] == g.user['username']:
            loans_list.append(i)
        if i['other_username'] == g.user['username']:
            loans_list.append(i)    

    return render_template('blog/mypages.html', loans=loans_list)       

# search by id
# use if statment of id to say paid or recieved