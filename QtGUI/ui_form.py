# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QVBoxLayout, QWidget)

class Ui_InvestoPinoyGUI(object):
    def setupUi(self, InvestoPinoyGUI):
        if not InvestoPinoyGUI.objectName():
            InvestoPinoyGUI.setObjectName(u"InvestoPinoyGUI")
        InvestoPinoyGUI.resize(800, 600)
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(224, 222, 232, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        brush2 = QBrush(QColor(255, 255, 255, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Light, brush2)
        brush3 = QBrush(QColor(239, 238, 243, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush3)
        brush4 = QBrush(QColor(112, 111, 116, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush4)
        brush5 = QBrush(QColor(149, 148, 155, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush2)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush3)
        brush6 = QBrush(QColor(255, 255, 220, 255))
        brush6.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush6)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush)
        brush7 = QBrush(QColor(0, 0, 0, 127))
        brush7.setStyle(Qt.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush7)
#endif
        palette.setBrush(QPalette.Active, QPalette.Accent, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush6)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush7)
#endif
        palette.setBrush(QPalette.Inactive, QPalette.Accent, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush6)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush)
        brush8 = QBrush(QColor(112, 111, 116, 127))
        brush8.setStyle(Qt.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush8)
#endif
        palette.setBrush(QPalette.Disabled, QPalette.Accent, brush2)
        InvestoPinoyGUI.setPalette(palette)
        InvestoPinoyGUI.setWindowOpacity(1.000000000000000)
        self.horizontalLayout = QHBoxLayout(InvestoPinoyGUI)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.navigation_sidebar = QFrame(InvestoPinoyGUI)
        self.navigation_sidebar.setObjectName(u"navigation_sidebar")
        self.navigation_sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        self.navigation_sidebar.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.navigation_sidebar)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.navigation_sidebar)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"color: black;\n"
"font-weight: bold;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.navigation_home_button = QPushButton(self.navigation_sidebar)
        self.navigation_home_button.setObjectName(u"navigation_home_button")

        self.verticalLayout.addWidget(self.navigation_home_button)

        self.navigation_clients_button = QPushButton(self.navigation_sidebar)
        self.navigation_clients_button.setObjectName(u"navigation_clients_button")

        self.verticalLayout.addWidget(self.navigation_clients_button)

        self.navigation_policies_button = QPushButton(self.navigation_sidebar)
        self.navigation_policies_button.setObjectName(u"navigation_policies_button")

        self.verticalLayout.addWidget(self.navigation_policies_button)

        self.navigation_companies_button = QPushButton(self.navigation_sidebar)
        self.navigation_companies_button.setObjectName(u"navigation_companies_button")

        self.verticalLayout.addWidget(self.navigation_companies_button)

        self.navigation_collection_button = QPushButton(self.navigation_sidebar)
        self.navigation_collection_button.setObjectName(u"navigation_collection_button")

        self.verticalLayout.addWidget(self.navigation_collection_button)

        self.navigation_archives_button = QPushButton(self.navigation_sidebar)
        self.navigation_archives_button.setObjectName(u"navigation_archives_button")

        self.verticalLayout.addWidget(self.navigation_archives_button)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.navigation_account_button = QPushButton(self.navigation_sidebar)
        self.navigation_account_button.setObjectName(u"navigation_account_button")

        self.verticalLayout.addWidget(self.navigation_account_button)

        self.navigation_logout_button = QPushButton(self.navigation_sidebar)
        self.navigation_logout_button.setObjectName(u"navigation_logout_button")

        self.verticalLayout.addWidget(self.navigation_logout_button)


        self.horizontalLayout.addWidget(self.navigation_sidebar)

        self.current_active_tab = QStackedWidget(InvestoPinoyGUI)
        self.current_active_tab.setObjectName(u"current_active_tab")
        self.home_tab = QWidget()
        self.home_tab.setObjectName(u"home_tab")
        self.label_2 = QLabel(self.home_tab)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(250, 110, 191, 141))
        self.current_active_tab.addWidget(self.home_tab)
        self.clients_tab = QWidget()
        self.clients_tab.setObjectName(u"clients_tab")
        self.current_active_tab.addWidget(self.clients_tab)

        self.horizontalLayout.addWidget(self.current_active_tab)


        self.retranslateUi(InvestoPinoyGUI)

        self.current_active_tab.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(InvestoPinoyGUI)
    # setupUi

    def retranslateUi(self, InvestoPinoyGUI):
        InvestoPinoyGUI.setWindowTitle(QCoreApplication.translate("InvestoPinoyGUI", u"InvestoPinoy Insurance Management System", None))
        self.label.setText(QCoreApplication.translate("InvestoPinoyGUI", u"NAVIGATION", None))
        self.navigation_home_button.setText(QCoreApplication.translate("InvestoPinoyGUI", u"Home", None))
        self.navigation_clients_button.setText(QCoreApplication.translate("InvestoPinoyGUI", u"Clients", None))
        self.navigation_policies_button.setText(QCoreApplication.translate("InvestoPinoyGUI", u"Policies", None))
        self.navigation_companies_button.setText(QCoreApplication.translate("InvestoPinoyGUI", u"Companies", None))
        self.navigation_collection_button.setText(QCoreApplication.translate("InvestoPinoyGUI", u"Collection", None))
        self.navigation_archives_button.setText(QCoreApplication.translate("InvestoPinoyGUI", u"Archives", None))
        self.navigation_account_button.setText(QCoreApplication.translate("InvestoPinoyGUI", u"Account", None))
        self.navigation_logout_button.setText(QCoreApplication.translate("InvestoPinoyGUI", u"Log out", None))
        self.label_2.setText(QCoreApplication.translate("InvestoPinoyGUI", u"Welcome to InvestoPinoy\u00ae", None))
    # retranslateUi

