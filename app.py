from flask import Flask, jsonify
from flask_cors import CORS
from routes.student_routes import student_bp
from routes.faculty_routes import faculty_bp
from routes.courses_root import courses_bp

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(student_bp)
app.register_blueprint(faculty_bp, url_prefix='/api')
app.register_blueprint(courses_bp)

@app.route('/')
def home():
    return jsonify({
        "message": "Student Management API",
        "version": "1.0.0",
        "endpoints": {
            "students": {
                "create_student": "POST /student/create",
                "get_all_students": "GET /student/",
                "get_student": "GET /student/<student_id>",
                "delete_student": "DELETE /student/<student_id>"
            },
            "faculty": {
                "create_faculty": "POST /api/faculty/create",
                "get_all_faculties": "GET /api/faculty/",
                "get_faculty": "GET /api/faculty/<faculty_id>",
                "delete_faculty": "DELETE /api/faculty/<faculty_id>"
            },
            "courses": {
                "create_course": "POST /courses/create",
                "get_all_courses": "GET /courses/",
                "get_course": "GET /courses/<course_code>",
                "delete_course": "DELETE /courses/<course_code>"
            }
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)