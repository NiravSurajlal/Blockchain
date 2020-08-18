import functools

from flask import ( Blueprint, flash, g, redirect, render_template, 
                    request, session, url_for )

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# BP name, where it is defined, prepended url prefix to all URLs associated with this BP
bp = Blueprint('auth', __name__, url_prefix='/auth')

# associates url with register view func.
# flask recieves request /auth/register, it will call register function  
# methods defines list of methods this view can handle 
@bp.route('/register', methods=('GET', 'POST'))
def register():
    """ Func used to register user. Checks if username
        is already in DB or adds it to DB. """
    # user submitted form
    if request.method =='POST':
        # dict mapping 
        username = request.form['username']
        password = request.form['password']
        # gets database
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        # checks against USERNAMES in DB
        # fetchone returns one row if username already in DB
        elif db.execute('SELECT id FROM user WHERE username = ?', 
        (username,)).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        # adds to DB if it can
        if error is None:
            db.execute('INSERT INTO user (username, password) VALUES (?, ?)',
                        (username, generate_password_hash(password)))
            # called to save changes to DB
            db.commit()
            return redirect(url_for('auth.login'))

        # stores error message so it can be displayed when rendering the template 
        flash(error)
        
    # returns the rendered template
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """ Checks if user exists in DB then checks hashed password. 
        Creates new session for user. """

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            # creates new session and stores user ID in it
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

# registers a func that runs before any view function
@bp.before_app_request
def load_logged_in_user():
    """ Checks if USER ID is stored in current session. """

    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()

@bp.route('/logout')
def logout():
    """ Removes USER ID from session. Will not be loaded in future requests. """

    session.clear()
    return redirect(url_for('index'))

# auth required for other views
def login_required(view):
    """ Decorator for view function to check if logged in. """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
        
    return wrapped_view
