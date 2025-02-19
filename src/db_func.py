import psycopg2
from PyQt6.QtWidgets import QMessageBox

# change this to db pass, leaving it blank for now
dbPass = ""
currentTable = "public.test"

# connect to db, return connection if successful else error
def connect():
    try:
        connection = psycopg2.connect(
            dbname="test",
            host="localhost",
            user="postgres",
            password=dbPass,
        )
        return connection
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Error connecting to database: {e}")
        return None
    

# update row/s
# havent tested for postgresql yet, but it should work?
def update_row(**data):
    try:
        connection = connect()
        cursor = connection.cursor()
        set_clause = ", ".join([f'"{column}" = %s' for column in data["new"].keys()])
        where_clause = " AND ".join([f'"{column}" = %s' for column in data["old"].keys()])
        
        new_values = tuple(data["new"].values())
        old_values = tuple(data["old"].values())
        values = new_values + old_values
        cursor.execute(f"UPDATE {currentTable} SET {set_clause} WHERE {where_clause}", values)
        
        connection.commit()
        QMessageBox.information(None, "Success", f"Data updated from {currentTable} successfully")
        return True
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Error updating data from table {currentTable}: {e}")
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()
            
            
# delete row/s
def delete_row(**data):
    try:
        connection = connect()
        cursor = connection.cursor()

        # create WHERE clause dynamically depending on # of columns
        where_clause = " AND ".join([f'"{column}" = %s' for column in data.keys()])
        values = tuple(data.values())

        cursor.execute(f"DELETE FROM {currentTable} WHERE {where_clause}", values)
        
        connection.commit()
        QMessageBox.information(None, "Success", f"Data deleted from {currentTable} successfully")
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Error deleting data from table {currentTable}: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()