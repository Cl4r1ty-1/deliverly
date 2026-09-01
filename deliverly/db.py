import sqlite3
import csv
from dateutil import parser
from flask import current_app, g, jsonify, Blueprint, redirect, url_for, request
import traceback
from . import BASE_DIR

bp = Blueprint('database', __name__, url_prefix='/db')

# init db connection based on the request (g)
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.execute("PRAGMA foreign_keys = ON") # this resets on every db connection, so we need to override it
    return g.db

# close connection to avoid mem leak
def close_db(exception=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# create blank tables based on given schema
def init_db():
    db = get_db()

    with current_app.open_resource(BASE_DIR / 'schema.sql') as file:
        script = file.read().decode('utf-8')
        db.executescript(script)
        db.commit()

# insert normalised csv data
def insert_real_data():
    db = get_db()
    cu = db.cursor()
    with open(BASE_DIR / "data" / "customer.csv", 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            cu.execute("INSERT INTO Customer (CustomerID, FirstName, LastName, CustomerEmail, CustomerAddress, Suburb, PostCode, CustomerPhone) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", row)

    with open(BASE_DIR / "data" / "restaurant.csv", 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            cu.execute("INSERT INTO Restaurant (RestaurantID, RestaurantName, RestaurantAddress, RestaurantPhone) VALUES (?, ?, ?, ?)", row)

    with open(BASE_DIR / "data" / "dish.csv", 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                cu.execute("INSERT INTO Dish (DishID, RestaurantID, DishName, DishPrice) VALUES (?, ?, ?, ?)", row)

    with open(BASE_DIR / "data" / "orders.csv", 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                row[3] = parser.parse(row[3]).date()
                cu.execute("INSERT INTO Orders (OrderID, CustomerID, RestaurantID, OrderDate) VALUES (?, ?, ?, ?)", row)

    with open(BASE_DIR / "data" / "ordersitems.csv", 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                cu.execute("INSERT INTO OrdersItems (OrderID, DishID, Quantity) VALUES (?, ?, ?)", row)
    db.commit()
    cu.close()

# generate test data
def insert_test_data():
     db = get_db()
     cu = db.cursor()

     CUSTOMERS = (
          (1, "Oliver", "Sykes", "oli@gmail.com", "7 Sempiternal Road", "East Perth", 6004, "(08) 92641843"),
          (2, "Sam", "Carter", "sam@gmail.com", "3 Sky Place", "Mandurah", 6210, "(08) 91235456"),
          (3, "William", "Ramos", "will@gmail.com", "89 Flame Avenue", "Secret Harbour", 6173, "(08) 96313521")
     )
     RESTAURANTS = (
          (1, "KFC", "1234 Marmion Avenue", "(08) 98343156"),
          (2, "Hungry Jack's", "1844 Marmion Avenue", "(08) 64043699"),
          (3, "McDonalds", "45 Ancourage Drive", "(08) 64329462")
     )
     DISHS = (
          (1, 1, "Bucket", 10.00),
          (2, 2, "Whopper", 12.00),
          (3, 3, "Big Mac", 7.00)
     )
     ORDERS = (
          (1, 1, 2, '2026-08-30'),
          (2, 2, 3, '2025-11-30'),
          (3, 3, 1, '2026-01-01')
     )
     ORDERSITEMS = (
          (1, 2, 3),
          (2, 3, 2),
          (3, 1, 1)
     )

     cu.executemany("INSERT INTO Customer (CustomerID, FirstName, LastName, CustomerEmail, CustomerAddress, Suburb, PostCode, CustomerPhone) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", CUSTOMERS)
     cu.executemany("INSERT INTO Restaurant (RestaurantID, RestaurantName, RestaurantAddress, RestaurantPhone) VALUES (?, ?, ?, ?)", RESTAURANTS)
     cu.executemany("INSERT INTO Dish (DishID, RestaurantID, DishName, DishPrice) VALUES (?, ?, ?, ?)", DISHS)
     cu.executemany("INSERT INTO Orders (OrderID, CustomerID, RestaurantID, OrderDate) VALUES (?, ?, ?, ?)", ORDERS)
     cu.executemany("INSERT INTO OrdersItems (OrderID, DishID, Quantity) VALUES (?, ?, ?)", ORDERSITEMS)
     db.commit()
     cu.close()

@bp.route('/blank', methods=["POST"])
def blank():
    print("Creating tables...")
    try:
        init_db()
        print("Tables created!")
        return jsonify({"status": "success", "message":"Empty tables created successfully!"})
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"status": "fail", "message":str(e)})

# these two function are used to insert either production data (from the original data.csv)
# or test data i define myself
@bp.route('/prod_data', methods=['POST'])
def prod_data():
     print("Inserting data...")
     try:
        insert_real_data()
        print("Data inserted")
        return jsonify({"status": "success", "message":"Production data entered successfully!"})
     except Exception as e:
          print(traceback.format_exc())
          return jsonify({"status": "fail", "message":str(e)})

@bp.route('/test_data', methods=['POST'])
def test_data():
     print("Inserting data...")
     try:
        insert_test_data()
        print("Data inserted (TEST)")
        return jsonify({"status": "success", "message":"Test data entered successfully!"})
     except Exception as e:
          print(traceback.format_exc())
          return jsonify({"status": "fail", "message":str(e)})


@bp.route('/delete/<table>/<id>', methods=["POST"])
def delete_entry(table, id):
     # i couldn't use parameters with this query, but the function checks if table
     # name is valid to prevent sql injection. it is secure i swear
     VALID_TABLES = {'Customer', 'Restaurant', 'Dish', 'Orders', 'OrdersItems'}
     if request.form.get("delete") == "delete" and table in VALID_TABLES:
        db = get_db()
        db.execute(f"DELETE FROM {table} WHERE {table.replace("s", "") if table.endswith('s') else table}ID = ?", (id,))
        db.commit()

        return redirect(url_for(f"tables.{table.lower()}"))
     else:
        raise Exception

# function for querying the db in the whole app
def query_db(query, args=(), one=False):
     cu = get_db().execute(query, args)
     data = cu.fetchall()
     headers = [desc[0] for desc in cu.description]
     cu.close()    
     return headers, (data[0] if data else None) if one else data


def init_app(app):
     app.teardown_appcontext(close_db) # this will close the connection when the app shuts down
     app.register_blueprint(bp)
