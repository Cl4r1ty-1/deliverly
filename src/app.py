import sqlite3
import csv
from flask import Flask, render_template
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)

cx = sqlite3.connect(BASE_DIR / "records.db")
cu = cx.cursor()
cu.execute("PRAGMA foreign_keys = ON")

def create_tables():
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
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
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
            OrderDate TEXT NOT NULL CHECK(OrderDate IS date(OrderDate)),
            FOREIGN KEY CustomerID REFERENCES Customer(CustomerID),
            FOREIGN KEY RestaurantID REFERENCES Restaurant(ResturantID)
        )
        """)

    # not sure what UnitPrice is for when we have DishPrice in the Dish table
    
    cu.execute("""
        CREATE TABLE OrdersItems(
            OrderID INTEGER NOT NULL,
            DishID INTEGER NOT NULL,
            Quantity INTEGER NOT NULL CHECK(Quantity > 0),
            PRIMARY KEY (OrderID, DishID),
            FOREIGN KEY OrderID REFERENCES Orders(OrderID),
            FOREIGN KEY DishID REFERENCES Dish(DishID)
        )
        """)
    cx.commit()

def insert_sample_data():
    pass

def insert_real_data():
    with open(BASE_DIR / "data" / "customer.csv", 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            cu.execute("INSERT INTO Customer (CustomerID, FirstName, LastName, CustomerEmail, CustomerAddress, Suburb, PostCode, CustomerPhone) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", row)

    with open(BASE_DIR / "data" / "restaurant.csv", 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            cu.execute("INSERT INTO Restaurant (RestaurantID, RestaurantName, RestaurantAddress, RestaurantPhone) VAULES (?, ?, ?, ?)", row)

    with open(BASE_DIR / "data" / "dish.csv", 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                cu.execute("INSERT INTO Dish (DishID, RestaurantID, DishName, DishPrice) VAULES (?, ?, ?, ?)", row)

    with open(BASE_DIR / "data" / "orders.csv", 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                cu.execute("INSERT INTO Orders (OrderID, CustomerID, RestaurantID, OrderDate) VAULES (?, ?, ?, ?)", row)

    with open(BASE_DIR / "data" / "ordersitems.csv", 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                cu.execute("INSERT INTO OrdersItems (OrderID, DishID, Quantity) VAULES (?, ?, ?)", row)
    cx.commit()

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
