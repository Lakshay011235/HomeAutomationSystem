import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve database credentials from environment variables
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Connect to the database
try:
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    print("Connected to the database")

    # Example: Execute a query
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    print("Users:")
    for user in users:
        print(user)

     # Close connection
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Connection closed")
        
except mysql.connector.Error as error:
    print("Error:", error)
    
    
# def getData(userId, userPassword, )