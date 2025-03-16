import mysql.connector
# pip install mysql-connector-python
import streamlit as st

# Create MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    port=3306,  # No quotes, since it's an integer
    user="root",
    password="dada",  # Change this to your actual MySQL root password
    database="my_streamlit"
)

# Use a dictionary cursor to return column names
c = conn.cursor(dictionary=True)

# Function to fetch all data
def view_all_data():
    c.execute('SELECT * FROM customers ORDER BY id ASC')
    data = c.fetchall()
    return data

# Function to fetch department data
def view_all_departments():
    c.execute('SELECT DISTINCT Department FROM customers')  # DISTINCT avoids duplicate values
    data = c.fetchall()  # Fetch all results
    return [row['Department'] for row in data]  # Extract only department names
