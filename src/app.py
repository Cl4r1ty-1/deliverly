import sqlite3
import csv
from flask import Flask, render_template
import os

app = Flask(__name__)

cx = sqlite3.connect("records.db")
cu = cx.cursor()

def inital_db():
    #clear all db records
    cu.execute("DROP TABLE IF EXISTS Customer")
    cu.execute("DROP TABLE IF EXISTS Restaurant")
    cu.execute("DROP TABLE IF EXISTS Dish")
    cu.execute("DROP TABLE IF EXISTS Orders")
    cu.execute("DROP TABLE IF EXISTS OrdersItems")

    #create new tables
    cu.execute("""
        CREATE TABLE Customer(
            CustomerID INTEGER PRIMARY KEY,
            CustomerName TEXT NOT NULL,
            CustomerEmail TEXT NOT NULL,
            CustomerAddress TEXT NOT NULL,
            Suburb TEXT NOT NULL,
            PostCode INTEGER NOT NULL,
            CustomerPhone TEXT NOT NULL
        )
""")
    

@app.route("/")
def home_message():
    return "<h1>Welcome to Deliverly</h1>"

