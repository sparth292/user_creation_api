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

def get_all_faculties():
    """
    Get all faculties from the database
    
    Returns:
        dict: Result with success status, message, and faculties list
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT faculty_id, name, email, phone, department, designation 
            FROM faculty 
            ORDER BY faculty_id
        """)
        
        results = cursor.fetchall()
        
        faculties = []
        for row in results:
            faculty_dict = {
                'faculty_id': row[0],
                'name': row[1],
                'email': row[2],
                'phone': row[3],
                'department': row[4],
                'designation': row[5]
            }
            faculties.append(faculty_dict)
        
        cursor.close()
        conn.close()
        
        return {
            'success': True,
            'message': 'Faculties retrieved successfully',
            'faculties': faculties
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Database error: {str(e)}'
        }

def get_faculty_by_id(faculty_id):
    """
    Get faculty by ID
    
    Args:
        faculty_id (str): Faculty ID to search for
    
    Returns:
        dict: Result with success status, message, and faculty data
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT faculty_id, name, email, phone, department, designation 
            FROM faculty 
            WHERE faculty_id = %s
        """, (faculty_id,))
        
        result = cursor.fetchone()
        
        if not result:
            cursor.close()
            conn.close()
            return {
                'success': False,
                'message': 'Faculty not found'
            }
        
        faculty_dict = {
            'faculty_id': result[0],
            'name': result[1],
            'email': result[2],
            'phone': result[3],
            'department': result[4],
            'designation': result[5]
        }
        
        cursor.close()
        conn.close()
        
        return {
            'success': True,
            'message': 'Faculty retrieved successfully',
            'faculty': faculty_dict
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Database error: {str(e)}'
        }

def delete_faculty(faculty_id):
    """
    Delete faculty by ID
    
    Args:
        faculty_id (str): Faculty ID to delete
    
    Returns:
        dict: Result with success status and message
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if faculty exists
        cursor.execute("SELECT faculty_id FROM faculty WHERE faculty_id = %s", (faculty_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return {
                'success': False,
                'message': 'Faculty not found'
            }
        
        # Delete faculty
        cursor.execute("DELETE FROM faculty WHERE faculty_id = %s", (faculty_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return {
            'success': True,
            'message': 'Faculty deleted successfully'
        }
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
            cursor.close()
            conn.close()
        return {
            'success': False,
            'message': f'Database error: {str(e)}'
        }
