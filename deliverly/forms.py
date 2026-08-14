from flask import Blueprint, render_template, request, redirect, url_for
from deliverly.db import get_db

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
