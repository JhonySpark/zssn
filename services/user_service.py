from database.config import mysql

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

        return True
    except Exception as e:
        print('Error 20: ', e)
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
        return True
    except Exception as e:
        print('Error 35: ', e)
    finally:
        if(conn):
            cursor.close()
            conn.close()

# update survivor items
def set_survivor_items(item, survivorId):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = 'UPDATE inventory SET amount = %s WHERE survivor_id = %s AND item_id = %s'
        cursor.execute(query, (item['amount'], survivorId, item['id']))
        conn.commit()
        return True
    except Exception as e:
        print('Error 50: ', e)
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
        print('Error 65: ', e)
    finally:
        if(conn):
            cursor.close()
            conn.close()