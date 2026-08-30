from flask import Blueprint, render_template
from deliverly.db import query_db
from sqlite3 import OperationalError

bp = Blueprint('tables', __name__, url_prefix='/tables')

@bp.route('/customers')
def customer():
    headers, data = query_db("SELECT * FROM Customer")

    return render_template('table.html', columns=headers, data=data, table="Customer")

@bp.route('/restaurants')
def restaurant():
    headers, data = query_db("SELECT * FROM Restaurant")

    return render_template('table.html', columns=headers, data=data, table="Restaurant")

@bp.route('/dishs')
def dish():
    headers, data = query_db("SELECT * FROM Dish")

    return render_template('table.html', columns=headers, data=data, table="Dish")

@bp.route('/orders')
def orders():
    headers, data = query_db("SELECT * FROM Orders")

    return render_template('table.html', columns=headers, data=data, table="Orders")

@bp.route('/ordersitems')
def ordersitems():
    headers, data = query_db("SELECT * FROM OrdersItems")

    return render_template('table.html', columns=headers, data=data, table="OrdersItems")

@bp.errorhandler(OperationalError)
def no_table(e):
    return render_template('error/no_table.html')
