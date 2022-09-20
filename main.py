from services.user_service import *
from app import app
from flask import jsonify
from flask import flash, request

@app.route('/')
def main():
    return "Welcome to the ZSSN Survivors API!"

# function to create a new survivor
@app.route('/add_user', methods=['POST'])
def create_survivor():
    try:        
        _json = request.json
        new_survivor(_json)   
        return jsonify({'message': 'Survivor added successfully!'})   
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error adding survivor!'})
     
# update survivor location on the system
@app.route('/update_user_location/<int:user_id>', methods=['PUT'])
def update_survivor_location():
    try:        
        _json = request.json
    except Exception as e:
        print(e)   
      
# report infected survivor
@app.route('/set_infected_user/<int:user_id>', methods=['PUT'])
def report_infected_survivor():
    try:        
        _json = request.json
    except Exception as e:
        print(e)   
     
# update survivor inventory items
@app.route('/update_user_inventory/<int:user_id>', methods=['PUT'])
def update_survivor_items():
    try:        
        _json = request.json
    except Exception as e:
        print(e)   
     
# function to trade items between survivors
@app.route('/trade', methods=['POST'])
def trade():
    try:        
        _json = request.json
    except Exception as e:
        print(e)   

# function to get system report
@app.route('/report', methods=['GET'])
def system_report():
    try:        
        _json = request.json
    except Exception as e:
        print(e)  
        
# not found route      
@app.errorhandler(404)
def not_found():
    try:        
        _json = request.json
    except Exception as e:
        print(e)   


app.run(host='localhost', port=5000)