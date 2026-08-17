from flask import Blueprint, render_template, request, redirect, url_for
from deliverly.db import get_db, query_db

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
    

@bp.errorhandler(Exception)
def form_error(e):
    return render_template('error/form.html')