-- ensure foreign key validation
PRAGMA foreign_keys = ON;

-- delete all data
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS OrdersItems;
DROP TABLE IF EXISTS Dish;
DROP TABLE IF EXISTS Restaurant;
DROP TABLE IF EXISTS Customer;
    
-- create new tables
CREATE TABLE Customer(
    CustomerID INTEGER PRIMARY KEY,
    FirstName TEXT NOT NULL CHECK(LENGTH(FirstName) <= 40),
    LastName TEXT NOT NULL CHECK(LENGTH(LastName) <= 40),
    CustomerEmail TEXT NOT NULL CHECK(CustomerEmail LIKE '%_@__%.__%'),
    CustomerAddress TEXT NOT NULL,
    Suburb TEXT NOT NULL,
    PostCode INTEGER NOT NULL CHECK(LENGTH(PostCode) = 4),
    CustomerPhone TEXT NOT NULL CHECK(CustomerPhone LIKE '(__) ________')
);
        
CREATE TABLE Restaurant(
    RestaurantID INTEGER PRIMARY KEY,
    RestaurantName TEXT NOT NULL,
    RestaurantAddress TEXT NOT NULL,
    RestaurantPhone TEXT NOT NULL CHECK(RestaurantPhone LIKE '(__) ________')
);

CREATE TABLE Dish(
    DishID INTEGER PRIMARY KEY,
    RestaurantID INTEGER NOT NULL,
    DishName TEXT NOT NULL,
    DishPrice REAL NOT NULL CHECK(DishPrice > 0),
    FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID) ON DELETE CASCADE
);

CREATE TABLE Orders(
    OrderID INTEGER PRIMARY KEY,
    CustomerID INTEGER NOT NULL,
    RestaurantID INTEGER NOT NULL,
    OrderDate DATE NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE,
    FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID)
);

CREATE TABLE OrdersItems(
    OrderID INTEGER NOT NULL,
    DishID INTEGER NOT NULL,
    Quantity INTEGER NOT NULL CHECK(Quantity > 0),
    PRIMARY KEY (OrderID, DishID),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE,
    FOREIGN KEY (DishID) REFERENCES Dish(DishID)
);