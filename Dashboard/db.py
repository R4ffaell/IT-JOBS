import mysql.connector
import pandas as pd

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="xxx",
        password="xxx!",
        database="xxx"
    )

def fetch_data():
    conn = get_connection()
    query = "SELECT * FROM job_opportunities"

    # ✅ Workaround: Use cursor and fetchall() since `mysql.connector` doesn't support `pd.read_sql()`
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    data = cursor.fetchall()
    
    # ✅ Convert fetched data to DataFrame
    df = pd.DataFrame(data)

    cursor.close()
    conn.close()
    return df

# ✅ Now Fetch Data and Check Column Names
df = fetch_data()
print(df.columns)
