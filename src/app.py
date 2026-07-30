import sqlite3
import csv
from flask import Flask, render_template


app = Flask(__name__)

cx = sqlite3.connect("records.db")
cu = cx.cursor()
cu.execute("PRAGMA foreign_keys = ON")

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
    cu.execute("""
        CREATE TABLE Restaurant(
            RestaurantID INTEGER PRIMARY KEY,
            RestaurantName TEXT NOT NULL,
            RestaurantAddress TEXT NOT NULL,
            RestaurantPhone TEXT NOT NULL,
        )
        """)
    cu.execute("""
        CREATE TABLE Dish(
            DishID INTEGER PRIMARY KEY,
            RestaurantID INTEGER NOT NULL,
            DishName TEXT NOT NULL,
            DishPrice REAL NOT NULL CHECK(DishPrice > 0),
            FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID)
            )
            """)
    cu.execute("""
        CREATE TABLE Orders(
            OrderID INTEGER PRIMARY KEY,
            CustomerID INTEGER NOT NULL,
            RestaurantID INTEGER NOT NULL,
            OrderDate TEXT NOT NULL CHECK()
               """)
    

@app.route("/")
def render_table():
    with open("data.csv", "r") as file:
        data = csv.reader(file)
        header = next(data)
        rest = list(data)
        print(rest)

    return render_template("index.html", columns=header, data=rest)

if __name__ == "__main__":
    app.run(debug=True)
