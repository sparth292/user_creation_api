from flask import Blueprint, request, jsonify
from services.rooms_service import RoomService

rooms_bp = Blueprint('rooms', __name__)

@rooms_bp.route('/rooms/create', methods=['POST'])
def create_room():
    data = request.get_json()
    result, status_code = RoomService.create_room(data)
    return jsonify(result), status_code

@rooms_bp.route('/rooms/', methods=['GET'])
def get_all_rooms():
    result, status_code = RoomService.get_all_rooms()
    return jsonify(result), status_code

@rooms_bp.route('/rooms/<room_id>', methods=['GET'])
def get_room(room_id):
    result, status_code = RoomService.get_room_by_id(room_id)
    return jsonify(result), status_code

@rooms_bp.route('/rooms/<room_id>', methods=['DELETE'])
def delete_room(room_id):
    result, status_code = RoomService.delete_room(room_id)
    return jsonify(result), status_code
