from db import get_db_connection

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
                date_of_birth, address, department, year, roll_number, sgpa
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            ) RETURNING student_id, name, email, phone, department, year, roll_number, sgpa
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
                student_data.get('sgpa')
            )
            
            cursor.execute(insert_query, values)
            result = cursor.fetchone()
            conn.commit()
            
            # Close connection
            cursor.close()
            conn.close()
            
            # Return created student data
            columns = ['student_id', 'name', 'email', 'phone', 'department', 'year', 'roll_number', 'sgpa']
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
