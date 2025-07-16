import os
import sys
import db_func
import csv
from PyQt6.QtWidgets import QApplication, QWidget, QHeaderView, QAbstractItemView, QMessageBox, QSizePolicy, QTableWidget, QLabel, QFrame, QPushButton, QHBoxLayout, QFileDialog
from PyQt6.QtCore import QMetaObject
from PyQt6 import uic
from datetime import datetime
from openpyxl import Workbook
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

if sys.platform.startswith('linux'):
    print("Running on Linux")
elif sys.platform.startswith('win'):
    print("Running on Windows")
    os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=0"
elif sys.platform.startswith('darwin'):
    print("Running on macOS")
else:
    print("Unknown operating system")

# Monkey-patch to disable auto-connections globally
QMetaObject.connectSlotsByName = lambda *args, **kwargs: None

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi("QtGUI/login.ui", self)
        self.login_button.clicked.connect(self.on_login)
        self.register_button.clicked.connect(self.on_register)

    def on_login(self):
        username = self.login_username.text().strip()
        password = self.login_password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Login", "Username and password are required.")
            return

        if db_func.login_user(username, password):
            QMessageBox.information(self, "Login", "Login successful!")

            # Launch main window
            self.main_window = MainWindow(current_username=username)
            self.main_window.show()
            self.close()  # close login window
        
        if not db_func.login_user(username, password):
            QMessageBox.warning(self, "Login", "Invalid credentials or account not yet approved.")

    def on_register(self):
        username = self.login_username.text().strip()
        password = self.login_password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Register", "Username and password are required.")
            return

        if db_func.register_user(username, password, email=None):
            QMessageBox.information(self, "Register", "Registration will be reviewed!")
        else:
            QMessageBox.warning(self, "Register", "Registration failed. Username may already exist.")


class MainWindow(QWidget):
    def __init__(self, current_username=None):
        super().__init__()
        uic.loadUi("QtGUI/form.ui", self)
        self.current_username = current_username
        self.showMaximized()
        
        # connect to DB
        db_func.connect()

        self.load_expiring_policies_grouped(self)

        # connect button to function
        self.navigation_home_button.clicked.connect(self.on_home_button_clicked)
        self.navigation_clients_button.clicked.connect(self.on_clients_button_clicked)
        self.navigation_companies_button.clicked.connect(self.on_companies_button_clicked)
        self.navigation_collection_button.clicked.connect(self.on_collection_button_clicked)
        self.navigation_archives_button.clicked.connect(self.on_archives_button_clicked)
        self.navigation_account_button.clicked.connect(self.on_account_button_clicked)
        self.navigation_logout_button.clicked.connect(self.on_logout_button_clicked)

        # connect search bar
        # self.search_edit.textChanged.connect(self.on_search_text_changed)
        self.clients_search_edit.textChanged.connect(self.on_search_text_changed)
        self.clients_hmo_search_edit.textChanged.connect(self.on_search_text_changed)
        self.archives_search_edit.textChanged.connect(self.on_search_text_changed)
        self.archives_hmo_search_edit.textChanged.connect(self.on_search_text_changed)
        
        # add client buttons
        self.clients_non_life_add_client_submit_push_button.clicked.connect(self.on_clients_non_life_add_client_submit_push_button_clicked)
        self.clients_hmo_add_client_individual_submit_push_button.clicked.connect(self.on_clients_hmo_add_client_individual_submit_push_button_clicked)
        self.clients_hmo_add_client_corporate_submit_push_button.clicked.connect(self.on_clients_hmo_add_client_corporate_submit_push_button_clicked)

        # set view policy fields to read only
        self.set_view_policy_fields_readonly(True)
        self.set_hmo_individual_view_policy_fields_readonly(True)
        self.set_hmo_corporate_view_policy_fields_readonly(True)

        # allow view policy fields to be edited
        self.clients_non_life_view_policy_edit_push_button.clicked.connect(self.on_clients_non_life_view_policy_edit_push_button_clicked)
        self.clients_hmo_view_policy_individual_edit_push_button.clicked.connect(self.on_clients_hmo_view_policy_individual_edit_push_button_clicked)
        self.clients_hmo_view_policy_corporate_edit_push_button.clicked.connect(self.on_clients_hmo_view_policy_corporate_edit_push_button_clicked)

        # client table row double click handlers
        self.clients_non_life_dashboard_table.cellDoubleClicked.connect(self.on_clients_non_life_dashboard_table_row_double_clicked)
        self.clients_hmo_dashboard_table.cellDoubleClicked.connect(self.on_clients_hmo_dashboard_table_cell_double_clicked)

        # update policy details button
        self.clients_non_life_view_policy_update_push_button.clicked.connect(self.on_clients_non_life_view_policy_update_push_button_clicked)
        self.clients_hmo_view_policy_individual_update_push_button.clicked.connect(self.on_clients_hmo_view_policy_individual_update_push_button_clicked)
        self.clients_hmo_view_policy_corporate_update_push_button.clicked.connect(self.on_clients_hmo_view_policy_corporate_update_push_button_clicked)

        # set selection behavior to rows
        self.clients_non_life_dashboard_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.clients_hmo_dashboard_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.archives_non_life_dashboard_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.archives_hmo_dashboard_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        # archive client buttons
        self.clients_non_life_dashboard_archive_button.clicked.connect(self.on_clients_non_life_dashboard_archive_button_clicked)
        self.clients_hmo_dashboard_archive_button.clicked.connect(self.on_clients_hmo_dashboard_archive_button_clicked)

        # record policy payment buttons
        self.clients_non_life_dashboard_record_payment_button.clicked.connect(self.on_clients_non_life_dashboard_record_payment_button_clicked)
        self.clients_hmo_dashboard_record_payment_button.clicked.connect(self.on_clients_hmo_dashboard_record_payment_button_clicked)
        
        # restore archive buttons
        self.archives_non_life_dashboard_restore_button.clicked.connect(self.on_archives_non_life_dashboard_restore_button_clicked)
        self.archives_hmo_dashboard_restore_button.clicked.connect(self.on_archives_hmo_dashboard_restore_button_clicked)

        # delete archive buttons
        self.archives_non_life_dashboard_delete_button.clicked.connect(self.on_archives_non_life_dashboard_delete_button_clicked)
        self.archives_hmo_dashboard_delete_button.clicked.connect(self.on_archives_hmo_dashboard_delete_button_clicked)

        # REVISE: move to separate functions later
        # resize cols to header/content
        self.archives_non_life_dashboard_table.resizeColumnsToContents()
        self.archives_non_life_dashboard_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.archives_hmo_dashboard_table.resizeColumnsToContents()
        self.archives_hmo_dashboard_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.clients_non_life_dashboard_table.resizeColumnsToContents()
        self.clients_non_life_dashboard_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.clients_hmo_dashboard_table.resizeColumnsToContents()
        self.clients_hmo_dashboard_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.companies_non_life_dashboard_table.resizeColumnsToContents()
        self.companies_non_life_dashboard_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.companies_hmo_dashboard_table.resizeColumnsToContents()
        self.companies_hmo_dashboard_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.client_payments_table.resizeColumnsToContents()
        self.client_payments_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.company_expenses_table.resizeColumnsToContents()
        self.company_expenses_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

        # sort data when header is clicked
        self.archives_non_life_dashboard_table.setSortingEnabled(True)
        self.archives_hmo_dashboard_table.setSortingEnabled(True)
        self.client_payments_table.setSortingEnabled(True)
        self.company_expenses_table.setSortingEnabled(True)
        self.clients_non_life_dashboard_table.setSortingEnabled(True)
        self.clients_hmo_dashboard_table.setSortingEnabled(True)
        
        # REVISE: move to separate functions later
        # display result count per table
        self.archives_non_life_dashboard_count.setText( str(self.archives_non_life_dashboard_table.rowCount()) )
        self.archives_hmo_dashboard_count.setText( str(self.archives_hmo_dashboard_table.rowCount()) )
        self.client_payments_count.setText( str(self.client_payments_table.rowCount()) )
        self.company_expenses_count.setText( str(self.company_expenses_table.rowCount()) )
        self.clients_hmo_dashboard_count.setText( str(self.clients_hmo_dashboard_table.rowCount()) )
        self.clients_non_life_dashboard_count.setText( str(self.clients_non_life_dashboard_table.rowCount()) )
        self.companies_hmo_dashboard_count.setText( str(self.companies_hmo_dashboard_table.rowCount()) )
        self.companies_non_life_dashboard_count.setText( str(self.companies_non_life_dashboard_table.rowCount()) )
    
        # edit account buttons
        self.account_edit_button.clicked.connect(self.enable_account_editing)
        self.account_save_button.clicked.connect(self.save_account_changes)

        # change password button
        self.change_password_button.clicked.connect(self.change_password)

        # export buttons
        self.export_clients_nonlife_csv_button.clicked.connect(self.export_clients_nonlife_to_csv)
        self.export_clients_nonlife_xls_button.clicked.connect(self.export_clients_nonlife_to_xls)
        self.export_clients_nonlife_pdf_button.clicked.connect(self.export_clients_nonlife_to_pdf)
        self.export_clients_hmo_individual_csv_button.clicked.connect(self.export_clients_hmo_individual_to_csv)
        self.export_clients_hmo_individual_xls_button.clicked.connect(self.export_clients_hmo_individual_to_xls)
        self.export_clients_hmo_individual_pdf_button.clicked.connect(self.export_clients_hmo_individual_to_pdf)
        #self.export_clients_nonlife_corporate_csv_button.clicked.connect(self.export_clients_nonlife_corporate_to_csv)
        #self.export_clients_nonlife_corporate_xls_button.clicked.connect(self.export_clients_nonlife_corporate_to_xls)
        #self.export_clients_nonlife_corporate_pdf_button.clicked.connect(self.export_clients_nonlife_corporate_to_pdf)
        #self.export_clients_hmo_corporate_csv_button.clicked.connect(self.export_clients_hmo_corporate_to_csv)
        #self.export_clients_hmo_corporate_xls_button.clicked.connect(self.export_clients_hmo_corporate_to_xls)
        #self.export_clients_hmo_corporate_pdf_button.clicked.connect(self.export_clients_hmo_corporate_to_pdf)


    #### Navigation Tab Button Functions
    def on_home_button_clicked(self):
        self.current_active_tab.setCurrentIndex(0)
        self.load_expiring_policies_grouped(self)

    def on_clients_button_clicked(self):
        self.current_active_tab.setCurrentIndex(1)
        db_func.fetch_client_table_data(self)

    def on_clients_non_life_dashboard_table_row_double_clicked(self, row, column):
        db_func.handle_nonlife_row_double_click(self, row, column)

    def on_clients_non_life_view_policy_edit_push_button_clicked(self):
        self.set_view_policy_fields_readonly(False)

    def on_clients_hmo_view_policy_individual_edit_push_button_clicked(self):
        self.set_hmo_individual_view_policy_fields_readonly(False)
    
    def on_clients_hmo_view_policy_corporate_edit_push_button_clicked(self):
        self.set_hmo_corporate_view_policy_fields_readonly(False)

    def on_clients_non_life_view_policy_update_push_button_clicked(self):
        db_func.update_nonlife_policy(self)

    def on_clients_hmo_view_policy_individual_update_push_button_clicked(self):
        db_func.update_hmo_individual_policy(self)
    
    def on_clients_hmo_view_policy_corporate_update_push_button_clicked(self):
        db_func.update_hmo_corporate_policy(self)

    def on_clients_non_life_add_client_submit_push_button_clicked(self):
        db_func.insert_nonlife_client(self)

    def on_clients_hmo_dashboard_table_cell_double_clicked(self, row, column):
        db_func.handle_hmo_row_double_click(self, row, column)

    def on_clients_hmo_add_client_individual_submit_push_button_clicked(self):
        db_func.insert_hmo_individual_client(self)

    def on_clients_hmo_add_client_corporate_submit_push_button_clicked(self):
        db_func.insert_hmo_corporate_client(self)

    def on_clients_non_life_dashboard_archive_button_clicked(self):
        db_func.archive_nonlife_client(self)

    def on_clients_non_life_dashboard_record_payment_button_clicked(self):
        db_func.record_policy_payment_nonlife(self)

    def on_clients_hmo_dashboard_archive_button_clicked(self):
        db_func.archive_hmo_client(self)
    
    def on_clients_hmo_dashboard_record_payment_button_clicked(self):
        db_func.record_policy_payment_hmo(self)
        
    def on_companies_button_clicked(self):
        self.current_active_tab.setCurrentIndex(2)
        db_func.fetch_company_table_data(self)
      
    def on_collection_button_clicked(self):
        self.current_active_tab.setCurrentIndex(3)
        db_func.fetch_all_client_payments(self)
      
    def on_archives_button_clicked(self):
        self.current_active_tab.setCurrentIndex(4)
        db_func.fetch_archive_table_data(self)

    def on_archives_non_life_dashboard_restore_button_clicked(self):
        db_func.restore_nonlife_client(self)

    def on_archives_hmo_dashboard_restore_button_clicked(self):
        db_func.restore_hmo_client(self)

    def on_archives_non_life_dashboard_delete_button_clicked(self):
        db_func.delete_nonlife_client(self)

    def on_archives_hmo_dashboard_delete_button_clicked(self):
        db_func.delete_hmo_client(self)

    def update_table_counts(self):
        """Update the result count labels for all tables based on visible rows."""
        try:
            # Archives tables
            if hasattr(self, 'archives_non_life_dashboard_table'):
                visible_archives_nonlife = sum(1 for row in range(self.archives_non_life_dashboard_table.rowCount()) 
                                             if not self.archives_non_life_dashboard_table.isRowHidden(row))
                self.archives_non_life_dashboard_count.setText(str(visible_archives_nonlife))
            
            if hasattr(self, 'archives_hmo_dashboard_table'):
                visible_archives_hmo = sum(1 for row in range(self.archives_hmo_dashboard_table.rowCount()) 
                                         if not self.archives_hmo_dashboard_table.isRowHidden(row))
                self.archives_hmo_dashboard_count.setText(str(visible_archives_hmo))
            
            # Client tables
            if hasattr(self, 'clients_non_life_dashboard_table'):
                visible_clients_nonlife = sum(1 for row in range(self.clients_non_life_dashboard_table.rowCount()) 
                                            if not self.clients_non_life_dashboard_table.isRowHidden(row))
                self.clients_non_life_dashboard_count.setText(str(visible_clients_nonlife))
            
            if hasattr(self, 'clients_hmo_dashboard_table'):
                visible_clients_hmo = sum(1 for row in range(self.clients_hmo_dashboard_table.rowCount()) 
                                        if not self.clients_hmo_dashboard_table.isRowHidden(row))
                self.clients_hmo_dashboard_count.setText(str(visible_clients_hmo))
            
            # Company tables
            if hasattr(self, 'companies_non_life_dashboard_table'):
                visible_companies_nonlife = sum(1 for row in range(self.companies_non_life_dashboard_table.rowCount()) 
                                              if not self.companies_non_life_dashboard_table.isRowHidden(row))
                self.companies_non_life_dashboard_count.setText(str(visible_companies_nonlife))
            
            if hasattr(self, 'companies_hmo_dashboard_table'):
                visible_companies_hmo = sum(1 for row in range(self.companies_hmo_dashboard_table.rowCount()) 
                                          if not self.companies_hmo_dashboard_table.isRowHidden(row))
                self.companies_hmo_dashboard_count.setText(str(visible_companies_hmo))
            
            # Collection tables
            if hasattr(self, 'client_payments_table'):
                visible_client_payments = sum(1 for row in range(self.client_payments_table.rowCount()) 
                                            if not self.client_payments_table.isRowHidden(row))
                self.client_payments_count.setText(str(visible_client_payments))
            
            if hasattr(self, 'company_expenses_table'):
                visible_company_expenses = sum(1 for row in range(self.company_expenses_table.rowCount()) 
                                             if not self.company_expenses_table.isRowHidden(row))
                self.company_expenses_count.setText(str(visible_company_expenses))
        except AttributeError as e:
            # Some tables might not be loaded yet
            pass

    def on_search_text_changed(self, text):
        """Filter visible table rows based on the search text."""
        # Get the sender widget to determine which search box triggered this
        sender = self.sender()
        
        # Determine the search text based on the current widget or sender
        if sender:
            text = sender.text().strip().lower()
        else:
            text = text.strip().lower()
            
        current_tab = self.current_active_tab.currentWidget()
        current_tab_index = self.current_active_tab.currentIndex()
        
        # Debug: Print current tab info
        print(f"Search triggered on tab index: {current_tab_index}")
        
        # If search text is empty, show all rows
        if not text:
            tables = current_tab.findChildren(QTableWidget)
            print(f"Clearing search - found {len(tables)} tables")
            for table in tables:
                for row in range(table.rowCount()):
                    table.setRowHidden(row, False)
            self.update_table_counts()
            return
        
        # Search through all tables in the current tab
        tables = current_tab.findChildren(QTableWidget)
        print(f"Searching '{text}' - found {len(tables)} tables")
        
        # If no tables found, return early (like home tab)
        if not tables:
            print("No tables found in current tab")
            return
            
        for table in tables:
            print(f"Searching table: {table.objectName()} with {table.rowCount()} rows")
            # Only search if table is visible and has data
            if table.isVisible() and table.rowCount() > 0:
                hidden_count = 0
                for row in range(table.rowCount()):
                    match = False
                    # Search through all columns for the text
                    for col in range(table.columnCount()):
                        item = table.item(row, col)
                        if item and item.text() and text in item.text().lower():
                            match = True
                            break
                    # Hide row if no match found
                    table.setRowHidden(row, not match)
                    if not match:
                        hidden_count += 1
                print(f"Hidden {hidden_count} rows in {table.objectName()}")
        
        # Update the counts after filtering
        self.update_table_counts()

    
    def on_account_button_clicked(self):
        self.current_active_tab.setCurrentIndex(5)
        db_func.load_user_account(self, self.current_username)
    
    def enable_account_editing(self):
        self.account_full_name_line_edit.setReadOnly(False)
        self.account_agent_number_line_edit.setReadOnly(False)
        self.account_email_line_edit.setReadOnly(False)
        self.account_contact_number_line_edit.setReadOnly(False)
        self.account_save_button.setEnabled(True)

    def save_account_changes(self):
        db_func.save_user_account(self, self.current_username)
        QMessageBox.information(self, "Saved", "Account updated.")
        self.account_save_button.setEnabled(False)
        self.account_full_name_line_edit.setReadOnly(True)
        self.account_agent_number_line_edit.setReadOnly(True)
        self.account_email_line_edit.setReadOnly(True)
        self.account_contact_number_line_edit.setReadOnly(True)
    
    def on_logout_button_clicked(self):
        self.login_window = LoginPage()
        self.login_window.show()
        self.close()

    def change_password(self):
        old_pass = self.account_old_password_line_edit.text()
        new_pass = self.account_new_password_line_edit.text()
        confirm_pass = self.account_confirm_password_line_edit.text()

        if not old_pass or not new_pass or not confirm_pass:
            QMessageBox.warning(self, "Missing Fields", "Please fill in all fields.")
            return

        if new_pass != confirm_pass:
            QMessageBox.warning(self, "Mismatch", "New passwords do not match.")
            return

        success = db_func.change_user_password(self.current_username, old_pass, new_pass)

        if success:
            QMessageBox.information(self, "Success", "Password changed successfully.")
            self.account_old_password_line_edit.clear()
            self.account_new_password_line_edit.clear()
            self.account_confirm_password_line_edit.clear()
        else:
            QMessageBox.critical(self, "Error", "Old password is incorrect.")

    def set_view_policy_fields_readonly(self, readonly=True):
        self.clients_non_life_view_policy_update_push_button.setEnabled(not readonly)

        # Make all fields read-only by default
        for widget in [
            self.clients_non_life_view_policy_assured_name_line_edit,
            self.clients_non_life_view_policy_contact_number_line_edit,
            self.clients_non_life_view_policy_email_line_edit,
            self.clients_non_life_view_policy_birthday_line_edit,
            self.clients_non_life_view_policy_inception_date_line_edit,
            self.clients_non_life_view_policy_expiry_date_line_edit,
            self.clients_non_life_view_policy_net_premium_line_edit,
            self.clients_non_life_view_policy_gross_premium_line_edit,
            self.clients_non_life_view_policy_policy_number_line_edit,
            self.clients_non_life_view_policy_agent_code_line_edit,
            self.clients_non_life_view_policy_payment_invoice_line_edit,
            self.clients_non_life_view_policy_commission_line_edit,
            self.clients_non_life_view_policy_insurance_company_line_edit,
            self.clients_non_life_view_policy_amount_covered_line_edit,
            self.clients_non_life_view_policy_notes_text_edit,
        ]:
            widget.setReadOnly(readonly)
        self.clients_non_life_view_policy_insurance_type_combo_box.setEnabled(not readonly)

    def set_hmo_individual_view_policy_fields_readonly(self, readonly=True):
        self.clients_hmo_view_policy_individual_update_push_button.setEnabled(not readonly)

        for widget in [
            self.clients_hmo_view_policy_individual_assured_name_line_edit,
            self.clients_hmo_view_policy_individual_contact_number_line_edit,
            self.clients_hmo_view_policy_individual_email_line_edit,
            self.clients_hmo_view_policy_individual_birthday_line_edit,
            self.clients_hmo_view_policy_individual_inception_date_line_edit,
            self.clients_hmo_view_policy_individual_expiry_date_line_edit,
            self.clients_hmo_view_policy_individual_agent_code_line_edit,
            self.clients_hmo_view_policy_individual_policy_number_line_edit,
            self.clients_hmo_view_policy_individual_mbl_abl_line_edit,
            self.clients_hmo_view_policy_individual_net_premium_line_edit,
            self.clients_hmo_view_policy_individual_gross_premium_line_edit,
            self.clients_hmo_view_policy_individual_commission_line_edit,
            self.clients_hmo_view_policy_individual_notes_text_edit,
            self.clients_hmo_view_policy_individual_hmo_company_line_edit,
        ]:
            widget.setReadOnly(readonly)

    def set_hmo_corporate_view_policy_fields_readonly(self, readonly=True):
        self.clients_hmo_view_policy_corporate_update_push_button.setEnabled(not readonly)

        for widget in [
            self.clients_hmo_view_policy_corporate_company_name_line_edit,
            self.clients_hmo_view_policy_corporate_contact_number_line_edit,
            self.clients_hmo_view_policy_corporate_email_line_edit,
            self.clients_hmo_view_policy_corporate_number_of_enrollees_line_edit,
            self.clients_hmo_view_policy_corporate_inception_date_line_edit,
            self.clients_hmo_view_policy_corporate_expiry_date_line_edit,
            self.clients_hmo_view_policy_corporate_agent_code_line_edit,
            self.clients_hmo_view_policy_corporate_policy_number_line_edit,
            self.clients_hmo_view_policy_corporate_mbl_abl_line_edit,
            self.clients_hmo_view_policy_corporate_net_premium_line_edit,
            self.clients_hmo_view_policy_corporate_gross_premium_line_edit,
            self.clients_hmo_view_policy_corporate_commission_line_edit,
            self.clients_hmo_view_policy_corporate_notes_text_edit,
            self.clients_hmo_view_policy_corporate_hmo_company_line_edit,
        ]:
            widget.setReadOnly(readonly)

    def create_section_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-weight: bold; font-size: 18px; margin-top: 20px; margin-bottom: 10px;")
        return label

    def create_notification_card(self, policy_number, client_name, expiry_date, color):
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border: 1px solid #aaa;
                border-radius: 6px;
                padding: 10px;
            }}
        """)
        frame_layout = QHBoxLayout(frame)

        days_left = (expiry_date - datetime.now().date()).days
        message = f"Policy number {policy_number} insured to {client_name} is about to expire on {expiry_date}."
        if days_left <= 0:
            message = f"Policy number {policy_number} insured to {client_name} expired on {expiry_date}."
        label = QLabel(message)
        label.setWordWrap(True)
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)  # stretch label horizontally

        dismiss_button = QPushButton("Dismiss")
        dismiss_button.setFixedWidth(80)
        dismiss_button.clicked.connect(lambda _, f=frame: f.setParent(None))

        frame_layout.addWidget(label)
        frame_layout.addStretch()
        frame_layout.addWidget(dismiss_button)

        return frame
    
    def load_expiring_policies_grouped(self, ui):
        try:
            conn = db_func.connect()
            cursor = conn.cursor()

            self.clear_notifications()

            queries = [
                # Non-Life
                """
                SELECT policy_number, assured_name AS client_name, expiry_date
                FROM clients_nonlife
                WHERE status = 'active'
                """,
                # HMO Individual
                """
                SELECT policy_number, assured_name AS client_name, expiry_date
                FROM clients_hmo_individual
                WHERE status = 'active'
                """,
                # HMO Corporate
                """
                SELECT policy_number, company_name AS client_name, expiry_date
                FROM clients_hmo_corporate
                WHERE status = 'active'
                """
            ]

            all_results = []
            for query in queries:
                cursor.execute(query)
                all_results.extend(cursor.fetchall())

            all_results.sort(key=lambda row: row[2])

            # Get layout inside notifications scroll area
            layout = ui.notifications_center.findChild(QWidget, "scrollAreaWidgetContents").layout()

            # Group policies
            grouped = {"Expired Policies": [], "This Week": [], "Next Week": [], "This Month": [], "Upcoming Months": []}

            for policy_number, client_name, expiry_date in all_results:
                days_left = (expiry_date - datetime.now().date()).days
                if days_left <= 0:
                    grouped["Expired Policies"].append((policy_number, client_name, expiry_date))
                elif days_left <= 7:
                    grouped["This Week"].append((policy_number, client_name, expiry_date))
                elif 8 <= days_left <= 14:
                    grouped["Next Week"].append((policy_number, client_name, expiry_date))
                elif 15 <= days_left <= 30:
                    grouped["This Month"].append((policy_number, client_name, expiry_date))
                else:
                    grouped["Upcoming Months"].append((policy_number, client_name, expiry_date))

            for category, items in grouped.items():
                if not items:
                    continue

                layout.addWidget(self.create_section_label(category))

                for policy_number, client_name, expiry_date in items:
                    color = {
                        "This Week": "#ffcccc",
                        "Next Week": "#fff0cc",
                        "This Month": "#e0f0ff"
                    }.get(category, "#ffffff")

                    card = self.create_notification_card(policy_number, client_name, expiry_date, color)
                    layout.addWidget(card)

            cursor.close()
            conn.close()

        except Exception as e:
            print("Error loading grouped notifications:", e)

    def clear_notifications(self):
        container = self.notifications_center.widget()
        if container is not None:
            layout = container.layout()
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
    
    def get_visible_row_ids(self, table_widget, id_column=0):
        ids = []
        for row in range(table_widget.rowCount()):
            if not table_widget.isRowHidden(row):
                item = table_widget.item(row, id_column)
                if item:
                    ids.append(item.text())
        return ids
    
    def export_clients_nonlife_to_csv(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save CSV", "clients-nonlife.csv", "CSV Files (*.csv)"
        )

        if not path:
            return  # User canceled

        try:
            #print("search for ids")
            ids = self.get_visible_row_ids(self.clients_non_life_dashboard_table, id_column=0)
            #print("Exporting the following client IDs:", ids)
            if not ids:
                QMessageBox.information(self, "No Data", "No visible rows to export.")
                return
            
            rows, headers = db_func.fetch_clients_nonlife_by_ids(ids)

            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(rows)

            QMessageBox.information(self, "Export Complete", f"CSV exported to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Export failed:\n{e}")
        
    def export_clients_nonlife_to_xls(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Excel File", "clients-nonlife.xlsx", "Excel Files (*.xlsx)"
        )

        if not path:
            return  # user canceled

        try:
            ids = self.get_visible_row_ids(self.clients_non_life_dashboard_table, id_column=0)
            if not ids:
                QMessageBox.information(self, "No Data", "No visible rows to export.")
                return
            
            rows, headers = db_func.fetch_clients_nonlife_by_ids(ids)

            wb = Workbook()
            ws = wb.active
            ws.title = "Clients"

            # Write headers
            ws.append(headers)

            # Write data rows
            for row in rows:
                ws.append(row)

            wb.save(path)
            QMessageBox.information(self, "Export Successful", f"Excel file saved:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", f"Error:\n{e}")
    
    def export_clients_nonlife_to_pdf(self):
        ids = self.get_visible_row_ids(self.clients_non_life_dashboard_table, id_column=0)
        if not ids:
            QMessageBox.information(self, "No Data", "No visible rows to export.")
            return
            
        rows, headers = db_func.fetch_clients_nonlife_by_ids(ids)
        
        export_columns = [
            ("Assured Name", "assured_name"),
            ("Contact No.", "contact_number"),
            ("Email", "email"),
            ("Type of Insurance", "type_of_insurance"),
            ("Insurance Company", "insurance_company"),
            ("Inception Date", "inception_date"),
            ("Expiry Date", "expiry_date"),
            ("Policy Number", "policy_number"),
            ("Gross Premium", "gross_premium"),
            ("Commission", "commission"),
            ("Coverage", "amount_covered"),
        ]

        # Map header to column index
        header_index_map = {header: i for i, header in enumerate(headers)}

        # Build filtered headers and data rows
        filtered_headers = [label for label, _ in export_columns]
        filtered_rows = [
            [row[header_index_map[col]] for _, col in export_columns]
            for row in rows
        ]

        path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF", "clients-nonlife.pdf", "PDF Files (*.pdf)"
        )

        if not path:
            return

        try:
            doc = SimpleDocTemplate(path, pagesize=landscape(A4))
            page_width, _ = landscape(A4)
            usable_width = page_width - 72  # 0.5 inch margins left & right
            col_width = usable_width / len(filtered_headers)
            col_widths = [col_width] * len(filtered_headers)

            styles = getSampleStyleSheet()
            cell_style = styles["BodyText"]
            cell_style.fontSize = 5
            cell_style.leading = 7

            table_data = [filtered_headers]
            for row in filtered_rows:
                table_data.append([Paragraph(str(cell), cell_style) for cell in row])

            table = Table(table_data, colWidths=col_widths, repeatRows=1)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 5),
                ('LEFTPADDING', (0, 0), (-1, -1), 2),
                ('RIGHTPADDING', (0, 0), (-1, -1), 2),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
            ]))

            elements = [
                Paragraph("Client HMO Individual", styles["Title"]),
                Spacer(1, 7),
                table
            ]
            doc.build(elements)

            QMessageBox.information(self, "Export Successful", f"PDF saved to:\n{path}")

        except Exception as e:
            QMessageBox.critical(self, "Export Failed", f"Error:\n{e}")

    def export_clients_hmo_individual_to_csv(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save CSV", "clients-hmo-ind.csv", "CSV Files (*.csv)"
        )

        if not path:
            return  # User canceled

        try:
            #print("search for ids")
            ids = self.get_visible_row_ids(self.clients_hmo_dashboard_table, id_column=0)
            #print("Exporting the following client IDs:", ids)
            if not ids:
                QMessageBox.information(self, "No Data", "No visible rows to export.")
                return
            
            rows, headers = db_func.fetch_clients_hmo_individual_by_ids(ids)

            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(rows)

            QMessageBox.information(self, "Export Complete", f"CSV exported to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Export failed:\n{e}")
        
    def export_clients_hmo_individual_to_xls(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Excel File", "clients-hmo-ind.xlsx", "Excel Files (*.xlsx)"
        )

        if not path:
            return  # user canceled

        try:
            ids = self.get_visible_row_ids(self.clients_hmo_dashboard_table, id_column=0)
            if not ids:
                QMessageBox.information(self, "No Data", "No visible rows to export.")
                return
            
            rows, headers = db_func.fetch_clients_hmo_individual_by_ids(ids)

            wb = Workbook()
            ws = wb.active
            ws.title = "Clients"

            # Write headers
            ws.append(headers)

            # Write data rows
            for row in rows:
                ws.append(row)

            wb.save(path)
            QMessageBox.information(self, "Export Successful", f"Excel file saved:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", f"Error:\n{e}")
    
    def export_clients_hmo_individual_to_pdf(self):
        ids = self.get_visible_row_ids(self.clients_hmo_dashboard_table, id_column=0)
        if not ids:
            QMessageBox.information(self, "No Data", "No visible rows to export.")
            return
        
        rows, headers = db_func.fetch_clients_hmo_individual_by_ids(ids)

        export_columns = [
            ("Assured Name", "assured_name"),
            ("Contact No.", "contact_number"),
            ("Email", "email"),
            ("HMO Company", "hmo_company"),
            ("Inception Date", "inception_date"),
            ("Expiry Date", "expiry_date"),
            ("Policy Number", "policy_number"),
            ("Gross Premium", "gross_premium"),
            ("Commission", "commission"),
        ]

        # Map header to column index
        header_index_map = {header: i for i, header in enumerate(headers)}

        # Build filtered headers and data rows
        filtered_headers = [label for label, _ in export_columns]
        filtered_rows = [
            [row[header_index_map[col]] for _, col in export_columns]
            for row in rows
        ]

        path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF", "clients-hmo-ind.pdf", "PDF Files (*.pdf)"
        )

        if not path:
            return

        try:
            doc = SimpleDocTemplate(path, pagesize=landscape(A4))
            page_width, _ = landscape(A4)
            usable_width = page_width - 72  # 0.5 inch margins left & right
            col_width = usable_width / len(filtered_headers)
            col_widths = [col_width] * len(filtered_headers)

            styles = getSampleStyleSheet()
            cell_style = styles["BodyText"]
            cell_style.fontSize = 5
            cell_style.leading = 7

            table_data = [filtered_headers]
            for row in filtered_rows:
                table_data.append([Paragraph(str(cell), cell_style) for cell in row])

            table = Table(table_data, colWidths=col_widths, repeatRows=1)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 5),
                ('LEFTPADDING', (0, 0), (-1, -1), 2),
                ('RIGHTPADDING', (0, 0), (-1, -1), 2),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
            ]))

            elements = [
                Paragraph("Client HMO Individual", styles["Title"]),
                Spacer(1, 7),
                table
            ]
            doc.build(elements)

            QMessageBox.information(self, "Export Successful", f"PDF saved to:\n{path}")

        except Exception as e:
            QMessageBox.critical(self, "Export Failed", f"Error:\n{e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec())
