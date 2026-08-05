from flask import Blueprint, render_template, request
from deliverly.db import query_db

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
        ("Get a restaurant's menu",
            """SELECT DishName, DishPrice
                FROM Dish
                WHERE RestaurantID = ?""",
        True, "RestaurantID"),
    "query_3":
        ("Show total amount spent by each customer",
            """SELECT Customer.CustomerID, Customer.FirstName, Customer.LastName, SUM(Dish.DishPrice*OrdersItems.Quantity) AS "Total Spent ($)"
            FROM Orders
            INNER JOIN Customer ON Orders.CustomerID = Customer.CustomerID
            INNER JOIN OrdersItems ON Orders.OrderID = OrdersItems.OrderID
            INNER JOIN Dish ON OrdersItems.DishID = Dish.DishID
            GROUP BY Customer.CustomerID
            ORDER BY "Total Spent ($)" DESC""",
        False, ""),
    "query_4":
        ("Show number of orders placed by each customer",
            """SELECT Customer.CustomerID, Customer.FirstName, Customer.LastName, COUNT(Orders.OrderID) AS "Total Orders"
            FROM Orders
            INNER JOIN Customer ON Orders.CustomerID = Customer.CustomerID
            GROUP BY Customer.CustomerID
            ORDER BY Customer.CustomerID DESC""",
        False, ""),
    "query_5":  # yo what????
        ("Find customers who have never placed an order",
            """""",
        False, ""),
    "query_6":
        ("List names of all dishes and the restaurants that serve them",
            """SELECT Dish.DishName, Restaurant.RestaurantName
            FROM Dish
            INNER JOIN Restaurant ON Dish.RestaurantID = Restaurant.RestaurantID
            ORDER BY Restaurant.RestaurantName ASC""",
        False, ""),
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

