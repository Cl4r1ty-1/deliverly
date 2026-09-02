# deliverly

My Semester 2 Computer Science Database Project!

Database management system for a fictitious delivery company. Built with [Flask](https://flask.palletsprojects.com/en/stable/) and Bootstrap.

## Usage

Clone the repo

```bash
git clone https://github.com/Cl4r1ty-1/deliverly
cd deliverly
```

Create and activate your virtual environment
```bash
python3 -m venv venv
```
Windows (Powershell):
```powershell
.\venv\Scripts\Activate.ps1
```
Linux/macOS:
```bash
source venv/bin/activate
```

Install requirements
```bash
pip install -r requirements.txt
```

Run the app (locally)
```bash
flask --app ./deliverly run
```

In your browser go to
http://localhost:5000

## Project Layout

```bash
.
├── .github
│   └── workflows
│       └── deploy.yml # check out deliverly.cl4r1ty.dev (if i give you permission)
├── .gitignore
├── LICENSE
├── README.md
├── data.csv # original data we were provided
├── deliverly
│   ├── __init__.py
│   ├── data # normalised data ready for database
│   │   ├── customer.csv
│   │   ├── dish.csv
│   │   ├── orders.csv
│   │   ├── ordersitems.csv
│   │   └── restaurant.csv
│   ├── db.py # where you will find code to connect to and initalise database, including importing data
│   ├── forms.py # where you will find INSERT and UPDATE queries controllable by the user
│   ├── normalise.py # script to normalise data.csv, possibily irrelevant to the project
│   ├── queries.py # where you will find the list of queries, including required and custom queries
│   ├── schema.sql # sql script to initalise the blank database (CREATE TABLE, etc)
│   ├── static
│   │   ├── favicon.ico
│   │   ├── icon.png
│   │   ├── js # my horribe and sometimes forked javascript (we do have correct attribution tho)
│   │   │   ├── db_admin.js # mine
│   │   │   ├── form_validation.js # from bootstrap docs
│   │   │   ├── order_form.js # prob like 50% mine, 50% stack overflow. ignore the xss pls i did not have time to fix
│   │   │   └── query_menu.js # mine
│   │   └── reports # folder where exported reports go to before being sent to the user
│   │       └── .gitignore
│   ├── tables.py # nothing too interesting, just serves the user the raw data
│   └── templates # the entire frontend lol, written in html and jinja2
│       ├── admin.html
│       ├── base.html # the navbar and other things included on every page
│       ├── error # error pages
│       │   ├── 404.html
│       │   ├── base.html
│       │   ├── form.html
│       │   ├── no_table.html
│       │   ├── query.html
│       │   └── unknown.html
│       ├── forms # user forms
│       │   ├── customer.html
│       │   ├── dish.html
│       │   ├── edit.html
│       │   ├── order.html
│       │   ├── restaurant.html
│       │   └── submit.html
│       ├── index.html # home screen
│       ├── jsglue # ignore this
│       │   └── js_bridge.js # view justification for including it in the file itself
│       ├── queries # the query menu
│       │   ├── index.html
│       │   └── table.html
│       └── table.html # the raw data in a nice table format
└── requirements.txt # refer to usage

12 directories, 44 files

```


## License
MIT
