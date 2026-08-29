from flask import Blueprint, render_template
from deliverly.db import query_db
from sqlite3 import OperationalError

bp = Blueprint('tables', __name__, url_prefix='/tables')

@bp.route('/customers')
def customers():
    headers, data = query_db("SELECT * FROM Customer")

    return render_template('table.html', columns=headers, data=data, table="Customer")

@bp.route('/restaurants')
def restaurants():
    headers, data = query_db("SELECT * FROM Restaurant")

    return render_template('table.html', columns=headers, data=data, table="Restaurant")

@bp.errorhandler(OperationalError)
def no_table(e):
    return render_template('error/no_table.html')