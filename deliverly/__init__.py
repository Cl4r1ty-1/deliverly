import os
from flask import Flask, render_template, request
from flask_jsglue import JSGlue
from pathlib import Path
import traceback

def create_app():
    global BASE_DIR
    # create the deliverly app
    jsglue = JSGlue()
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'records.db')
    )
    jsglue.init_app(app)

    os.makedirs(app.instance_path, exist_ok=True)

    BASE_DIR = Path(app.root_path)

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route('/admin')
    def admin_menu():
        return render_template("admin.html")

    @app.errorhandler(Exception)
    def unknown_error(e):
        print(traceback.format_exc())

        return render_template('error/unknown.html', exception=str(e), exception_type=type(e).__name__)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/404.html', exception=str(e))

    from . import db, tables, queries, forms
    db.init_app(app)
    app.register_blueprint(tables.bp)
    app.register_blueprint(queries.bp, url_prefix='/queries')
    app.register_blueprint(forms.bp)

    return app
