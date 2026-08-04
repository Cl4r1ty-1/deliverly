from flask import Blueprint, render_template
from deliverly.db import query_db

bp = Blueprint('tables', __name__, url_prefix='/tables')

@bp.route('/customers')
def customers():
    headers, data = query_db("SELECT * FROM Customer")

    return render_template('table.html', columns=headers, data=data)

@bp.route('/restaurants')
def restaurants():
    headers, data = query_db("SELECT * FROM Restaurant")

    return render_template('table.html', columns=headers, data=data)