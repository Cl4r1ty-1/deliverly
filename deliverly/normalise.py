import pandas as pd
from . import BASE_DIR

def normalise_csv():
    # read unnormalised data
    df = pd.read_csv(BASE_DIR.parent / "data.csv", dtype=str)

    # handle 1nf
    split = df.pop("CustomerName").str.split(' ', expand=True)
    df.insert(1, "FirstName", split[0])
    df.insert(2, "LastName", split[1])

    #2nf
    #extract customers
    customer_df = df[["FirstName", "LastName", "CustomerEmail", "CustomerAddress", "Suburb", "PostCode", "CustomerPhone"]].drop_duplicates().reset_index(drop=True)
    customer_df.index.name = "CustomerID"
    customer_df.reset_index(inplace=True)
    customer_df.CustomerID += 1 # id starts at 1 rather than 0

    #extract dish
    dish_df = df[["RestaurantName", "RestaurantAddress", "RestaurantPhone", "DishName", "DishPrice"]].drop_duplicates().reset_index(drop=True)
    dish_df.index.name = "DishID"
    dish_df.reset_index(inplace=True)
    dish_df.DishID += 1

    #3nf
    # extract restaurant
    restaurant_df = dish_df[["RestaurantName", "RestaurantAddress", "RestaurantPhone"]].drop_duplicates().reset_index(drop=True)
    restaurant_df.index.name = "RestaurantID"
    restaurant_df.reset_index(inplace=True)
    restaurant_df.RestaurantID += 1

    #merge dish + restaurant
    norm_dish_df = dish_df.merge(restaurant_df, on=["RestaurantName", "RestaurantAddress", "RestaurantPhone"])
    final_dish_df = norm_dish_df[["DishID", "RestaurantID", "DishName", "DishPrice"]]

    #merge all + orders
    norm_orders = df.merge(customer_df, on=["FirstName", "LastName", "CustomerEmail", "CustomerAddress", "Suburb", "PostCode", "CustomerPhone"])
    norm_orders = norm_orders.merge(restaurant_df, on=["RestaurantName", "RestaurantAddress", "RestaurantPhone"])
    norm_orders = norm_orders.merge(final_dish_df, on=["RestaurantID", "DishName", "DishPrice"]) # dish is dependant on which restaurant it comes from

    # remove all unnecessary fields
    norm_orders = norm_orders[["OrderID", "CustomerID", "RestaurantID", "OrderDate", "DishID", "Quantity"]]
    final_orders = norm_orders[["OrderID", "CustomerID", "RestaurantID", "OrderDate"]]

    # create assosiative entity for orders/items
    order_items = norm_orders[["OrderID", "DishID", "Quantity"]]

    # output csv files and their corresponding dataframes
    csv_names = [
        ("customer.csv", customer_df),
        ("restaurant.csv", restaurant_df),
        ("dish.csv", final_dish_df),
        ("orders.csv", final_orders),
        ("ordersitems.csv", order_items)
    ]

    # export final dataframes to csv files
    for tup in csv_names:
        tup[1].to_csv(BASE_DIR / "data" / tup[0], index=False, encoding='utf-8')

if __name__ == "__main__":
    normalise_csv()
