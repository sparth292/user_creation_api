from flask import Blueprint, request, jsonify
from services.course_service import CourseService

courses_bp = Blueprint('courses', __name__, url_prefix='/courses')

@courses_bp.route('/create', methods=['POST'])
def create_course():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    result, status_code = CourseService.create_course(data)
    return jsonify(result), status_code

@courses_bp.route('/', methods=['GET'])
def get_all_courses():
    result, status_code = CourseService.get_all_courses()
    return jsonify(result), status_code

@courses_bp.route('/<course_code>', methods=['GET'])
def get_course(course_code):
    result, status_code = CourseService.get_course_by_code(course_code)
    return jsonify(result), status_code

@courses_bp.route('/<course_code>', methods=['DELETE'])
def delete_course(course_code):
    result, status_code = CourseService.delete_course(course_code)
    return jsonify(result), status_code