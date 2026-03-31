from flask import Flask
from flask_cors import CORS
from routes.student_routes import student_bp
from routes.faculty_routes import faculty_bp

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(student_bp)
app.register_blueprint(faculty_bp, url_prefix='/api')

@app.route('/')
def home():
    return jsonify({
        "message": "Student Management API",
        "version": "1.0.0",
        "endpoints": {
            "create_student": "POST /student/create",
            "create_faculty": "POST /faculty/create"
        }
        
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)