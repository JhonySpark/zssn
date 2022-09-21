from flask import Flask
from flask_cors import CORS, cross_origin
from flaskext.mysql import MySQL

mysql = MySQL()

from routes import app_routes

def create_app():
    app = Flask(__name__)

    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
    app.config['MYSQL_DATABASE_DB'] = 'zssn_db'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    
    app_routes(app)
    mysql.init_app(app)

    return app

