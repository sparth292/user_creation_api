from db import get_db_connection
from psycopg2.extras import RealDictCursor

class StudentService:
    @staticmethod
    def create_student(student_data):
        """
        Create a new student record in the database
        
        Args:
            student_data (dict): Dictionary containing student information
            
        Returns:
            dict: Created student record (without password)
        """
        try:
            # Get plain text password
            password = student_data.get('password')
            if not password:
                raise ValueError("Password is required")
            
            # Database connection
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Insert query
            insert_query = """
            INSERT INTO students (
                student_id, password_hash, name, email, phone, 
                date_of_birth, address, department, year, roll_number, sgpa, lab_batch
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            ) RETURNING student_id, name, email, phone, department, year, roll_number, sgpa, lab_batch
            """
            
            # Convert year to enum value if needed
            year_value = student_data.get('year')
            if isinstance(year_value, int):
                # If year is an integer, convert to string enum
                year_mapping = {1: 'FYCO', 2: 'SYCO', 3: 'TYCO'}
                year_value = year_mapping.get(year_value, str(year_value))
            
            values = (
                student_data.get('student_id'),
                password,  # Store plain text password
                student_data.get('name'),
                student_data.get('email'),
                student_data.get('phone'),
                student_data.get('date_of_birth'),
                student_data.get('address'),
                student_data.get('department'),
                year_value,  # Use enum value
                student_data.get('roll_number'),
                student_data.get('sgpa'),
                student_data.get('lab_batch')
            )
            
            cursor.execute(insert_query, values)
            result = cursor.fetchone()
            conn.commit()
            
            # Close connection
            cursor.close()
            conn.close()
            
            # Return created student data
            columns = ['student_id', 'name', 'email', 'phone', 'department', 'year', 'roll_number', 'sgpa', 'lab_batch']
            created_student = dict(zip(columns, result))
            
            return {
                "success": True,
                "message": "Student created successfully",
                "data": created_student
            }
            
        except Exception as e:
            if 'conn' in locals():
                conn.rollback()
                cursor.close()
                conn.close()
            
            error_message = str(e)
            if "duplicate key" in error_message.lower():
                return {
                    "success": False,
                    "message": "Student with this ID or email already exists"
                }
            else:
                return {
                    "success": False,
                    "message": f"Error creating student: {error_message}"
                }
    
    @staticmethod
    def get_all_students():
        """Get all students from database"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT student_id, name, email, phone, department, year, roll_number, sgpa, lab_batch
                FROM students 
                ORDER BY student_id
            """)
            
            students = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return {
                "success": True,
                "data": students,
                "count": len(students)
            }
            
        except Exception as e:
            if 'conn' in locals():
                cursor.close()
                conn.close()
            
            return {
                "success": False,
                "message": f"Error retrieving students: {str(e)}"
            }
    
    @staticmethod
    def get_student_by_id(student_id):
        """Get a specific student by ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT student_id, name, email, phone, department, year, roll_number, sgpa, lab_batch
                FROM students 
                WHERE student_id = %s
            """, (student_id,))
            
            student = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if not student:
                return {
                    "success": False,
                    "message": "Student not found"
                }
            
            return {
                "success": True,
                "data": student
            }
            
        except Exception as e:
            if 'conn' in locals():
                cursor.close()
                conn.close()
            
            return {
                "success": False,
                "message": f"Error retrieving student: {str(e)}"
            }
    
    @staticmethod
    def delete_student(student_id):
        """Delete a student by ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if student exists
            cursor.execute("SELECT student_id FROM students WHERE student_id = %s", (student_id,))
            if not cursor.fetchone():
                cursor.close()
                conn.close()
                return {
                    "success": False,
                    "message": "Student not found"
                }
            
            # Delete student
            cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return {
                "success": True,
                "message": "Student deleted successfully"
            }
            
        except Exception as e:
            if 'conn' in locals():
                conn.rollback()
                cursor.close()
                conn.close()
            
            return {
                "success": False,
                "message": f"Error deleting student: {str(e)}"
            }
