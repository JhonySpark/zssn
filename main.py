import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request

# function to create a new survivor
@app.route('/add_user', methods=['POST'])
def create_emp():
    try:        
        _json = request.json
    except Exception as e:
        print(e)   
     
# update survivor location on the system
@app.route('/update_user_location/<int:user_id>', methods=['PUT'])
def create_emp():
    try:        
        _json = request.json
    except Exception as e:
        print(e)   
      
# report infected survivor
@app.route('/set_infected_user/<int:user_id>', methods=['PUT'])
def create_emp():
    try:        
        _json = request.json
    except Exception as e:
        print(e)   
     
# update survivor inventory items
@app.route('/update_user_inventory/<int:user_id>', methods=['PUT'])
def create_emp():
    try:        
        _json = request.json
    except Exception as e:
        print(e)   
     
# function to trade items between survivors
@app.route('/trade', methods=['POST'])
def create_emp():
    try:        
        _json = request.json
    except Exception as e:
        print(e)   

# function to get system report
@app.route('/report', methods=['GET'])
def create_emp():
    try:        
        _json = request.json
    except Exception as e:
        print(e)  
        
# not found route      
@app.errorhandler(404)
def create_emp():
    try:        
        _json = request.json
    except Exception as e:
        print(e)   
     