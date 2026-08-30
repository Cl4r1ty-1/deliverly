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
│       └── deploy.yml
├── .gitignore
├── LICENSE
├── README.md
├── data.csv
├── deliverly
│   ├── __init__.py
│   ├── data
│   │   ├── customer.csv
│   │   ├── dish.csv
│   │   ├── orders.csv
│   │   ├── ordersitems.csv
│   │   └── restaurant.csv
│   ├── db.py
│   ├── forms.py
│   ├── normalise.py
│   ├── queries.py
│   ├── schema.sql
│   ├── static
│   │   ├── favicon.ico
│   │   ├── icon.png
│   │   ├── js
│   │   │   ├── db_admin.js
│   │   │   ├── form_validation.js
│   │   │   ├── order_form.js
│   │   │   └── query_menu.js
│   │   └── reports
│   │       └── .gitignore
│   ├── tables.py
│   └── templates
│       ├── admin.html
│       ├── base.html
│       ├── error
│       │   ├── 404.html
│       │   ├── base.html
│       │   ├── form.html
│       │   ├── no_table.html
│       │   ├── query.html
│       │   └── unknown.html
│       ├── forms
│       │   ├── customer.html
│       │   ├── dish.html
│       │   ├── order.html
│       │   ├── restaurant.html
│       │   └── submit.html
│       ├── index.html
│       ├── jsglue
│       │   └── js_bridge.js
│       ├── queries
│       │   ├── index.html
│       │   └── table.html
│       └── table.html
├── requirements.txt
└── update_layout.sh

12 directories, 44 files

```


## License
MIT
