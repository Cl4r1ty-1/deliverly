from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from deliverly.db import get_db, query_db
from datetime import date

bp = Blueprint('forms', __name__)

@bp.route('/')
def form_menu():
    return render_template('forms/index.html')

@bp.route('/submit/<form>')
def success(form):
    return render_template('forms/submit.html', form=form)

@bp.route('/new_customer', methods=["GET", "POST"])
def new_customer_form():
    if request.method == 'GET':
        return render_template("forms/customer.html")

    values = (request.form.get("first_name"), 
              request.form.get("last_name"), 
              request.form.get("email"), 
              request.form.get("address"),
              request.form.get("suburb"),
              request.form.get("postcode"),
              request.form.get("phone"))

    db = get_db()
    cu = db.cursor()
    cu.execute("INSERT INTO Customer(FirstName, LastName, CustomerEmail, CustomerAddress, Suburb, PostCode, CustomerPhone) VALUES (?, ?, ?, ?, ?, ?, ?)", values)
    db.commit()
    cu.close()
    print("New customer entry.")

    return redirect(url_for('forms.success', form="customer"))

@bp.route('/new_restaurant', methods=["GET", "POST"])
def new_restaurant_form():
    if request.method == "GET":
        return render_template('forms/restaurant.html')

    values = (request.form.get("restaurant_name"),
              request.form.get("address"),
              request.form.get("phone"))

    db = get_db()
    cu = db.cursor()
    cu.execute("INSERT INTO Restaurant(RestaurantName, RestaurantAddress, RestaurantPhone) VALUES (?, ?, ?)", values)
    db.commit()
    cu.close()
    print("New restaurant entry.")

    return redirect(url_for('forms.success', form="restaurant"))

@bp.route('/new_dish', methods=["GET", "POST"])
def new_dish_form():
    if request.method == "GET":
        headers, data = query_db("SELECT RestaurantID, RestaurantName FROM Restaurant")
        return render_template('forms/dish.html', restaurants=data)

    values = (request.form.get("restaurant_id"),
              request.form.get("dish_name"),
              request.form.get("dish_price"))

    db = get_db()
    cu = db.cursor()
    cu.execute("INSERT INTO Dish(RestaurantID, DishName, DishPrice) VALUES (?, ?, ?)", values)
    db.commit()
    cu.close()
    print("New dish entry.")

    return redirect(url_for('forms.success', form='dish'))

@bp.route('/get_dishes', methods=["POST"])
def get_dishes():
    try:
        restaurant = request.json['id']
        headers, dishes = query_db("SELECT DishID, DishName, DishPrice FROM Dish WHERE RestaurantID = ?", (restaurant,))
        return jsonify({"status":"success", "dishes":dishes})
    except Exception as e:
        return jsonify({"status":"fail", "error":str(e)})

@bp.route('/new_order', methods=["GET", "POST"])
def new_order_form():
    if request.method == 'GET':
        headers, customers = query_db("SELECT CustomerID, FirstName || ' ' || LastName AS Name FROM Customer")
        headers, restaurants = query_db("SELECT RestaurantID, RestaurantName FROM Restaurant")
        headers, dishs = query_db("SELECT DishID, DishName FROM Dish")

        return render_template('forms/order.html', 
                               customers=customers, 
                               restaurants=restaurants, 
                               dishs=dishs)

    customer_id = request.form.get("customer_id")
    restaurant_id = request.form.get("restaurant_id")
    dish_ids = request.form.getlist("dishs")

    items = []
    for dish_id in dish_ids:
        quantity = request.form.get(f"quantity_{dish_id}", type=int)
        items.append((int(dish_id), quantity))

    db = get_db()
    cu = db.cursor()

    cu.execute("""INSERT INTO Orders (CustomerID, RestaurantID, OrderDate)
                  VALUES (?, ?, ?)""", (customer_id, restaurant_id, date.today()))
    order_id = cu.lastrowid
    db.executemany("""INSERT INTO OrdersItems (OrderID, DishID, Quantity)
                      VALUES (?, ?, ?)""", [(order_id, dish_id, quantity) for dish_id, quantity in items])
    db.commit()
    cu.close()

    return redirect(url_for('forms.success', form='order'))    

@bp.route('/edit_entry/<table>/<id>', methods=["GET", "POST"])
def edit_entry(table, id):
    VALID_TABLES = {'Customer', 'Restaurant', 'Dish', 'Orders'}
    if table in VALID_TABLES:
        row_id = table.replace("s", "") if table.endswith('s') else table
        headers, data = query_db(f"SELECT * FROM {table} WHERE {row_id}ID = ?", (id,))
    
        if request.method == "GET":
                return render_template("forms/edit.html", headers=headers, data=data, table=table, id=id)

        for _ in range(len(headers)):
            if _ != 0:
                new_value = request.form.get(headers[_], None)
                if new_value != str(data[0][_]):
                    db = get_db()
                    db.execute(f"UPDATE {table} SET {headers[_]} = '{new_value}' WHERE {row_id}ID = ?", (id,))
                    db.commit()

        return redirect(url_for("forms.success", form='edit'))
    else:
        raise Exception("Not a valid table!")

@bp.errorhandler(Exception)
def form_error(e):
    return render_template('error/form.html', exception=str(e))