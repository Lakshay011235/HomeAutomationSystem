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

# Connect to MySQL server
db_connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
)

# Create a cursor object
cursor = db_connection.cursor()

# Create a new database
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

# Switch to the new database
cursor.execute(f"USE {db_name}")

# Create Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Create Posts table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Posts (
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
)
""")

# Commit changes and close connection
db_connection.commit()
cursor.close()
db_connection.close()

print("Database and tables created successfully!")
