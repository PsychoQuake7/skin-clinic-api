import mysql.connector
from config import DB_CONFIG

def inspect_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DESCRIBE patients")
        columns = cursor.fetchall()
        print("Columns in patients table:")
        for col in columns:
            print(col)
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_db()
