from app import create_app
import pytest

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

# create multiple users
def create_multiple_users(client):
    for i in range(1, 3):
        client.post('/add_user', json={
            "name": f'John Doe {i}',
            "age": "25",
            "gender": "M",
            "latitude": "40.7128",
            "longitude": "-74.0060",
            "items": [{
                "id": 1,
                "amount": 10
            },{
                "id": 2,
                "amount": 10
            },{
                "id": 3,
                "amount": 10
            },{
                "id": 4,
                "amount": 10
            }]
        })

# test server status
def test_server_status(client):
    response = client.get('/')
    assert response.status_code == 200

# test for create mew survivor
def test_add_user(client):
    response = client.post('/add_user', json={
        "name": "John Doe",
        "age": "25",
        "gender": "M",
        "latitude": "40.7128",
        "longitude": "-74.0060",
        "items": [{
            "id": 1,
            "amount": 10
        },{
            "id": 2,
            "amount": 10
        },{
            "id": 3,
            "amount": 10
        },{
            "id": 4,
            "amount": 10
        }]
    })
    
    assert response.status_code == 200

# test for create mew survivor with invalid json
def test_add_user_fail_500(client):
    response = client.post('/add_user', json={
        "age": "25",
        "gender": "M",
        "latitude": "40.7128",
        "longitude": "-74.0060",
        "items": [{
            "id": 1,
            "amount": 10
        },{
            "id": 2,
            "amount": 10
        },{
            "id": 3,
            "amount": 10
        },{
            "id": 4,
            "amount": 10
        }]
    })

    assert response.status_code == 500

# test for update survivor location
def test_update_survivor_location_200(client):
    response = client.put('/update_user_location/1', json={
        "latitude": "40.7128",
        "longitude": "-74.0060"
    })

    assert response.status_code == 200

# test for update survivor location with invalid json
def test_update_survivor_location_fail_505(client):
    response = client.put('/update_user_location/1', json={
        "longitude": "-74.0060"
    })

    assert response.status_code == 500

# test for update survivor location with not survivor found
def test_update_survivor_location_fail_404(client):
    response = client.put('/update_user_location/56598', json={
        "latitude": "40.7128",
        "longitude": "-74.0060"
    })

    assert response.status_code == 404

# test for report survivor infected
def test_report_infected_200(client):
    response = client.put('/report_infected/1')

    assert response.status_code == 200

# test for not found survivor
def test_report_infected_fail_404(client):
    response = client.put('/report_infected/65689')

    assert response.status_code == 404

# test  for update survivor inventory items with infected survivor
def test_set_survivor_items_400(client):
    for i in range(1, 3):
        client.put('/report_infected/1')

    response = client.put('/update_user_inventory/1', json={
        "id": 2,
        "amount": 1
    })

    assert response.data == b'{"message":"Survivor is infected, access denied!"}\n'
    assert response.status_code == 400

# test fro  manage survivor inventory
def test_set_survivor_items_200(client):
    create_multiple_users(client)
    response = client.put('/update_user_inventory/3', json={
        "id": 2,
        "amount": 1
    })

    assert response.status_code == 200

# test for manage survivor inventory with not found survivor
def test_set_survivor_items_404(client):
    create_multiple_users(client)
    response = client.put('/update_user_inventory/95959', json={
        "id": 2,
        "amount": 1
    })

    assert response.status_code == 404

# test for trade between survivors
def test_trade_function_200(client):
    create_multiple_users(client)
    response = client.post('/trade', json={
        "survivor1_id": 2,
        "survivor1_item":{
            "id": 1,
            "amount": 1
        },
        "survivor2_id": 3,
        "survivor2_item":{
            "id": 1,
            "amount": 1
        }
    })

    assert response.data == b'{"message":"Trade completed"}\n'
    assert response.status_code == 200

# test for trade between survivors with an infected one
def test_trade_function_with_infected_400(client):   
    response = client.post('/trade', json={
        "survivor1_id": 1,
        "survivor1_item":{
            "id": 4,
            "amount": 3
        },
        "survivor2_id": 3,
        "survivor2_item":{
            "id": 2,
            "amount": 1
        }
    })
    assert response.data == b'{"message":"There is infected survivors in this trade"}\n'
    assert response.status_code == 400

# test for trade between survivors with not enougth item to trade
def test_trade_function_not_enougth_item_400(client):
    response = client.post('/trade', json={
        "survivor1_id": 2,
        "survivor1_item":{
            "id": 4,
            "amount": 3
        },
        "survivor2_id": 3,
        "survivor2_item":{
            "id": 1,
            "amount": 50
        }
    })

    assert response.status_code == 400

# test for trade between survivors with not balanced item values
def test_trade_function_not_enougth_points_400(client):
    response = client.post('/trade', json={
        "survivor1_id": 2,
        "survivor1_item":{
            "id": 1,
            "amount": 2
        },
        "survivor2_id": 3,
        "survivor2_item":{
            "id": 4,
            "amount": 1
        }
    })
    assert response.data == b'{"message":"Trade items value mismatch, the trade must be fair!"}\n'
    assert response.status_code == 400