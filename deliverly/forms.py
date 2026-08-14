from flask import Blueprint, render_template

bp = Blueprint('forms', __name__)

@bp.route('/')
def form_menu():
    pass

@bp.route('/new_customer')
def new_customer_form():
    return render_template("forms/customer.html")