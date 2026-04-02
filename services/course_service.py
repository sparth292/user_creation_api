from db import get_db_connection

class CourseService:
    
    @staticmethod
    def create_course(course_data):
        """
        Create a new course
        """
        try:
            # Validate required fields
            required_fields = ['course_code', 'course_name', 'department', 'batch', 'credits']
            for field in required_fields:
                if field not in course_data or not course_data[field]:
                    return {'error': f'Missing required field: {field}'}, 400
            
            # Validate batch enum
            valid_batches = ['FYCO', 'SYCO', 'TYCO']
            if course_data['batch'] not in valid_batches:
                return {'error': f'Batch must be one of: {", ".join(valid_batches)}'}, 400
            
            # Validate credits
            try:
                credits = int(course_data['credits'])
                if credits <= 0:
                    return {'error': 'Credits must be a positive integer'}, 400
            except ValueError:
                return {'error': 'Credits must be a valid integer'}, 400
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if course already exists
            cursor.execute("SELECT course_code FROM courses WHERE course_code = %s", 
                         (course_data['course_code'],))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return {'error': 'Course with this code already exists'}, 409
            
            # Insert course
            cursor.execute("""
                INSERT INTO courses (course_code, course_name, department, batch, credits)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING course_code, course_name, department, batch, credits
            """, (
                course_data['course_code'],
                course_data['course_name'],
                course_data['department'],
                course_data['batch'],
                credits
            ))
            
            result = cursor.fetchone()
            conn.commit()
            
            cursor.close()
            conn.close()
            
            course_dict = {
                'course_code': result[0],
                'course_name': result[1],
                'department': result[2],
                'batch': result[3],
                'credits': result[4]
            }
            
            return {'message': 'Course created successfully', 'course': course_dict}, 201
            
        except Exception as e:
            if 'conn' in locals():
                conn.rollback()
                cursor.close()
                conn.close()
            return {'error': 'Failed to create course', 'details': str(e)}, 500
    
    @staticmethod
    def get_all_courses():
        """
        Get all courses
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT course_code, course_name, department, batch, credits FROM courses ORDER BY course_code")
            results = cursor.fetchall()
            
            courses = []
            for row in results:
                course_dict = {
                    'course_code': row[0],
                    'course_name': row[1],
                    'department': row[2],
                    'batch': row[3],
                    'credits': row[4]
                }
                courses.append(course_dict)
            
            cursor.close()
            conn.close()
            
            return {'courses': courses}, 200
            
        except Exception as e:
            return {'error': 'Failed to retrieve courses', 'details': str(e)}, 500
    
    @staticmethod
    def get_course_by_code(course_code):
        """
        Get course by code
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT course_code, course_name, department, batch, credits FROM courses WHERE course_code = %s", (course_code,))
            result = cursor.fetchone()
            
            if not result:
                cursor.close()
                conn.close()
                return {'error': 'Course not found'}, 404
            
            course_dict = {
                'course_code': result[0],
                'course_name': result[1],
                'department': result[2],
                'batch': result[3],
                'credits': result[4]
            }
            
            cursor.close()
            conn.close()
            
            return {'course': course_dict}, 200
            
        except Exception as e:
            return {'error': 'Failed to retrieve course', 'details': str(e)}, 500
    
    @staticmethod
    def delete_course(course_code):
        """
        Delete course by code
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if course exists
            cursor.execute("SELECT course_code FROM courses WHERE course_code = %s", (course_code,))
            if not cursor.fetchone():
                cursor.close()
                conn.close()
                return {'error': 'Course not found'}, 404
            
            # Delete course
            cursor.execute("DELETE FROM courses WHERE course_code = %s", (course_code,))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return {'message': 'Course deleted successfully'}, 200
            
        except Exception as e:
            if 'conn' in locals():
                conn.rollback()
                cursor.close()
                conn.close()
            return {'error': 'Failed to delete course', 'details': str(e)}, 500
