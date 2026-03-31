#db.py
import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host="college-attendance-management-system.cnsm4u028xzh.ap-south-1.rds.amazonaws.com",
        database="somaiya_db",
        user="prayagupadhyaya",
        password="Prayag2308",
        port="5432"
    )