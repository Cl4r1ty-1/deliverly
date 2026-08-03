from flask import Blueprint, render_template
from src.db import query_db

bp = Blueprint('tables', __name__, url_prefix='/tables')

@bp.route('/customers')
def customers():
    headers, data = query_db("SELECT * FROM Customer")

    return render_template('table.html', columns=headers, data=data)