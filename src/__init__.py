import os
from flask import Flask, render_template, request
from flask_jsglue import JSGlue
from pathlib import Path

def create_app(test_config=None):
    global BASE_DIR
    # create the deliverly app
    jsglue = JSGlue()
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'records.db')
    )
    jsglue.init_app(app)

    if test_config is None:
        #prod config
        app.config.from_pyfile('config.py', silent=True)
    else:
        #test config
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    BASE_DIR = Path(app.root_path)

    @app.route("/")
    def home():
        return render_template("index.html")

    from . import db
    db.init_app(app)

    from . import tables
    app.register_blueprint(tables.bp)

    return app