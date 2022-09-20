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
@app.route('/update_user_location/<int:survivor_id>', methods=['PUT'])
def update_survivor_location(survivor_id):
    try:        
        _json = request.json
        set_survivor_location(_json, survivor_id)
        return jsonify({'message': 'Survivor location updated!'})   
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error updating survivor location!'})
      
# report infected survivor
@app.route('/report_infected/<int:survivor_id>', methods=['PUT'])
def report_infected_user(survivor_id):
    try:        
        report_infected_survivor(survivor_id)
        return jsonify({'message': 'Survivor reported as infected!'})
    except Exception as e:
        print(e)   
        return jsonify({'message': 'Error reporting survivor as infected!'})
     
# update survivor inventory items
@app.route('/update_user_inventory/<int:survivor_id>', methods=['PUT'])
def update_survivor_items(survivor_id):
    try:        
        _json = request.json
        done = set_survivor_items(_json, survivor_id)
        if(done):
            return jsonify({'message': 'Survivor inventory updated!'})
        else:
            return jsonify({'message': 'Survivor is infected, access denied!'})
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error updating survivor inventory!'})  
     
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