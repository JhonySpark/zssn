import os
from flask import Flask
from flask_cors import CORS, cross_origin
from flaskext.mysql import MySQL

mysql = MySQL()

prod = False
if os.environ.get('ENV') is not None:
    if os.environ['ENV'] == 'prod': prod = True

def create_app():
    app = Flask(__name__)

    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
    app.config['MYSQL_DATABASE_DB'] = 'zssn_db' 
    app.config['MYSQL_DATABASE_HOST'] = 'mysql_db' if prod else 'localhost'

    mysql.init_app(app)
    
    from routes import app_routes
    app_routes(app)

    return app

