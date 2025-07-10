import psycopg2
import os
import bcrypt
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView, QInputDialog
from PyQt6.QtCore import Qt
from dotenv import load_dotenv
from decimal import Decimal

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
    

def load_table_data(db_table_name: str, qt_table_widget, columns_to_display: list, condition = '', clear_rows: bool = True):
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
        query += f" {condition}"
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

def fetch_client_table_data(self):
    load_table_data("clients_nonlife", self.clients_non_life_dashboard_table, ["assured_name", "type_of_insurance", "policy_number", "expiry_date"], "WHERE status = 'active'")
    load_table_data("clients_hmo_individual", self.clients_hmo_dashboard_table, ["assured_name", "'Individual' AS type_of_hmo", "policy_number", "expiry_date"], "WHERE status = 'active'")
    load_table_data("clients_hmo_corporate", self.clients_hmo_dashboard_table, ["company_name", "'Corporate' AS type_of_hmo", "policy_number", "expiry_date"], "WHERE status = 'active'", False)
    self.clients_non_life_dashboard_count.setText( str(self.clients_non_life_dashboard_table.rowCount()) )
    self.clients_hmo_dashboard_count.setText( str(self.clients_hmo_dashboard_table.rowCount()) )

def fetch_company_table_data(self):
    load_table_data("clients_nonlife", self.companies_non_life_dashboard_table, ["assured_name", "type_of_insurance", "insurance_company", "expiry_date"], "WHERE status = 'active'")
    load_table_data("clients_hmo_individual", self.companies_hmo_dashboard_table, ["assured_name", "'Individual' AS type_of_hmo", "hmo_company", "expiry_date"], "WHERE status = 'active'")
    load_table_data("clients_hmo_corporate", self.companies_hmo_dashboard_table, ["company_name", "'Corporate' AS type_of_hmo", "hmo_company", "expiry_date"], "WHERE status = 'active'", False)
    self.companies_non_life_dashboard_count.setText( str(self.companies_non_life_dashboard_table.rowCount()) )
    self.companies_hmo_dashboard_count.setText( str(self.companies_hmo_dashboard_table.rowCount()) )

def fetch_archive_table_data(self):
    load_table_data("clients_nonlife", self.archives_non_life_dashboard_table, ["assured_name", "type_of_insurance", "policy_number", "expiry_date"], "WHERE status = 'archived'")
    load_table_data("clients_hmo_individual", self.archives_hmo_dashboard_table, ["assured_name", "'Individual' AS type_of_hmo", "policy_number", "expiry_date"], "WHERE status = 'archived'")
    load_table_data("clients_hmo_corporate", self.archives_hmo_dashboard_table, ["company_name", "'Corporate' AS type_of_hmo", "policy_number", "expiry_date"], "WHERE status = 'archived'", False)
    self.archives_non_life_dashboard_count.setText( str(self.archives_non_life_dashboard_table.rowCount()) )
    self.archives_hmo_dashboard_count.setText( str(self.archives_hmo_dashboard_table.rowCount()) )

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

        # Validate NOT NULL fields
        if not name or not expiry_date or not policy_number or not insurance_type:
            QMessageBox.warning(self, "Missing Fields", "Please fill in all required fields: Assured Name, Expiry Date, Policy Number, Type of Insurance.")
            return

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

        fetch_client_table_data(self)
        QMessageBox.information(self, "Success", "Client added successfully!")

    except Exception as e:
        QMessageBox.critical(self, "Database Error", f"Failed to insert client:\n{e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def insert_hmo_individual_client(self):
    try:
        conn = connect()
        cursor = conn.cursor()

        # Extract values from widgets
        name = self.clients_hmo_add_client_individual_assured_name_line_edit.text()
        contact = self.clients_hmo_add_client_individual_contact_number_line_edit.text()
        email = self.clients_hmo_add_client_individual_email_line_edit.text()
        birthday = self.clients_hmo_add_client_individual_birthday_line_edit.text()
        hmo_company = self.clients_hmo_add_client_individual_hmo_company_line_edit.text()
        inception_date = self.clients_hmo_add_client_individual_inception_date_line_edit.text()
        expiry_date = self.clients_hmo_add_client_individual_expiry_date_line_edit.text()
        agent_code = self.clients_hmo_add_client_individual_agent_code_line_edit.text()
        policy_number = self.clients_hmo_add_client_individual_policy_number_line_edit.text()
        mbl_abl = self.clients_hmo_add_client_individual_mbl_abl_line_edit.text()
        net_premium = self.clients_hmo_add_client_individual_net_premium_line_edit.text()
        gross_premium = self.clients_hmo_add_client_individual_gross_premium_line_edit.text()
        commission = self.clients_hmo_add_client_individual_commission_line_edit.text()
        notes = self.clients_hmo_add_client_individual_notes_text_edit.toPlainText()

        # Convert dates and numerics safely
        def parse_date(date_str):
            return datetime.strptime(date_str, "%Y/%m/%d").date() if date_str else None

        def parse_decimal(val):
            return float(val) if val else None

        def clean_text(val):
            return val.strip() if val.strip() else None

        # Cleaned and parsed values
        name = clean_text(name)
        contact = clean_text(contact)
        email = clean_text(email)
        birthday = parse_date(birthday)
        hmo_company = clean_text(hmo_company)
        inception_date = parse_date(inception_date)
        expiry_date = parse_date(expiry_date)
        agent_code = clean_text(agent_code)
        policy_number = clean_text(policy_number)
        mbl_abl = clean_text(mbl_abl)
        net_premium = parse_decimal(net_premium)
        gross_premium = parse_decimal(gross_premium)
        commission = parse_decimal(commission)
        notes = clean_text(notes)

        # Validate NOT NULL fields
        if not name or not expiry_date or not policy_number:
            QMessageBox.warning(self, "Missing Fields", "Please fill in all required fields: Assured Name, Expiry Date, Policy Number.")
            return

        # Insert into database
        cursor.execute("""
            INSERT INTO clients_hmo_individual (
                assured_name, contact_number, email, birthday, hmo_company,
                inception_date, expiry_date, agent_code, policy_number,
                mbl_abl, net_premium, gross_premium, commission,
                client_notes
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            name, contact, email, birthday, hmo_company,
            inception_date, expiry_date, agent_code, policy_number,
            mbl_abl, net_premium, gross_premium, commission,
            notes
        ))
        conn.commit()
        cursor.close()
        conn.close()

        fetch_client_table_data(self)  # You can define this to refresh the client list
        QMessageBox.information(self, "Success", "HMO Individual client added successfully!")

    except Exception as e:
        QMessageBox.critical(self, "Database Error", f"Failed to insert client:\n{e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def insert_hmo_corporate_client(self):
    try:
        conn = connect()
        cursor = conn.cursor()

        # Extract values from widgets
        company_name = self.clients_hmo_add_client_corporate_company_name_line_edit.text()
        number_of_enrollees = self.clients_hmo_add_client_corporate_number_of_enrollees_line_edit.text()
        contact = self.clients_hmo_add_client_corporate_contact_number_line_edit.text()
        email = self.clients_hmo_add_client_corporate_email_line_edit.text()
        hmo_company = self.clients_hmo_add_client_corporate_hmo_company_line_edit.text()
        inception_date = self.clients_hmo_add_client_corporate_inception_date_line_edit.text()
        expiry_date = self.clients_hmo_add_client_corporate_expiry_date_line_edit.text()
        agent_code = self.clients_hmo_add_client_corporate_agent_code_line_edit.text()
        policy_number = self.clients_hmo_add_client_corporate_policy_number_line_edit.text()
        mbl_abl = self.clients_hmo_add_client_corporate_mbl_abl_line_edit.text()
        net_premium = self.clients_hmo_add_client_corporate_net_premium_line_edit.text()
        gross_premium = self.clients_hmo_add_client_corporate_gross_premium_line_edit.text()
        commission = self.clients_hmo_add_client_corporate_commission_line_edit.text()
        notes = self.clients_hmo_add_client_corporate_notes_text_edit.toPlainText()

        # Convert and sanitize input
        def parse_date(date_str):
            return datetime.strptime(date_str, "%Y/%m/%d").date() if date_str else None

        def parse_decimal(val):
            return float(val) if val else None

        def parse_int(val):
            return int(val) if val else None

        def clean_text(val):
            return val.strip() if val.strip() else None

        company_name = clean_text(company_name)
        number_of_enrollees = parse_int(number_of_enrollees)
        contact = clean_text(contact)
        email = clean_text(email)
        hmo_company = clean_text(hmo_company)
        inception_date = parse_date(inception_date)
        expiry_date = parse_date(expiry_date)
        agent_code = clean_text(agent_code)
        policy_number = clean_text(policy_number)
        mbl_abl = clean_text(mbl_abl)
        net_premium = parse_decimal(net_premium)
        gross_premium = parse_decimal(gross_premium)
        commission = parse_decimal(commission)
        notes = clean_text(notes)

        # Validate required fields
        if not company_name or not policy_number or not expiry_date:
            QMessageBox.warning(self, "Missing Fields", "Please fill in all required fields: Company Name, Policy Number, Expiry Date.")
            return

        # Insert into database
        cursor.execute("""
            INSERT INTO clients_hmo_corporate (
                company_name, number_of_enrollees, contact_number, email,
                hmo_company, inception_date, expiry_date, agent_code,
                policy_number, mbl_abl, net_premium, gross_premium,
                commission, client_notes
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            company_name, number_of_enrollees, contact, email,
            hmo_company, inception_date, expiry_date, agent_code,
            policy_number, mbl_abl, net_premium, gross_premium,
            commission, notes
        ))

        conn.commit()
        cursor.close()
        conn.close()

        fetch_client_table_data(self)  # Refresh table view, if defined
        QMessageBox.information(self, "Success", "HMO Corporate client added successfully!")

    except Exception as e:
        QMessageBox.critical(self, "Database Error", f"Failed to insert corporate client:\n{e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def archive_nonlife_client(self):
    try:
        conn = connect()
        cursor = conn.cursor()
        
        selected_rows = self.clients_non_life_dashboard_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a row to archive.")
            return

        for model_index in selected_rows:
            row = model_index.row()
            policy_number_item = self.clients_non_life_dashboard_table.item(row, 2)  # Assuming column 2 is policy_number

            if not policy_number_item:
                continue

            policy_number = policy_number_item.text().strip()

            if not policy_number:
                QMessageBox.warning(self, "Missing Info", "Cannot archive without a valid policy number.")
                return

            # Update DB
            cursor.execute("""
                UPDATE clients_nonlife
                SET status = 'archived', updated_at = CURRENT_TIMESTAMP
                WHERE policy_number = %s
            """, (policy_number,))
            conn.commit()

        cursor.close()
        conn.close()

        QMessageBox.information(self, "Success", "Selected client(s) archived.")
        fetch_client_table_data(self)

    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to archive client:\n{e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def archive_hmo_client(self):
    try:
        conn = connect()
        cursor = conn.cursor()

        selected_rows = self.clients_hmo_dashboard_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a row to archive.")
            return

        for model_index in selected_rows:
            row = model_index.row()
            type_item = self.clients_hmo_dashboard_table.item(row, 1)  # Type column
            policy_number_item = self.clients_hmo_dashboard_table.item(row, 2)  # Policy number column

            if not type_item or not policy_number_item:
                continue

            hmo_type = type_item.text().strip().lower()
            policy_number = policy_number_item.text().strip()

            if not policy_number:
                QMessageBox.warning(self, "Missing Info", "Missing policy number in selected row.")
                return

            # Determine target table
            if hmo_type == "individual":
                table_name = "clients_hmo_individual"
            elif hmo_type == "corporate":
                table_name = "clients_hmo_corporate"
            else:
                QMessageBox.warning(self, "Unknown Type", f"Unrecognized HMO type: {hmo_type}")
                return

            # Update the correct table
            cursor.execute(f"""
                UPDATE {table_name}
                SET status = 'archived', updated_at = CURRENT_TIMESTAMP
                WHERE policy_number = %s
            """, (policy_number,))
            conn.commit()

        cursor.close()
        conn.close()

        QMessageBox.information(self, "Success", "Selected HMO client(s) archived.")
        fetch_client_table_data(self)

    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to archive HMO client:\n{e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def restore_nonlife_client(self):
    try:
        conn = connect()
        cursor = conn.cursor()

        selected_rows = self.archives_non_life_dashboard_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a row to restore.")
            return

        for model_index in selected_rows:
            row = model_index.row()
            policy_number_item = self.archives_non_life_dashboard_table.item(row, 2)  # Column 3 = policy number

            if not policy_number_item:
                continue

            policy_number = policy_number_item.text().strip()

            if not policy_number:
                QMessageBox.warning(self, "Missing Info", "Missing policy number in selected row.")
                return

            cursor.execute("""
                UPDATE clients_nonlife
                SET status = 'active', updated_at = CURRENT_TIMESTAMP
                WHERE policy_number = %s
            """, (policy_number,))
            conn.commit()

        cursor.close()
        conn.close()

        QMessageBox.information(self, "Success", "Client(s) restored.")
        fetch_archive_table_data(self)

    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to restore client:\n{e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def delete_nonlife_client(self):
    try:
        conn = connect()
        cursor = conn.cursor()

        selected_rows = self.archives_non_life_dashboard_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a row to delete.")
            return

        for model_index in selected_rows:
            row = model_index.row()
            policy_number_item = self.archives_non_life_dashboard_table.item(row, 2)  # Column 3 = policy number

            if not policy_number_item:
                continue

            policy_number = policy_number_item.text().strip()

            if not policy_number:
                QMessageBox.warning(self, "Missing Info", "Missing policy number in selected row.")
                return

            cursor.execute("""
                UPDATE clients_nonlife
                SET status = 'deleted', updated_at = CURRENT_TIMESTAMP
                WHERE policy_number = %s
            """, (policy_number,))
            conn.commit()

        cursor.close()
        conn.close()

        QMessageBox.information(self, "Success", "Client(s) marked as deleted.")
        fetch_archive_table_data(self)

    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to delete client:\n{e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def restore_hmo_client(self):
    try:
        conn = connect()
        cursor = conn.cursor()

        selected_rows = self.archives_hmo_dashboard_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a row to restore.")
            return

        for model_index in selected_rows:
            row = model_index.row()
            policy_number_item = self.archives_hmo_dashboard_table.item(row, 2)  # Column 3 = policy number

            if not policy_number_item:
                continue

            policy_number = policy_number_item.text().strip()

            if not policy_number:
                QMessageBox.warning(self, "Missing Info", "Missing policy number in selected row.")
                return

            # Restore from both individual and corporate tables
            for table in ("clients_hmo_individual", "clients_hmo_corporate"):
                cursor.execute(f"""
                    UPDATE {table}
                    SET status = 'active', updated_at = CURRENT_TIMESTAMP
                    WHERE policy_number = %s
                """, (policy_number,))
            conn.commit()

        cursor.close()
        conn.close()

        QMessageBox.information(self, "Success", "HMO client(s) restored.")
        fetch_archive_table_data(self)

    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to restore HMO client:\n{e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def delete_hmo_client(self):
    try:
        conn = connect()
        cursor = conn.cursor()

        selected_rows = self.archives_hmo_dashboard_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a row to delete.")
            return

        for model_index in selected_rows:
            row = model_index.row()
            policy_number_item = self.archives_hmo_dashboard_table.item(row, 2)  # Column 3 = policy number

            if not policy_number_item:
                continue

            policy_number = policy_number_item.text().strip()

            if not policy_number:
                QMessageBox.warning(self, "Missing Info", "Missing policy number in selected row.")
                return

            # Soft-delete in both HMO tables
            for table in ("clients_hmo_individual", "clients_hmo_corporate"):
                cursor.execute(f"""
                    UPDATE {table}
                    SET status = 'deleted', updated_at = CURRENT_TIMESTAMP
                    WHERE policy_number = %s
                """, (policy_number,))
            conn.commit()

        cursor.close()
        conn.close()

        QMessageBox.information(self, "Success", "HMO client(s) marked as deleted.")
        fetch_archive_table_data(self)

    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to delete HMO client:\n{e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def record_policy_payment_nonlife(self):
    try:
        conn = connect()
        cursor = conn.cursor()

        selected_rows = self.clients_non_life_dashboard_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a policy row.")
            return

        row = selected_rows[0].row()
        policy_number = self.clients_non_life_dashboard_table.item(row, 2).text().strip()

        # Get gross premium from clients_nonlife
        cursor.execute("""
            SELECT gross_premium
            FROM clients_nonlife
            WHERE policy_number = %s
        """, (policy_number,))
        result = cursor.fetchone()

        if not result:
            QMessageBox.critical(self, "Not Found", "Policy not found in clients_nonlife.")
            return

        gross_premium = result[0] or 0

        # Prompt for amount paid
        amount_paid, ok = QInputDialog.getDouble(self, "Payment", "Enter amount paid:")
        if not ok:
            return

        amount_paid = Decimal(str(amount_paid))

        # Prompt for payment method
        payment_methods = ["Cash", "Bank Transfer", "GCash", "Check", "Others"]
        method, ok = QInputDialog.getItem(self, "Payment Method", "Select payment method:", payment_methods, 0, False)
        if not ok or not method:
            return

        payment_date = datetime.now().date()

        # Calculate total paid so far for this policy
        cursor.execute("""
            SELECT COALESCE(SUM(amount_paid), 0)
            FROM client_payments
            WHERE policy_number = %s
        """, (policy_number,))
        total_paid_before = cursor.fetchone()[0] or 0
        total_paid_after = total_paid_before + amount_paid

        status = "Paid" if total_paid_after >= gross_premium else "Partial"

        # Insert new payment
        cursor.execute("""
            INSERT INTO client_payments (
                policy_number,
                payment_date, payment_method, status, amount_paid
            ) VALUES (%s, %s, %s, %s, %s)
        """, (
            policy_number,
            payment_date, method, status, amount_paid
        ))

        conn.commit()
        QMessageBox.information(self, "Success", f"Payment recorded. Status: {status}")

    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to record payment:\n{e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def record_policy_payment_hmo(self):
    try:
        conn = connect()
        cursor = conn.cursor()

        selected_rows = self.clients_hmo_dashboard_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a policy row.")
            return

        row = selected_rows[0].row()
        policy_number = self.clients_hmo_dashboard_table.item(row, 2).text().strip()

        # Try fetching from individual first
        cursor.execute("""
            SELECT gross_premium FROM clients_hmo_individual
            WHERE policy_number = %s
        """, (policy_number,))
        result = cursor.fetchone()

        if result is None:
            # Try corporate instead
            cursor.execute("""
                SELECT gross_premium FROM clients_hmo_corporate
                WHERE policy_number = %s
            """, (policy_number,))
            result = cursor.fetchone()

        if not result:
            QMessageBox.critical(self, "Not Found", "Policy not found in HMO clients.")
            return

        gross_premium = result[0] or Decimal("0.00")

        # Prompt for amount paid
        amount_paid, ok = QInputDialog.getDouble(self, "Payment", "Enter amount paid:")
        if not ok:
            return

        amount_paid = Decimal(str(amount_paid))

        # Prompt for payment method
        payment_methods = ["Cash", "Bank Transfer", "GCash", "Check", "Others"]
        method, ok = QInputDialog.getItem(self, "Payment Method", "Select payment method:", payment_methods, 0, False)
        if not ok or not method:
            return

        payment_date = datetime.now().date()

        # Calculate total paid so far for this policy
        cursor.execute("""
            SELECT COALESCE(SUM(amount_paid), 0)
            FROM client_payments
            WHERE policy_number = %s
        """, (policy_number,))
        total_paid_before = cursor.fetchone()[0] or Decimal("0.00")
        if not isinstance(total_paid_before, Decimal):
            total_paid_before = Decimal(str(total_paid_before))

        total_paid_after = total_paid_before + amount_paid
        status = "Paid" if total_paid_after >= gross_premium else "Partial"

        # Insert new payment
        cursor.execute("""
            INSERT INTO client_payments (
                policy_number,
                payment_date, payment_method, status, amount_paid
            ) VALUES (%s, %s, %s, %s, %s)
        """, (
            policy_number,
            payment_date, method, status, amount_paid
        ))

        conn.commit()
        QMessageBox.information(self, "Success", f"Payment recorded. Status: {status}")

    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to record payment:\n{e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def fetch_all_client_payments(self):
    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                COALESCE(cnl.assured_name, chmi.assured_name, chmc.company_name) AS client_name,
                cp.policy_number,
                cp.amount_paid,
                cp.payment_method,
                COALESCE(cnl.gross_premium, chmi.gross_premium, chmc.gross_premium) AS total_premium_due,
                cp.status,
                cp.payment_date
            FROM client_payments cp
            LEFT JOIN clients_nonlife cnl ON cp.policy_number = cnl.policy_number
            LEFT JOIN clients_hmo_individual chmi ON cp.policy_number = chmi.policy_number
            LEFT JOIN clients_hmo_corporate chmc ON cp.policy_number = chmc.policy_number
            ORDER BY cp.payment_date DESC
        """)

        rows = cursor.fetchall()

        # Clear existing rows
        self.client_payments_table.setRowCount(0)
        self.client_payments_table.setRowCount(len(rows))

        for row_index, row_data in enumerate(rows):
            for col_index, value in enumerate(row_data):
                item = QTableWidgetItem(str(value) if value is not None else "")
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.client_payments_table.setItem(row_index, col_index, item)

        self.client_payments_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)


    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to fetch client payments:\n{e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


def register_user(username, password, email=None):
    try:
        conn = connect()
        cursor = conn.cursor()
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        cursor.execute("""
            INSERT INTO users (username, password_hash, email, status)
            VALUES (%s, %s, %s, 'pending')
        """, (username, password_hash, email))
        conn.commit()
        return True
    except Exception as e:
        print("Registration error:", e)
        return False
    finally:
        if conn:
            cursor.close()
            conn.close()

def login_user(username, password):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT password_hash, status FROM users WHERE username = %s
        """, (username,))
        row = cursor.fetchone()

        if row is None:
            print("Username not found:", username)
            return False

        password_hash, status = row

        if status != 'approved':
            print("User not approved:", username)
            return False

        if isinstance(password_hash, str):
            password_hash = password_hash.encode()

        return bcrypt.checkpw(password.encode(), password_hash)
    except Exception as e:
        print("Login error:", e)
        print("Checking login for:", username)
        print("Typed password:", password)

        if row:
            print("Hash from DB:", row[0])
            print("Match:", bcrypt.checkpw(password.encode(), row[0].encode()))
        else:
            print("Username not found")
        return False
    finally:
        if conn:
            cursor.close()
            conn.close()

def load_user_account(self, username):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT full_name, username, agent_number, email, contact_number
            FROM users
            WHERE username = %s
        """, (username,))
        user = cursor.fetchone()
        if user:
            self.account_full_name_line_edit.setText(user[0] or "")
            self.account_username_line_edit.setText(user[1] or "")
            self.account_agent_number_line_edit.setText(user[2] or "")
            self.account_email_line_edit.setText(user[3] or "")
            self.account_contact_number_line_edit.setText(user[4] or "")
        cursor.close()
        conn.close()
    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to load account:\n{e}")

def save_user_account(self, username):
    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET full_name = %s,
                agent_number = %s,
                email = %s,
                contact_number = %s
            WHERE username = %s
        """, (
            self.account_full_name_line_edit.text(),
            self.account_agent_number_line_edit.text(),
            self.account_email_line_edit.text(),
            self.account_contact_number_line_edit.text(),
            username
        ))

        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to save account:\n{e}")

def change_user_password(username, old_password, new_password):
    try:
        conn = connect()
        cursor = conn.cursor()

        # Get old password hash
        cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        row = cursor.fetchone()
        if not row:
            return False

        stored_hash = row[0]
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode()

        if not bcrypt.checkpw(old_password.encode(), stored_hash):
            return False  # old password doesn't match

        # Hash new password
        new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()

        # Update password in DB
        cursor.execute("UPDATE users SET password_hash = %s WHERE username = %s", (new_hash, username))
        conn.commit()
        return True

    except Exception as e:
        print("Change password error:", e)
        return False

    finally:
        if conn:
            cursor.close()
            conn.close()