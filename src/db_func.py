import psycopg2
from PyQt6.QtWidgets import QMessageBox

# change this to db pass, leaving it blank for now
dbPass = "qazwsx"

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
def update_row(table: str, **data):
    try:
        connection = connect()
        cursor = connection.cursor()
        set_clause = ", ".join([f'"{column}" = %s' for column in data["new"].keys()])
        where_clause = " AND ".join([f'"{column}" = %s' for column in data["old"].keys()])
        
        new_values = tuple(data["new"].values())
        old_values = tuple(data["old"].values())
        values = new_values + old_values
        cursor.execute(f"UPDATE {table} SET {set_clause} WHERE {where_clause}", values)
        
        connection.commit()
        QMessageBox.information(None, "Success", f"Data updated from {table} successfully")
        return True
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Error updating data from table {table}: {e}")
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()
            
            
# delete row/s
def delete_row(table: str, **data):
    try:
        connection = connect()
        cursor = connection.cursor()

        # create WHERE clause dynamically depending on # of columns
        where_clause = " AND ".join([f'"{column}" = %s' for column in data.keys()])
        values = tuple(data.values())

        cursor.execute(f"DELETE FROM {table} WHERE {where_clause}", values)
        
        connection.commit()
        QMessageBox.information(None, "Success", f"Data deleted from {table} successfully")
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Error deleting data from table {table}: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()


def insert_row(table: str, **data):
    try:
        connection = connect()
        cursor = connection.cursor()
        
        columns = ", ".join([f'"{column}"' for column in data.keys()])
        placeholders = ", ".join(["%s"] * len(data))
        values = tuple(data.values())
        
        cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values)
        connection.commit()
        
        QMessageBox.information(None, "Success", f"Data inserted into {table} successfully")
        return True
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Error inserting data into table {table}: {e}")
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()


def select_row(table: str, **condition):
    try:
        connection = connect()
        cursor = connection.cursor()
        if condition:
            where_clause = " AND ".join([f'"{column}" = %s' for column in condition.keys()])
            values = tuple(condition.values())
            cursor.execute(f"SELECT * FROM {table} WHERE {where_clause}", values)
        else:
            cursor.execute(f"SELECT * FROM {table}")
        
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Error fetching data from table {table}: {e}")
        return None
    finally:
        if connection:
            cursor.close()
            connection.close()
