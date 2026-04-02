from flask import Blueprint, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.faculty_service import create_faculty, get_all_faculties, get_faculty_by_id, delete_faculty

faculty_bp = Blueprint('faculty', __name__)

@faculty_bp.route('/create', methods=['POST'])
def create_faculty_endpoint():
    """
    Create a new faculty member
    Expected JSON payload:
    {
        "faculty_id": "string",
        "password": "string",
        "name": "string",
        "email": "string",
        "phone": "string (optional)",
        "department": "string (optional)",
        "designation": "string (optional)"
    }
    """
    try:
        # Get JSON data from request
        faculty_data = request.get_json()
        
        if not faculty_data:
            return jsonify({
                'success': False,
                'message': 'No JSON data provided'
            }), 400
        
        # Call service to create faculty
        result = create_faculty(faculty_data)
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@faculty_bp.route('/', methods=['GET'])
def get_all_faculties_endpoint():
    """
    Get all faculties
    """
    try:
        result = get_all_faculties()
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@faculty_bp.route('/<faculty_id>', methods=['GET'])
def get_faculty_endpoint(faculty_id):
    """
    Get faculty by ID
    """
    try:
        result = get_faculty_by_id(faculty_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@faculty_bp.route('/<faculty_id>', methods=['DELETE'])
def delete_faculty_endpoint(faculty_id):
    """
    Delete faculty by ID
    """
    try:
        result = delete_faculty(faculty_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500
