import os 

from flask import Flask

def create_app(test_config=None):
    # Create and config an app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite")
    )

    # allow custom configs, testing and otherwise
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    # ensure instance path exists
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    #Create a route
    @app.route('/hello')
    def hello():
        return "Hello world!"

    # attach appropriate db funtions to app upon creation
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app