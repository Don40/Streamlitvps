import mysql.connector

# Create MySQL connection function
def get_db_connection():
    return mysql.connector.connect(
        host="46.202.164.177",
        port=3306,
        user="streamlit_vps_user",
        password="vps_streamlit",  # Change this to your actual MySQL root password
        database="my_streamlit"
    )

# Function to fetch all data
def view_all_data():
    conn = get_db_connection()  # Open connection
    c = conn.cursor(dictionary=True)  # Create a fresh cursor
    c.execute('SELECT * FROM customers ORDER BY id ASC')
    data = c.fetchall()  # Fetch all results
    c.close()  # Close cursor
    conn.close()  # Close connection
    return data

# Function to fetch unique department names
def view_all_departments():
    conn = get_db_connection()
    c = conn.cursor(dictionary=True)
    c.execute('SELECT DISTINCT Department FROM customers')  
    data = [row['Department'] for row in c.fetchall()]  # Extract department names
    c.close()
    conn.close()
    return data
