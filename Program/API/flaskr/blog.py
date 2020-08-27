from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.hash_transaction import hash_transac_fxn 

import pdb

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    """ Index page for posts. """

    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username, amount, status_of_request'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
# login required auth decorator
@login_required
def create():
    """ Allows creation of post. Requires authentication to post. """

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        amount = request.form['amount']
        status_of_request = 'UNFILLED'
        error = None

        if not title:
            error = 'Title is required.'

        if not amount:
            error = 'Amount is required.'

        try:
            amount = float(amount)
        except ValueError:
            error = 'Invalid amount.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, amount, status_of_request, author_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, body, amount, status_of_request, g.user['id'])
            )
            # commit to DB            
            db.commit()
            # redirect back to index page            
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    """ Generic get post func. Eg. Update or Delete. """

    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username, amount, status_of_request'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

def get_post_no_check(id, check_author=True):
    """ Generic get post func without corresponding user ID. 
        Do not use for editing, only for viewing. 
        Returns one post in a list. """

    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username, amount, status_of_request'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    dum = [post]
    return dum 

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
# takes in a ID which corres to the <int:id> in the route, also see index.html
def update(id):
    """ Allows update of post. Requires authentication to post. """

    post = get_post(id)
    
    # prevents editing if already satisfied 
    availability = post['status_of_request']
    if availability == 'FILLED':
        return render_template('blog/unavailable.html')

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """ Allows deletion of post. Just a button in 'UPDATE'. """

    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

# incomplete
@bp.route('/<int:id>/payment', methods=('GET', 'POST'))
# @bp.route('/<int:id>/payment')
@login_required
def payment(id):
    """ Takes to page with one post and allows equal amount to be loaned. """

    posts = get_post_no_check(id)
    # username of postee
    other_username = posts[0]['username']
    # post number
    request_post_id = posts[0]['id']
    availability = posts[0]['status_of_request']

    if availability == 'FILLED':
        return render_template('blog/unavailable.html')

    if request.method == 'POST':
        if availability == 'UNFILLED':
            loan_amount = request.form['amount']
            money_type = 'PAYMENT'
            error = None    

            if not loan_amount:
                error = 'Amount is required.'
            # if amount != posts[0]['amount']:
            #     error = 'Amount incorrect.'

            try:
                loan_amount = float(loan_amount)
            except ValueError:
                error = 'Invalid amount.'

            if error is not None:
                flash(error)
            else:
                db = get_db()
                db.execute(
                    'INSERT INTO single_transaction (loan_amount, money_type, loan_reciever_username, request_post_id, loan_giver_id, hashed_transac)'
                    ' VALUES (?, ?, ?, ?, ?, ?)',
                    (loan_amount, money_type, other_username, request_post_id, g.user['id'], 'UNHASHED')
                )
                db.commit()
                
                # hashes single transac and adds to db
                hash_transac_fxn()
                
                # update status
                update_status(id)

                # redirect back to index page            
                return redirect(url_for('blog.index'))   
        else:
            return render_template('blog/unavailable.html')

    return render_template('blog/payment.html', posts=posts)               

def update_status(id):
    """ Updates status of post. Requires authentication to post. """
    
    s_dum = 'FILLED'
    db = get_db()
    db.execute(
        'UPDATE post SET status_of_request = ?'
        ' WHERE id = ?',
        (s_dum, id)
    )
    db.commit()



    


