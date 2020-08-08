import os

from flask import Flask

def create_app(test_config=None):
    # creates and configures app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev', DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),)

    if test_config is None:
        # load instance of config when not testing (if it exits)
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load test config is passed in
        app.config.from_mapping(test_config)

    try:
        # creates instance folder for SQLite database because Flask does not create automatically
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # simple hello world page
    # creates connection between URL/hello abd a function which returns 'Hello World'
    @app.route('/hello')
    def hello():
        return 'Hello, World'
    
    return app
