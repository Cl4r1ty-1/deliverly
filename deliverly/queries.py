from flask import Blueprint, render_template, request
from deliverly.db import query_db
from sqlite3 import OperationalError

QUERY_LIST = {
    "query_1":
    ("Retrieve a customer's orders",
        """SELECT Orders.OrderID, Orders.OrderDate, Restaurant.RestaurantName, Dish.DishName, Dish.DishPrice, OrdersItems.Quantity, (Dish.DishPrice*OrdersItems.Quantity) AS "Total ($)"
        FROM Orders
        INNER JOIN Restaurant ON Orders.RestaurantID = Restaurant.RestaurantID
        INNER JOIN Customer ON Orders.CustomerID = Customer.CustomerID
        INNER JOIN OrdersItems ON Orders.OrderID = OrdersItems.OrderID
        INNER JOIN Dish ON OrdersItems.DishID = Dish.DishID
        WHERE Customer.CustomerID = ?""",\
        True, "CustomerID"),
    "query_2":
    ("")
}

bp = Blueprint('queries', __name__)

@bp.route('/')
def query_menu():
    return render_template('queries/index.html', query_list=QUERY_LIST)

@bp.route('/<query>')
def render_query(query):
    if query in QUERY_LIST:
        query_to_run = QUERY_LIST[query]
        if query_to_run[2] == True:
            args = request.args.get('args', False, type=int)
            if args:
                headers, data = query_db(query_to_run[1], (args,))
                return render_template('queries/table.html', columns=headers, data=data, query_list=QUERY_LIST, query_name=query_to_run[0], argument=args)
            else:
                return render_template('error/query.html')
        else:
            headers, data = query_db(query_to_run[1], ())
            return render_template('queries/table.html', columns=headers, data=data, query_list=QUERY_LIST, query_name=query_to_run[0], argument="")
    else:
        return render_template('error/query.html')

@bp.errorhandler(OperationalError)
def query_error(e):
    return render_template('error/no_table.html')