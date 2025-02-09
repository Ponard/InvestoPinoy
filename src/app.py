from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6 import uic

import sys

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
      self.navigation_home_button.clicked.connect(self.on_home_button_clicked)
      self.navigation_clients_button.clicked.connect(self.on_clients_button_clicked)

   def on_home_button_clicked(self):
      self.current_active_tab.setCurrentIndex(0)

   def on_clients_button_clicked(self):
      self.current_active_tab.setCurrentIndex(1)
   
if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec())