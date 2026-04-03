from flask import Blueprint, request, jsonify
from services.timetable_service import TimetableService

timetable_bp = Blueprint('timetable', __name__)

@timetable_bp.route('/timetable', methods=['GET'])
def get_timetable():
    """
    Get timetables by batch
    Query parameter: batch (optional)
    Example: GET /timetable?batch=A1
    """
    try:
        batch = request.args.get('batch', '')
        result = TimetableService.get_timetable_by_batch(batch)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Internal server error: {str(e)}"
        }), 500
