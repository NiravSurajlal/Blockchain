import sqlite3
import click

# g (proxy) is a namespace obj were elements are stored
# current_app is a proxy for the app handling the current request (easier to use than importing app)
from flask import current_app, g      
# command line interface 
# guarantees execution with script's app context
from flask.cli import with_appcontext

def get_db():
    """ Establishes connection to database, database
        path given in config file. """

    # g returns as g.__dict__ 
    if 'db' not in g:
        # create new connection obj which represents database
            # est connection to file pointed to by DATABASE conf key
        g.db = sqlite3.connect(current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        # tells connection to return rows that behave like dicts
        g.db.row_factory =sqlite3.Row

        return g.db

def close_db(e=None):
    """ Checks if there is a connection. 
        Closes it. Called after each request. """

    # pop and default error if DNE
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """ Est then initialises sql db of tables and columns. """

    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        # executes sqlLite 
        db.executescript(f.read().decode('utf8'))

#defines command line command
@click.command('init-db')
@with_appcontext
def init_db_command():
    """ Clear existing db and create new tables """
    init_db()
    click.echo('Initialized the Database.')

def init_app(app):
    """ Register functions with app instance. """
    # tear downs indicates connection shutdown function & wraps
    app.teardown_appcontext(close_db)
    # adds new CLI command useable with command flask 
    app.cli.add_command(init_db_command)
