from db import get_db_connection

class RoomService:
    
    @staticmethod
    def create_room(room_data):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO room_numbers (room_number, room_type)
                VALUES (%s, %s)
                RETURNING room_id, room_number, room_type
            """, (
                room_data['room_number'],
                room_data['room_type']
            ))
            
            result = cursor.fetchone()
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return {'message': 'Room created successfully', 'room': result}, 201
            
        except Exception as e:
            return {'error': str(e)}, 500
    
    @staticmethod
    def get_all_rooms():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM room_numbers ORDER BY room_id")
            rooms = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return {'rooms': rooms}, 200
            
        except Exception as e:
            return {'error': str(e)}, 500
    
    @staticmethod
    def get_room_by_id(room_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM room_numbers WHERE room_id = %s", (room_id,))
            room = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if not room:
                return {'error': 'Room not found'}, 404
            
            return {'room': room}, 200
            
        except Exception as e:
            return {'error': str(e)}, 500
    
    @staticmethod
    def delete_room(room_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM room_numbers WHERE room_id = %s", (room_id,))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return {'message': 'Room deleted successfully'}, 200
            
        except Exception as e:
            return {'error': str(e)}, 500
