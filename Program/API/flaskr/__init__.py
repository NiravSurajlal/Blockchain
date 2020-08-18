import os

from flask import Flask

def create_app(test_config=None):
    # create WSGI central obj, linked to relative path
    app = Flask(__name__, instance_relative_config=True)
    # config file -> set database path and folder and secret key
    app.config.from_mapping(SECRET_KEY='dev', DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),)

    #chooses dev vs test_config file for config
    if test_config is None:
        # uses config file when not testing
        # silent -> if missing file
        app.config.from_pyfile('config.py', silent=True)
    else:
        # uses testing config
        app.config.from_mapping(test_config)

    try:
        # make SQLite database folder if not existing
        os.makedirs(app.instance_path)
    except OSError:
        # (if it exists already)        
        pass
    
    # simple hello world page
    # creates connection between URL/hello abd a function which returns 'Hello World'
    @app.route('/hello')
    def hello():
        return 'Hello, World'
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)  

    from . import blog
    app.register_blueprint(blog.bp)
    # no URL prefix, thus, 'index' URL becomes /    
    app.add_url_rule('/', endpoint='index')

    from . import info 
    app.register_blueprint(info.bp) 
    
    return app
 