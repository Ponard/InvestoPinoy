import os
import sys
import db_func
from PyQt6.QtWidgets import QApplication, QWidget, QHeaderView, QAbstractItemView, QMessageBox, QTableWidget
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
            self.main_window = MainWindow()
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
    def __init__(self):
        super().__init__()
        uic.loadUi("QtGUI/form.ui", self)
        self.showMaximized()
        
        # connect to DB
        db_func.connect()

        # connect button to function
        self.navigation_home_button.clicked.connect(self.on_home_button_clicked)
        self.navigation_clients_button.clicked.connect(self.on_clients_button_clicked)
        self.navigation_companies_button.clicked.connect(self.on_companies_button_clicked)
        self.navigation_collection_button.clicked.connect(self.on_collection_button_clicked)
        self.navigation_archives_button.clicked.connect(self.on_archives_button_clicked)
        self.navigation_logout_button.clicked.connect(self.on_logout_button_clicked)

        # connect search bar
        self.search_edit.textChanged.connect(self.on_search_text_changed)
        self.clients_search_edit.textChanged.connect(self.on_search_text_changed)
        self.clients_hmo_search_edit.textChanged.connect(self.on_search_text_changed)
        self.archives_search_edit.textChanged.connect(self.on_search_text_changed)
        self.archives_hmo_search_edit.textChanged.connect(self.on_search_text_changed)
        
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
        # Load collection data if db_func has the methods
        try:
            if hasattr(db_func, 'fetch_collection_table_data'):
                db_func.fetch_collection_table_data(self)
        except Exception as e:
            print(f"Error loading collection data: {e}")
      
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

    def on_logout_button_clicked(self):
        self.login_window = LoginPage()
        self.login_window.show()
        self.close()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec())