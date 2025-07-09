import os
import sys
import db_func
from PyQt6.QtWidgets import QApplication, QWidget, QHeaderView, QAbstractItemView, QMessageBox
from PyQt6.QtCore import QMetaObject
from PyQt6 import uic

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

        # connect button to function
        self.navigation_home_button.clicked.connect(self.on_home_button_clicked)
        self.navigation_clients_button.clicked.connect(self.on_clients_button_clicked)
        self.navigation_companies_button.clicked.connect(self.on_companies_button_clicked)
        self.navigation_collection_button.clicked.connect(self.on_collection_button_clicked)
        self.navigation_archives_button.clicked.connect(self.on_archives_button_clicked)
        self.navigation_account_button.clicked.connect(self.on_account_button_clicked)
        self.navigation_logout_button.clicked.connect(self.on_logout_button_clicked)
        
        # add client buttons
        self.clients_non_life_add_client_submit_push_button.clicked.connect(self.on_clients_non_life_add_client_submit_push_button_clicked)
        self.clients_hmo_add_client_individual_submit_push_button.clicked.connect(self.on_clients_hmo_add_client_individual_submit_push_button_clicked)
        self.clients_hmo_add_client_corporate_submit_push_button.clicked.connect(self.on_clients_hmo_add_client_corporate_submit_push_button_clicked)

        # set selection behavior to rows
        self.clients_non_life_dashboard_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.clients_hmo_dashboard_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.archives_non_life_dashboard_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.archives_hmo_dashboard_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        # archive client buttons
        self.clients_non_life_dashboard_archive_button.clicked.connect(self.on_clients_non_life_dashboard_archive_button_clicked)
        self.clients_hmo_dashboard_archive_button.clicked.connect(self.on_clients_hmo_dashboard_archive_button_clicked)
        
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


    #### Navigation Tab Button Functions
    def on_home_button_clicked(self):
        self.current_active_tab.setCurrentIndex(0)

    def on_clients_button_clicked(self):
        self.current_active_tab.setCurrentIndex(1)
        db_func.fetch_client_table_data(self)
    
    def on_clients_non_life_add_client_submit_push_button_clicked(self):
        db_func.insert_nonlife_client(self)

    def on_clients_hmo_add_client_individual_submit_push_button_clicked(self):
        db_func.insert_hmo_individual_client(self)

    def on_clients_hmo_add_client_corporate_submit_push_button_clicked(self):
        db_func.insert_hmo_corporate_client(self)

    def on_clients_non_life_dashboard_archive_button_clicked(self):
        db_func.archive_nonlife_client(self)

    def on_clients_hmo_dashboard_archive_button_clicked(self):
        db_func.archive_hmo_client(self)
      
    def on_companies_button_clicked(self):
        self.current_active_tab.setCurrentIndex(2)
        db_func.fetch_company_table_data(self)
      
    def on_collection_button_clicked(self):
        self.current_active_tab.setCurrentIndex(3)
      
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

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec())