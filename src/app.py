import os
import sys
import db_func
from PyQt6.QtWidgets import QApplication, QWidget, QHeaderView, QAbstractItemView
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

    def on_login(self):
        # username = self.login_username.text()
        # password = self.login_password.text()

        self.main_window = MainWindow()
        self.main_window.show()
        self.close()


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
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec())