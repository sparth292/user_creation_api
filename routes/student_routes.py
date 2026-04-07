from flask import Blueprint, request, jsonify
from services.student_service import StudentService

student_bp = Blueprint('student', __name__)

@student_bp.route('/student/', methods=['GET'])
def get_all_students():
    """Get all students"""
    try:
        result = StudentService.get_all_students()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Internal server error: {str(e)}"
        }), 500

@student_bp.route('/student/create', methods=['POST'])
def create_student():
    """
    Create a new student
    Expected JSON payload:
    {
        "student_id": "string",
        "password": "string",
        "name": "string",
        "email": "string",
        "phone": "string",
        "date_of_birth": "YYYY-MM-DD",
        "address": "string",
        "department": "string",
        "year": "integer",
        "roll_number": "string",
        "sgpa": "float",
        "lab_batch": "string" (optional, values: C1, C2, C3)
        
    }
    """
    try:
        # Get JSON data from request
        student_data = request.get_json()
        
        if not student_data:
            return jsonify({
                "success": False,
                "message": "No data provided"
            }), 400
        
        # Validate required fields
        required_fields = ['student_id', 'password', 'name', 'email', 'department', 'year', 'roll_number']
        missing_fields = [field for field in required_fields if not student_data.get(field)]
        
        if missing_fields:
            return jsonify({
                "success": False,
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
        
        # Validate email format
        email = student_data.get('email')
        if '@' not in email or '.' not in email:
            return jsonify({
                "success": False,
                "message": "Invalid email format"
            }), 400
        
        # Validate year
        year = student_data.get('year')
        if isinstance(year, int):
            if year < 1 or year > 3:
                return jsonify({
                    "success": False,
                    "message": "Year must be between 1 and 3"
                }), 400
        elif isinstance(year, str):
            valid_years = ['FYCO', 'SYCO', 'TYCO']
            if year.upper() not in valid_years:
                return jsonify({
                    "success": False,
                    "message": f"Year must be one of: {', '.join(valid_years)}"
                }), 400
        else:
            return jsonify({
                "success": False,
                "message": "Year must be an integer (1-3) or enum string (FYCO, SYCO, TYCO)"
            }), 400
        
        # Validate SGPA if provided
        if 'sgpa' in student_data and student_data['sgpa'] is not None:
            try:
                sgpa = float(student_data['sgpa'])
                if sgpa < 0 or sgpa > 10:
                    return jsonify({
                        "success": False,
                        "message": "SGPA must be between 0 and 10"
                    }), 400
            except ValueError:
                return jsonify({
                    "success": False,
                    "message": "SGPA must be a valid number"
                }), 400
        
        # Validate lab_batch if provided
        if 'lab_batch' in student_data and student_data['lab_batch'] is not None:
            valid_lab_batches = ['C1', 'C2', 'C3']
            if student_data['lab_batch'] not in valid_lab_batches:
                return jsonify({
                    "success": False,
                    "message": f"lab_batch must be one of: {', '.join(valid_lab_batches)}"
                }), 400
        
        # Create student using service
        result = StudentService.create_student(student_data)
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Internal server error: {str(e)}"
        }), 500

@student_bp.route('/student/<student_id>', methods=['GET'])
def get_student(student_id):
    """Get student by ID"""
    try:
        result = StudentService.get_student_by_id(student_id)
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Internal server error: {str(e)}"
        }), 500

@student_bp.route('/student/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete student by ID"""
    try:
        result = StudentService.delete_student(student_id)
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Internal server error: {str(e)}"
        }), 500
