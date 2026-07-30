import sqlite3
import csv
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home_message():
    return "<h1>Welcome to Deliverly</h1>"

