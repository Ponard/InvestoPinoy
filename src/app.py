import os
import sys
import db_func
from PyQt6.QtWidgets import QApplication, QWidget, QHeaderView
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
        self.navigation_policies_button.clicked.connect(self.on_policies_button_clicked)
        self.navigation_companies_button.clicked.connect(self.on_companies_button_clicked)
        self.navigation_collection_button.clicked.connect(self.on_collection_button_clicked)
        self.navigation_archives_button.clicked.connect(self.on_archives_button_clicked)
        self.archived_policies_restore_button.clicked.connect(self.on_policies_restore_button_clicked)
        self.archived_policies_delete_button.clicked.connect(self.on_policies_delete_button_clicked)
        self.archived_clients_restore_button.clicked.connect(self.on_clients_restore_button_clicked)
        self.archived_clients_delete_button.clicked.connect(self.on_clients_delete_button_clicked)
        self.clients_non_life_add_client_submit_push_button.clicked.connect(self.on_clients_non_life_add_client_submit_push_button_clicked)


        # REVISE: move to separate functions later
        # resize cols to header/content
        self.archived_clients_table.resizeColumnsToContents()
        self.archived_clients_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.archived_policies_table.resizeColumnsToContents()
        self.archived_policies_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
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
        self.commission_table.resizeColumnsToContents()
        self.commission_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.policies_non_life_dashboard_table.resizeColumnsToContents()
        self.policies_non_life_dashboard_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.policies_hmo_dashboard_table.resizeColumnsToContents()
        self.policies_hmo_dashboard_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        # sort data when header is clicked
        self.archived_clients_table.setSortingEnabled(True)
        self.archived_policies_table.setSortingEnabled(True)
        self.client_payments_table.setSortingEnabled(True)
        self.company_expenses_table.setSortingEnabled(True)
        self.commission_table.setSortingEnabled(True)
        
        # REVISE: move to separate functions later
        # display result count per table
        self.archived_clients_count.setText( str(self.archived_clients_table.rowCount()) )
        self.archived_policies_count.setText( str(self.archived_policies_table.rowCount()) )
        self.client_payments_count.setText( str(self.client_payments_table.rowCount()) )
        self.company_expenses_count.setText( str(self.company_expenses_table.rowCount()) )
        self.commission_count.setText( str(self.commission_table.rowCount()) )
        self.clients_hmo_dashboard_count.setText( str(self.clients_hmo_dashboard_table.rowCount()) )
        self.clients_non_life_dashboard_count.setText( str(self.clients_non_life_dashboard_table.rowCount()) )
        self.companies_hmo_dashboard_count.setText( str(self.companies_hmo_dashboard_table.rowCount()) )
        self.companies_non_life_dashboard_count.setText( str(self.companies_non_life_dashboard_table.rowCount()) )
        self.policies_hmo_dashboard_count.setText( str(self.policies_hmo_dashboard_table.rowCount()) )
        self.policies_non_life_dashboard_count.setText( str(self.policies_non_life_dashboard_table.rowCount()) )
    
    
    #### Navigation Tab Button Functions
    def on_home_button_clicked(self):
        self.current_active_tab.setCurrentIndex(0)

    def on_clients_button_clicked(self):
        self.current_active_tab.setCurrentIndex(1)
        db_func.fetch_nonlife_clients(self)
    
    def on_clients_non_life_add_client_submit_push_button_clicked(self):
        db_func.insert_nonlife_client(self)

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
        current_table_widget = None
        current_table_db = None
        
        # check if current tab is Client/Policy
        # NOTE: Tables for Client/Policy currently doesn't exist
        # so this might give an error for now
        # but this will work correctly when the tables are made, already tested
        if self.current_active_tab.currentIndex() == 1:
            current_table_widget = self.clients_table
            current_table_db = "public.clients"
        elif self.current_active_tab.currentIndex() == 2:
            current_table_widget = self.policies_table
            current_table_db = "public.policies"
            
        # NOTE: need bool in Original Client/Policy db
        # isArchived: True/False
        selected_rows = set(index.row() for index in current_table_widget.selectedIndexes())
  
        for row in selected_rows:
            formatted_data = self.format_data(current_table_widget, row)
            merged_dict = {"old" : {**formatted_data, "isArchived" : False},
                           "new" : {**formatted_data, "isArchived" : True}
                        }
            db_func.update_row( current_table_db, **merged_dict )


    #### Archive Tab Functions
    def on_policies_restore_button_clicked(self):
        current_table_db = "public.policies"
        
        # send back to policy db
        selected_rows = set(index.row() for index in self.archived_policies_table.selectedIndexes())
  
        for row in selected_rows:
            formatted_data = self.format_data(self.archived_policies_table, row)
            merged_dict = {"old" : {**formatted_data, "isArchived" : True},
                           "new" : {**formatted_data, "isArchived" : False}
                        }
            db_func.update_row( current_table_db, **merged_dict )
    
    def on_policies_delete_button_clicked(self):
        current_table_db = "public.policies"
        
        selected_rows = set(index.row() for index in self.archived_policies_table.selectedIndexes())
  
        for row in selected_rows:
            db_func.delete_row( current_table_db, **self.format_data(self.archived_policies_table, row) )

    def on_clients_restore_button_clicked(self):
        # current_table_db = "public.clients"
        current_table_db = "public.test" # NOTE: For test, to remove
        
        
        
        # send back to client db
        selected_rows = set(index.row() for index in self.archived_clients_table.selectedIndexes())
  
        for row in selected_rows:
            formatted_data = self.format_data(self.archived_clients_table, row)
            merged_dict = {"old" : {**formatted_data, "isArchived" : True},
                           "new" : {**formatted_data, "isArchived" : False}
                        }
            db_func.update_row( current_table_db, **merged_dict )
    
    def on_clients_delete_button_clicked(self):
        current_table_db = "public.clients"
        
        selected_rows = set(index.row() for index in self.archived_clients_table.selectedIndexes())
        
        for row in selected_rows:
            db_func.delete_row( current_table_db, **self.format_data(self.archived_clients_table, row) )
    
    
    #### General functions
    # format tablewidget row to dict
    def format_data (self, table_widget, selected_row):
        formatted_data = {}
        
        # get text for each cell in a row
        for col in range(table_widget.columnCount()):
            data = table_widget.item(selected_row, col)
            formatted_data[table_widget.horizontalHeaderItem(col).text()] = data.text()
        
        return formatted_data
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec())