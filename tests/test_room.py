import pytest
import json
from src import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# --- CREATE Room ---
def test_create_room(client):
    payload = {
        "roomType": "standard",
        "maxGuest": 2,
        "basePrice": 1000.0,
        "roomStatus": "available"
    }
    response = client.post('/api/v1/rooms/', data=json.dumps(payload),
                           content_type='application/json')
    assert response.status_code == 201
    data = response.get_json()
    assert data['roomType'] == "standard"
    assert data['maxGuest'] == 2
    assert data['basePrice'] == 1000.0
    assert data['roomStatus'] == "available"

# --- READ all Rooms ---
def test_get_rooms(client):
    response = client.get('/api/v1/rooms/')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

# --- READ Room by ID ---
def test_get_room_by_id(client):
    payload = {"roomType": "economy", "maxGuest": 1, "basePrice": 500.0, "roomStatus": "occupied"}
    post_resp = client.post('/api/v1/rooms/', data=json.dumps(payload),
                            content_type='application/json')
    room_id = post_resp.get_json()['roomId']

    # Тестуємо GET /rooms/<id>
    get_resp = client.get(f'/api/v1/rooms/{room_id}')
    assert get_resp.status_code == 200
    data = get_resp.get_json()
    assert data['roomId'] == room_id

# --- UPDATE Room ---
def test_update_room(client):
    payload = {"roomType": "deluxe", "maxGuest": 3, "basePrice": 1500.0, "roomStatus": "available"}
    post_resp = client.post('/api/v1/rooms/', data=json.dumps(payload),
                            content_type='application/json')
    room_id = post_resp.get_json()['roomId']

    update_payload = {"roomStatus": "occupied"}
    put_resp = client.put(f'/api/v1/rooms/{room_id}', data=json.dumps(update_payload),
                          content_type='application/json')
    assert put_resp.status_code == 200
    data = put_resp.get_json()
    assert data['roomStatus'] == "occupied"

# --- DELETE Room ---
def test_delete_room(client):
    payload = {"roomType": "standard", "maxGuest": 2, "basePrice": 1200.0, "roomStatus": "maintenance"}
    post_resp = client.post('/api/v1/rooms/', data=json.dumps(payload),
                            content_type='application/json')
    room_id = post_resp.get_json()['roomId']

    del_resp = client.delete(f'/api/v1/rooms/{room_id}')
    assert del_resp.status_code == 204

    get_resp = client.get(f'/api/v1/rooms/{room_id}')
    assert get_resp.status_code == 404