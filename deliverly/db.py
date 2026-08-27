import sqlite3
import csv
from dateutil import parser
from flask import current_app, g, jsonify, Blueprint
import traceback
from . import BASE_DIR

bp = Blueprint('database', __name__, url_prefix='/db')

# init db connection based on the request (g)
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)

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

# note: make this 'insert data' use AJAX to make a drop down with test or prod data :)
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
