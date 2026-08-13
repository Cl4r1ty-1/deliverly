from flask import Blueprint, render_template, send_from_directory, request
import pandas as pd
from deliverly.db import query_db, get_db, BASE_DIR

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
            """SELECT Customer.CustomerID, Customer.FirstName, Customer.LastName, COUNT(Orders.OrderID) AS "Total Orders"
            FROM Orders
            INNER JOIN Customer ON Orders.CustomerID = Customer.CustomerID
            GROUP BY Customer.CustomerID
            HAVING "Total Orders" = 0""",
        False, ""),
    "query_6":
        ("List names of all dishes and the restaurants that serve them",
            """SELECT Dish.DishName, Restaurant.RestaurantName
            FROM Dish
            INNER JOIN Restaurant ON Dish.RestaurantID = Restaurant.RestaurantID
            ORDER BY Restaurant.RestaurantName ASC""",
        False, ""),
    "query_7": # there are multiple, thats ok leave without a LIMIT
        ("Show the most popular dish",
            """SELECT Dish.DishName, Restaurant.RestaurantName, COUNT(OrdersItems.DishID) AS "Total Ordered"
            FROM OrdersItems
            INNER JOIN Dish ON OrdersItems.DishID = Dish.DishID
            INNER JOIN Restaurant ON Dish.RestaurantID = Restaurant.RestaurantID
            GROUP BY Dish.DishID
            ORDER BY "Total Ordered" DESC""",
        False, ""),
    "query_8":
        ("Find the average dish price of each restaurant",
            """SELECT Restaurant.RestaurantName, ROUND(SUM(Dish.DishPrice)/COUNT(Dish.DishPrice), 2) AS "Average Price ($)"
            FROM Restaurant
            INNER JOIN Dish ON Restaurant.RestaurantID = Dish.RestaurantID
            GROUP BY Restaurant.RestaurantID""",
        False, ""),
    "query_9":
        ("List all orders with dishes and quantities",
            """SELECT Orders.OrderID, Orders.OrderDate, Customer.FirstName || ' ' || Customer.LastName AS 'Customer Name', Dish.DishName, OrdersItems.Quantity
            From Orders
            INNER JOIN Customer ON Orders.CustomerID = Customer.CustomerID
            INNER JOIN OrdersItems ON Orders.OrderID = OrdersItems.OrderID
            INNER JOIN Dish ON OrdersItems.DishID = Dish.DishID
            ORDER BY Orders.OrderID ASC""",
        False, ""),
    "query_10":
        ("Calculate Total Revenue of each Restaurant",
            """SELECT Restaurant.RestaurantName, SUM(Dish.DishPrice*OrdersItems.Quantity) AS "Total Revenue ($)"
            FROM Restaurant
            INNER JOIN Dish ON Dish.RestaurantID = Restaurant.RestaurantID
            INNER JOIN OrdersItems ON OrdersItems.DishID = Dish.DishID
            GROUP BY Restaurant.RestaurantID
            ORDER BY "Total Revenue ($)" DESC""",
        False, ""),
    "query_11":
        ("Show the customer's name and email",
            """SELECT FirstName || ' ' || LastName || ' ' || CustomerEmail AS CustomerContact
            FROM Customer
            WHERE CustomerID = ?""",
        True, "CustomerID"),
    "query_12":
        ("Show the total amount spent on each dish",
            """SELECT Dish.DishName, Restaurant.RestaurantName, Dish.DishPrice*SUM(OrdersItems.Quantity) AS CalculatedTotal
            FROM Dish
            INNER JOIN Restaurant ON Restaurant.RestaurantID = Dish.RestaurantID
            INNER JOIN OrdersItems ON OrdersItems.DishID = Dish.DishID
            GROUP BY Dish.DishID
            ORDER BY CalculatedTotal DESC""",
        False, "")
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
                return render_template('queries/table.html', 
                                       columns=headers, 
                                       data=data, 
                                       query_list=QUERY_LIST,
                                       query=query, 
                                       query_name=query_to_run[0], 
                                       argument=args)
            else:
                return render_template('error/query.html')
        else:
            headers, data = query_db(query_to_run[1], ())
            return render_template('queries/table.html', 
                                   columns=headers, 
                                   data=data, 
                                   query_list=QUERY_LIST, 
                                   query=query,
                                   query_name=query_to_run[0], 
                                   argument="")
    else:
        return render_template('error/query.html')

@bp.route('/<query>/report')
def download_report(query):
    args = request.args.get('args', None, type=int)
    if query in QUERY_LIST:
        query_to_run = QUERY_LIST[query]
        csv_path = BASE_DIR / "static" / "reports"
        csv_name = f"{query}_report_{args}.csv" if args else f"{query}_report.csv"
        df = pd.read_sql_query(query_to_run[1], get_db(), params=(args,) if args else ())
        df.to_csv(csv_path / csv_name, index=False, encoding='utf-8')
        return send_from_directory(csv_path, csv_name, as_attachment=True)
    else:
        raise Exception