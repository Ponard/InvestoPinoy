from PyQt6.QtWidgets import QApplication, QWidget, QHeaderView
from PyQt6 import uic

import sys
import db_func


class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self = uic.loadUi("QtGUI/login.ui", self)
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
        self = uic.loadUi("QtGUI/form.ui", self)
        
        # connect to DB
        # db_func.connect()
        
        # connect button to function
        self.navigation_home_button.clicked.connect(self.on_home_button_clicked)
        self.navigation_clients_button.clicked.connect(self.on_clients_button_clicked)
        self.navigation_policies_button.clicked.connect(self.on_policies_button_clicked)
        self.navigation_companies_button.clicked.connect(self.on_companies_button_clicked)
        self.navigation_collection_button.clicked.connect(self.on_collection_button_clicked)
        self.navigation_archives_button.clicked.connect(self.on_archives_button_clicked)
        self.archived_policies_restore_button.clicked.connect(self.on_policies_restore_button_clicked)
        self.archived_policies_delete_button.clicked.connect(self.on_policies_delete_button_clicked)
        self.archived_clients_restore_button.clicked.connect(self.on_clients_restore_button_clicked)
        self.archived_clients_delete_button.clicked.connect(self.on_clients_delete_button_clicked)
        self.expired_bin_restore_button.clicked.connect(self.on_bin_restore_button_clicked)
        self.expired_bin_delete_button.clicked.connect(self.on_bin_delete_button_clicked)


        # REVISE: move to separate functions later
        # resize cols to header/content
        self.expired_bin_table.resizeColumnsToContents()
        self.expired_bin_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.archived_clients_table.resizeColumnsToContents()
        self.archived_clients_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.archived_policies_table.resizeColumnsToContents()
        self.archived_policies_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.client_payments_table.resizeColumnsToContents()
        self.client_payments_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.company_expenses_table.resizeColumnsToContents()
        self.company_expenses_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.commission_table.resizeColumnsToContents()
        self.commission_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        # sort data when header is clicked
        self.expired_bin_table.setSortingEnabled(True)
        self.archived_clients_table.setSortingEnabled(True)
        self.archived_policies_table.setSortingEnabled(True)
        self.client_payments_table.setSortingEnabled(True)
        self.company_expenses_table.setSortingEnabled(True)
        self.commission_table.setSortingEnabled(True)
        
        # REVISE: move to separate functions later
        # display result count per table
        self.expired_bin_count.setText( str(self.expired_bin_table.rowCount()) )
        self.archived_clients_count.setText( str(self.archived_clients_table.rowCount()) )
        self.archived_policies_count.setText( str(self.archived_policies_table.rowCount()) )
        self.client_payments_count.setText( str(self.client_payments_table.rowCount()) )
        self.company_expenses_count.setText( str(self.company_expenses_table.rowCount()) )
        self.commission_count.setText( str(self.commission_table.rowCount()) )
    
    
    #### Navigation Tab Button Functions
    def on_home_button_clicked(self):
        self.current_active_tab.setCurrentIndex(0)

    def on_clients_button_clicked(self):
        self.current_active_tab.setCurrentIndex(1)
      
    def on_policies_button_clicked(self):
        self.current_active_tab.setCurrentIndex(2)
      
    def on_companies_button_clicked(self):
        self.current_active_tab.setCurrentIndex(3)
      
    def on_collection_button_clicked(self):
        self.current_active_tab.setCurrentIndex(4)
      
    def on_archives_button_clicked(self):
        self.current_active_tab.setCurrentIndex(5)
    
    
    # function for archive button on View Client & Policy
    def on_archive_button_clicked(self):
        # check if self.current_active_tab index == Client
            # add to Archived Client db
        # check if self.current_active_tab index == Policy
            # add to Archived Policy db
            
        ## OR
        # have a bool in Original Client/Policy db
        # isArchived: True/False
        pass


    #### Archive Tab Functions
    def on_policies_restore_button_clicked(self):
        # send back to policy db
        pass
    
    def on_policies_delete_button_clicked(self):
        # send to bin
        pass
    
    def on_clients_restore_button_clicked(self):
        # send back to client db
        pass
    
    def on_clients_delete_button_clicked(self):
        # send to bin
        pass
    
    def on_bin_restore_button_clicked(self):
        # check if selected is Client/Policy before restoring
        pass
    
    def on_bin_delete_button_clicked(self):
        pass
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec())