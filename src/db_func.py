import psycopg2
import os
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView
from dotenv import load_dotenv

load_dotenv()

# set the PASSWORD environment variable in .env
dbPass = os.getenv("PASSWORD")

# connect to db, return connection if successful else error
def connect():
    try:
        connection = psycopg2.connect(
            dbname=os.getenv("DATABASE_NAME"),
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            password=dbPass
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

def load_table_data(db_table_name: str, qt_table_widget, columns_to_display: list, clear_rows: bool = True):
    """
    Generalized function to load client data from a PostgreSQL table into a Qt table.

    Args:
        db_table_name (str): Name of the PostgreSQL table (e.g., "clients_nonlife").
        qt_table_widget (QTableWidget): The Qt table widget where data will be loaded.
        columns_to_display (list): List of column names to fetch from the database and show in the table.
    """
    try:
        conn = connect()
        cursor = conn.cursor()

        # Generate SQL query
        column_list = ', '.join(columns_to_display)
        query = f"SELECT {column_list} FROM {db_table_name}"
        cursor.execute(query)
        records = cursor.fetchall()

        # Clear existing rows
        if clear_rows:
            qt_table_widget.setRowCount(0)
        row_count = qt_table_widget.rowCount()
        qt_table_widget.setRowCount(row_count + len(records))

        # Populate the table
        for row_idx, row_data in enumerate(records):
            for col_idx, cell_data in enumerate(row_data):
                qt_table_widget.setItem(row_idx + row_count, col_idx, QTableWidgetItem(str(cell_data)))

        header = qt_table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error loading data from '{db_table_name}': {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def fetch_nonlife_clients(self):
    load_table_data("clients_nonlife", self.clients_non_life_dashboard_table, ["assured_name", "type_of_insurance", "policy_number", "expiry_date"])
    load_table_data("clients_hmo_individual", self.clients_hmo_dashboard_table, ["assured_name", "'Individual' AS type_of_hmo", "policy_number", "expiry_date"])
    load_table_data("clients_hmo_corporate", self.clients_hmo_dashboard_table, ["company_name", "'Corporate' AS type_of_hmo", "policy_number", "expiry_date"], False)
    self.clients_hmo_dashboard_count.setText( str(self.clients_hmo_dashboard_table.rowCount()) )
    self.clients_non_life_dashboard_count.setText( str(self.clients_non_life_dashboard_table.rowCount()) )

def insert_nonlife_client(self):
    try:
        conn = connect()
        cursor = conn.cursor()

        # Extract values from widgets
        name = self.clients_non_life_add_client_assured_name_line_edit.text()
        contact = self.clients_non_life_add_client_contact_number_line_edit.text()
        email = self.clients_non_life_add_client_email_line_edit.text()
        birthday = self.clients_non_life_add_client_birthday_line_edit.text()
        inception_date = self.clients_non_life_add_client_inception_date_line_edit.text()
        expiry_date = self.clients_non_life_add_client_expiry_date_line_edit.text()
        net_premium = self.clients_non_life_add_client_net_premium_line_edit.text()
        gross_premium = self.clients_non_life_add_client_gross_premium_line_edit.text()
        policy_number = self.clients_non_life_add_client_policy_number_line_edit.text()
        agent_code = self.clients_non_life_add_client_agent_code_line_edit.text()
        payment_invoice = self.clients_non_life_add_client_payment_invoice_line_edit.text()
        commission = self.clients_non_life_add_client_commission_line_edit.text()
        insurance_type = self.clients_non_life_add_client_insurance_type_combo_box.currentText()
        insurance_company = self.clients_non_life_add_client_insurance_company_line_edit.text()
        amount_covered = self.clients_non_life_add_client_amount_covered_line_edit.text()
        notes = self.clients_non_life_add_client_notes_text_edit.toPlainText()

        # Convert dates and numerics safely
        def parse_date(date_str):
            return datetime.strptime(date_str, "%Y/%m/%d").date() if date_str else None

        def parse_decimal(val):
            return float(val) if val else None

        def clean_text(val):
            return val.strip() if val.strip() else None

        name = clean_text(name)
        contact = clean_text(contact)
        email = clean_text(email)
        birthday = parse_date(birthday)
        inception_date = parse_date(inception_date)
        expiry_date = parse_date(expiry_date)
        net_premium = parse_decimal(net_premium)
        gross_premium = parse_decimal(gross_premium)
        policy_number = clean_text(policy_number)
        agent_code = clean_text(agent_code)
        payment_invoice = clean_text(payment_invoice)
        commission = parse_decimal(commission)
        insurance_type = clean_text(insurance_type)
        insurance_company = clean_text(insurance_company)
        amount_covered = parse_decimal(amount_covered)
        notes = clean_text(notes)

        # Insert into database
        cursor.execute("""
            INSERT INTO clients_nonlife (
                assured_name, contact_number, email, birthday,
                inception_date, expiry_date, net_premium, gross_premium,
                policy_number, agent_code, payment_invoice, commission,
                type_of_insurance, insurance_company, amount_covered, client_notes
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            name, contact, email, birthday,
            inception_date, expiry_date, net_premium, gross_premium,
            policy_number, agent_code, payment_invoice, commission,
            insurance_type, insurance_company, amount_covered, notes
        ))
        conn.commit()
        cursor.close()
        conn.close()

        fetch_nonlife_clients(self)
        QMessageBox.information(self, "Success", "Client added successfully!")

    except Exception as e:
        QMessageBox.critical(self, "Database Error", f"Failed to insert client:\n{e}")
    finally:
        if conn:
            cursor.close()
            conn.close()