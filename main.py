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
    _json = request.json
    return new_survivor(_json)        
     
# update survivor location on the system
@app.route('/update_user_location/<int:survivor_id>', methods=['PUT'])
def update_survivor_location(survivor_id):
    _json = request.json
    return set_survivor_location(_json, survivor_id)
           
# report infected survivor
@app.route('/report_infected/<int:survivor_id>', methods=['PUT'])
def report_infected_user(survivor_id):
    return report_infected_survivor(survivor_id)
     
# update survivor inventory items
@app.route('/update_user_inventory/<int:survivor_id>', methods=['PUT'])
def update_survivor_items(survivor_id):
    _json = request.json
    return set_survivor_items(_json, survivor_id)

# function to trade items between survivors
@app.route('/trade/', methods=['POST'])
def trade_controller():      
    _json = request.json
    return trade_service(_json)  
     
# function to get system report
@app.route('/report/', methods=['GET'])
def system_report():      
    return report()
     
# not found route      
@app.errorhandler(404)
def not_found():
    return jsonify({'message': 'Not found'}), 404  

app.run(host='localhost', port=5000)