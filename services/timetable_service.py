import psycopg2
import datetime
from db import get_db_connection

class TimetableService:
    @staticmethod
    def get_timetable_by_batch(batch):
        """
        Fetch timetables from database by batch
        If batch is empty string, returns all timetables
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            if batch:
                query = "SELECT * FROM timetable WHERE batch = %s"
                cursor.execute(query, (batch,))
            else:
                query = "SELECT * FROM timetable WHERE batch = ''"
                cursor.execute(query)
            
            columns = [desc[0] for desc in cursor.description]
            timetables = cursor.fetchall()
            
            result_list = []
            for row in timetables:
                result_dict = dict(zip(columns, row))
                # Convert datetime/time objects to strings for JSON serialization
                for key, value in result_dict.items():
                    if isinstance(value, (datetime.datetime, datetime.date, datetime.time)):
                        result_dict[key] = str(value)
                result_list.append(result_dict)
            
            return {
                "success": True,
                "data": result_list,
                "count": len(result_list)
            }
            
        except psycopg2.Error as e:
            return {
                "success": False,
                "message": f"Database error: {str(e)}"
            }
        finally:
            cursor.close()
            conn.close()
