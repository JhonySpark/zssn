from database.config import mysql
from flask import jsonify

# Service to add new survivor to database
def new_survivor(data):
    try:
        # new user query
        conn = mysql.connect()
        cursor = conn.cursor()
        query = 'INSERT INTO survivor (name, age, gender, location, infected) VALUES (%s, %s, %s, POINT(1, 1), %s)'
        cursor.execute(query, (data['name'], data['age'], data['gender'], '0'))   
        conn.commit()

        # set new user location
        set_survivor_location(data, cursor.lastrowid)
        
        # if user has items, add them to inventory
        if(data['items']):
            for item in data['items']:
                insert_survivor_item(item, cursor.lastrowid)

        return jsonify({'message': 'Survivor added successfully!'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error adding survivor!'}), 500
    finally:
        if(conn):
            cursor.close()
            conn.close()

# update survivor location
def set_survivor_location(data, survivorId):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = 'UPDATE survivor SET location = POINT(%s, %s) WHERE id = %s'
        cursor.execute(query, (data['latitude'], data['longitude'], survivorId))
        conn.commit()
        return jsonify({'message': 'Survivor location updated!'}), 200
    except Exception as e:
        print('Error: ', e)
        return jsonify({'message': 'Error updating survivor location!'}), 500
    finally:
        if(conn):
            cursor.close()
            conn.close()

# update survivor items
def set_survivor_items(item, survivorId):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        
         # check if item exists and get data
        survivor_query = 'SELECT * FROM survivor WHERE id = %s'
        cursor.execute(survivor_query, survivorId)
        survivor = cursor.fetchone()

        # check if survivor is infected
        if(survivor[5] >= 3):
            return jsonify({'message': 'Survivor is infected, access denied!'}), 400
        
        #update inventory item
        query = 'UPDATE inventory SET amount = %s WHERE survivor_id = %s AND item_id = %s'
        cursor.execute(query, (item['amount'], survivorId, item['id']))
        conn.commit()
        return jsonify({'message': 'Survivor inventory updated!'}), 200
    except Exception as e:
        print('Error: ', e)
        return jsonify({'message': 'Error updating survivor inventory!'}), 500
    finally:
        if(conn):
            cursor.close()
            conn.close()

# insert survivor new items
def insert_survivor_item(item, survivorId):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = 'REPLACE INTO inventory (survivor_id, item_id, amount) VALUES (%s, %s, %s)'
        cursor.execute(query, (survivorId, item['id'], item['amount']))
        conn.commit()
        return True
    except Exception as e:
        print('Error: ', e)
    finally:
        if(conn):
            cursor.close()
            conn.close()

# report infected survivor
def report_infected_survivor(survivorId):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = 'UPDATE survivor SET infected = infected + %s WHERE id = %s'
        cursor.execute(query, ('1', survivorId))
        conn.commit()
        return jsonify({'message': 'Survivor reported as infected!'}), 200
    except Exception as e:
        print('Error: ', e)
    finally:
        if(conn):
            cursor.close()
            conn.close()

# the trade function
def trade_service(data):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        # items in table to trade
        survivor1_item = data['survivor1_item']
        survivor2_item = data['survivor2_item']

        # get suvivor 1 data
        survivor1_query = 'SELECT * FROM survivor WHERE id = %s'
        cursor.execute(survivor1_query, data['survivor1_id'])
        survivor1 = cursor.fetchone()

        # get survivor 1 inventory
        survivor1_inventory_query = 'SELECT * FROM inventory INNER JOIN items ON inventory.item_id = items.id WHERE survivor_id = %s AND item_id = %s' 
        cursor.execute(survivor1_inventory_query, (data['survivor1_id'], survivor1_item['id']))
        survivor1_inventory_item = cursor.fetchone()

        # get suvivor 2 data
        survivor2_query = 'SELECT * FROM survivor WHERE id = %s'
        cursor.execute(survivor2_query, data['survivor2_id'])
        survivor2 = cursor.fetchone()

        # get survivor 2 inventory
        survivor2_inventory_query = 'SELECT * FROM inventory INNER JOIN items ON inventory.item_id = items.id WHERE survivor_id = %s AND item_id = %s'
        cursor.execute(survivor2_inventory_query, (data['survivor2_id'], survivor2_item['id']))
        survivor2_inventory_item = cursor.fetchone()
        
        # Check if there is infected survivors
        if(survivor1[5] >= 3 or survivor2[5] >= 3):
            return jsonify({'message': 'There is infected survivors in this trade'}), 400

        # Check if survivors have enough items to trade
        if(survivor1_inventory_item[2] < survivor1_item['amount']):
            return jsonify({'message': 'Survivor 1 dont have enough items to trade'}), 400

        if(survivor2_inventory_item[2] < survivor2_item['amount']):
            return jsonify({'message': 'Survivor 2 dont have enough items to trade'}), 400
        
        # Check if survivors have enough points to trade
        points_sum = int(survivor1_item['amount'] * survivor1_inventory_item[6]) + int(survivor2_item['amount'] * survivor2_inventory_item[6])
        if(points_sum % 2 > 0):
            return jsonify({'message': 'Trade items value mismatch, the trade must be fair!'}), 400

        # update survivor 1 inventory
        survivor1_inventory_query = 'UPDATE inventory SET amount = %s WHERE survivor_id = %s AND item_id = %s'
        cursor.execute(survivor1_inventory_query, (survivor1_inventory_item[2] - survivor1_item['amount'], data['survivor1_id'], survivor1_item['id']))

        # update survivor 2 inventory
        survivor2_inventory_query = 'UPDATE inventory SET amount = %s WHERE survivor_id = %s AND item_id = %s'
        cursor.execute(survivor2_inventory_query, (survivor2_inventory_item[2] - survivor2_item['amount'], data['survivor2_id'], survivor2_item['id']))

        # insert survivor 1 new item
        survivor1_new_item_query = 'UPDATE inventory SET amount = amount + %s WHERE survivor_id = %s AND item_id = %s'
        cursor.execute(survivor1_new_item_query, (survivor2_item['amount'], data['survivor1_id'], survivor2_item['id']))

        # insert survivor 2 new item
        survivor2_new_item_query = 'UPDATE inventory SET amount = amount + %s WHERE survivor_id = %s AND item_id = %s'
        cursor.execute(survivor2_new_item_query, (survivor1_item['amount'], data['survivor2_id'], survivor1_item['id']))

        conn.commit()
        return jsonify({'message': 'Trade completed'}), 200
    except Exception as e:
        print('Error: ', e)
        return jsonify({'message': 'Error: ' + str(e)}), 500
    finally:
        if(conn):
            cursor.close()
            conn.close()

# generate report
def report():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        # get total survivors
        total_survivors_query = 'SELECT COUNT(*) FROM survivor'
        cursor.execute(total_survivors_query)
        total_survivors = cursor.fetchone()

        # get total infected survivors
        total_infected_survivors_query = 'SELECT COUNT(*) FROM survivor WHERE infected >= 3'
        cursor.execute(total_infected_survivors_query)
        total_infected_survivors = cursor.fetchone()

        # get total non infected survivors
        total_non_infected_survivors_query = 'SELECT COUNT(*) FROM survivor WHERE infected < 3'
        cursor.execute(total_non_infected_survivors_query)
        total_non_infected_survivors = cursor.fetchone()

        # get average resources per survivor
        average_resources_per_survivor_query = 'SELECT AVG(amount) FROM inventory'
        cursor.execute(average_resources_per_survivor_query)
        average_resources_per_survivor = cursor.fetchone()

        # get average water per survivor
        average_water_per_survivor_query = 'SELECT AVG(amount) FROM inventory WHERE item_id = 1'
        cursor.execute(average_water_per_survivor_query)
        average_water_per_survivor = cursor.fetchone()

        # get average food per survivor
        average_food_per_survivor_query = 'SELECT AVG(amount) FROM inventory WHERE item_id = 2'
        cursor.execute(average_food_per_survivor_query)
        average_food_per_survivor = cursor.fetchone()

        # get average medicine per survivor
        average_medicine_per_survivor_query = 'SELECT AVG(amount) FROM inventory WHERE item_id = 3'
        cursor.execute(average_medicine_per_survivor_query)
        average_medicine_per_survivor = cursor.fetchone()

        # get average ammo per survivor
        average_ammo_per_survivor_query = 'SELECT AVG(amount) FROM inventory WHERE item_id = 4'
        cursor.execute(average_ammo_per_survivor_query)
        average_ammo_per_survivor = cursor.fetchone()

        # get points lost because of infected survivor
        points_lost_query = 'SELECT SUM(amount * items.value) FROM inventory INNER JOIN items ON inventory.item_id = items.id WHERE survivor_id IN (SELECT id FROM survivor WHERE infected >= 3)'
        cursor.execute(points_lost_query)
        points_lost = cursor.fetchone() or 0

        # percenta calculation
        def percent_calc(num_a, num_b):
            return int((num_a / num_b) * 100)

        # get report data
        report = {
            'total_survivors': total_survivors[0],
            'total_infected_survivors': f'{percent_calc(total_infected_survivors[0], total_survivors[0])}%',
            'total_non_infected_survivors': f'{percent_calc(total_non_infected_survivors[0], total_survivors[0])}%',
            'average_resources_per_survivor': ('%.2f' % average_resources_per_survivor[0]),
            'average_water_per_survivor': ('%.2f' % average_water_per_survivor[0]),
            'average_food_per_survivor': ('%.2f' % average_food_per_survivor[0]),
            'average_medicine_per_survivor': ('%.2f' % average_medicine_per_survivor[0]),
            'average_ammo_per_survivor': ('%.2f' % average_ammo_per_survivor[0]),
            'points_lost': int(points_lost[0])
        }

        return jsonify(report), 200
    except Exception as e:
        print('Error: ', e)
        return jsonify({'message': 'Error: ' + str(e)}), 500
    finally:
        if(conn):
            cursor.close()
            conn.close()