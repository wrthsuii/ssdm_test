from flask import Blueprint, request, jsonify
from flasgger import swag_from
from datetime import datetime

rooms_bp = Blueprint('rooms', __name__, url_prefix='/api/v1/rooms')

# Mock data
rooms = []
room_id_counter = 1

# --- CREATE Room ---
@rooms_bp.route('/', methods=['POST'])
@swag_from({
    'tags': ['Room'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'roomType': {'type': 'string', 'enum': ['economy', 'standard', 'deluxe']},
                    'maxGuest': {'type': 'integer'},
                    'basePrice': {'type': 'number'},
                    'roomStatus': {'type': 'string', 'enum': ['available', 'occupied', 'maintenance']}
                },
                'required': ['roomType', 'maxGuest', 'basePrice', 'roomStatus']
            }
        }
    ],
    'responses': {
        201: {'description': 'Room created successfully'},
        400: {'description': 'Invalid input'}
    }
})
def create_room():
    global room_id_counter
    data = request.get_json()
    room = {
        'roomId': str(room_id_counter),
        'roomType': data['roomType'],
        'maxGuest': data['maxGuest'],
        'basePrice': data['basePrice'],
        'roomStatus': data.get('roomStatus', 'available'),
        'createdAt': datetime.utcnow().isoformat()
    }
    rooms.append(room)
    room_id_counter += 1
    return jsonify(room), 201

# --- READ all Rooms ---
@rooms_bp.route('/', methods=['GET'])
@swag_from({
    'tags': ['Room'],
    'responses': {
        200: {'description': 'List of all rooms'}
    }
})
def get_rooms():
    return jsonify(rooms), 200

# --- READ Room by ID ---
@rooms_bp.route('/<room_id>', methods=['GET'])
@swag_from({
    'tags': ['Room'],
    'parameters': [{'name': 'room_id', 'in': 'path', 'type': 'string', 'required': True}],
    'responses': {
        200: {'description': 'Room details'},
        404: {'description': 'Room not found'}
    }
})
def get_room(room_id):
    room = next((r for r in rooms if r['roomId'] == room_id), None)
    if not room:
        return jsonify({'message': 'Room not found'}), 404
    return jsonify(room), 200

# --- UPDATE Room ---
@rooms_bp.route('/<room_id>', methods=['PUT'])
@swag_from({
    'tags': ['Room'],
    'parameters': [
        {'name': 'room_id', 'in': 'path', 'type': 'string', 'required': True},
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'roomType': {'type': 'string', 'enum': ['economy', 'standard', 'deluxe']},
                    'maxGuest': {'type': 'integer'},
                    'basePrice': {'type': 'number'},
                    'roomStatus': {'type': 'string', 'enum': ['available', 'occupied', 'maintenance']}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Room updated successfully'},
        404: {'description': 'Room not found'}
    }
})
def update_room(room_id):
    room = next((r for r in rooms if r['roomId'] == room_id), None)
    if not room:
        return jsonify({'message': 'Room not found'}), 404
    data = request.get_json()
    room.update({k: v for k, v in data.items() if k in room})
    return jsonify(room), 200

# --- DELETE Room ---
@rooms_bp.route('/<room_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Room'],
    'parameters': [{'name': 'room_id', 'in': 'path', 'type': 'string', 'required': True}],
    'responses': {
        204: {'description': 'Room deleted successfully'},
        404: {'description': 'Room not found'}
    }
})
def delete_room(room_id):
    global rooms
    room = next((r for r in rooms if r['roomId'] == room_id), None)
    if not room:
        return jsonify({'message': 'Room not found'}), 404
    rooms = [r for r in rooms if r['roomId'] != room_id]
    return '', 204
