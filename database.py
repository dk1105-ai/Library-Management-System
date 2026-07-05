import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root@123",
        database="library"
    )
    cursor = conn.cursor()
except Exception as e:
    print(f"Database Connection Error: {e}")