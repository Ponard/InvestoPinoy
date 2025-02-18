import psycopg2
from PyQt6.QtWidgets import QMessageBox

# change this to db pass, leaving it blank for now
dbPass = ""

# connect to db, return connection if successful else error
def connect():
    try:
        connection = psycopg2.connect(
            host="localhost",
            user="root",
            password=dbPass
        )
        return connection
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Error connecting to database: {e}")
        return None