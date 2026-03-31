import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import get_db_connection

def create_faculty(faculty_data):
    """
    Create a new faculty record in the database
    
    Args:
        faculty_data (dict): Dictionary containing faculty information
            - faculty_id (str): Required
            - password (str): Required (plain text as requested)
            - name (str): Required
            - email (str): Required
            - phone (str): Optional
            - department (str): Optional
            - designation (str): Optional
    
    Returns:
        dict: Result of the operation with success status and message
    """
    try:
        # Validate required fields
        required_fields = ['faculty_id', 'password', 'name', 'email']
        for field in required_fields:
            if field not in faculty_data or not faculty_data[field]:
                return {
                    'success': False,
                    'message': f'Missing required field: {field}'
                }
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if faculty_id already exists
        cursor.execute("SELECT faculty_id FROM faculty WHERE faculty_id = %s", 
                      (faculty_data['faculty_id'],))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return {
                'success': False,
                'message': 'Faculty ID already exists'
            }
        
        # Check if email already exists
        cursor.execute("SELECT email FROM faculty WHERE email = %s", 
                      (faculty_data['email'],))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return {
                'success': False,
                'message': 'Email already exists'
            }
        
        # Insert new faculty
        insert_query = """
        INSERT INTO faculty (faculty_id, password_hash, name, email, phone, department, designation)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            faculty_data['faculty_id'],
            faculty_data['password'],  # Plain text password as requested
            faculty_data['name'],
            faculty_data['email'],
            faculty_data.get('phone'),
            faculty_data.get('department'),
            faculty_data.get('designation')
        )
        
        cursor.execute(insert_query, values)
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return {
            'success': True,
            'message': 'Faculty created successfully',
            'faculty_id': faculty_data['faculty_id']
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Database error: {str(e)}'
        }
