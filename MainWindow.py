# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_2022-07-22.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QToolButton, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(875, 590)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet(u"")
        self.actionNew_from_template = QAction(MainWindow)
        self.actionNew_from_template.setObjectName(u"actionNew_from_template")
        icon = QIcon()
        icon.addFile(u"icons/file-plus.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionNew_from_template.setIcon(icon)
        self.actionRemove_selected_project = QAction(MainWindow)
        self.actionRemove_selected_project.setObjectName(u"actionRemove_selected_project")
        icon1 = QIcon()
        icon1.addFile(u"icons/file-minus.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionRemove_selected_project.setIcon(icon1)
        self.actionRename_selected_project = QAction(MainWindow)
        self.actionRename_selected_project.setObjectName(u"actionRename_selected_project")
        icon2 = QIcon()
        icon2.addFile(u"icons/edit-3.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionRename_selected_project.setIcon(icon2)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        icon3 = QIcon()
        icon3.addFile(u"icons/x-square.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionExit.setIcon(icon3)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.projectsListView = QListWidget(self.centralwidget)
        self.projectsListView.setObjectName(u"projectsListView")
        self.projectsListView.setMinimumSize(QSize(0, 350))
        self.projectsListView.setStyleSheet(u"")

        self.gridLayout.addWidget(self.projectsListView, 2, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.categoriesLabel = QLabel(self.centralwidget)
        self.categoriesLabel.setObjectName(u"categoriesLabel")
        font = QFont()
        font.setBold(True)
        self.categoriesLabel.setFont(font)
        self.categoriesLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.categoriesLabel)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.addCategoryButton = QToolButton(self.centralwidget)
        self.addCategoryButton.setObjectName(u"addCategoryButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.addCategoryButton.sizePolicy().hasHeightForWidth())
        self.addCategoryButton.setSizePolicy(sizePolicy1)
        icon4 = QIcon()
        icon4.addFile(u"icons/plus.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.addCategoryButton.setIcon(icon4)
        self.addCategoryButton.setIconSize(QSize(24, 24))
        self.addCategoryButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.verticalLayout_3.addWidget(self.addCategoryButton)

        self.renameCategoryButton = QToolButton(self.centralwidget)
        self.renameCategoryButton.setObjectName(u"renameCategoryButton")
        sizePolicy1.setHeightForWidth(self.renameCategoryButton.sizePolicy().hasHeightForWidth())
        self.renameCategoryButton.setSizePolicy(sizePolicy1)
        self.renameCategoryButton.setIcon(icon2)
        self.renameCategoryButton.setIconSize(QSize(24, 24))
        self.renameCategoryButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.verticalLayout_3.addWidget(self.renameCategoryButton)

        self.removeCategoryButton = QToolButton(self.centralwidget)
        self.removeCategoryButton.setObjectName(u"removeCategoryButton")
        sizePolicy1.setHeightForWidth(self.removeCategoryButton.sizePolicy().hasHeightForWidth())
        self.removeCategoryButton.setSizePolicy(sizePolicy1)
        icon5 = QIcon()
        icon5.addFile(u"icons/minus.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.removeCategoryButton.setIcon(icon5)
        self.removeCategoryButton.setIconSize(QSize(24, 24))
        self.removeCategoryButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.verticalLayout_3.addWidget(self.removeCategoryButton)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.categoriesListView = QListWidget(self.centralwidget)
        self.categoriesListView.setObjectName(u"categoriesListView")

        self.horizontalLayout_2.addWidget(self.categoriesListView)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 875, 22))
        self.menuProject = QMenu(self.menuBar)
        self.menuProject.setObjectName(u"menuProject")
        self.menuProgram = QMenu(self.menuBar)
        self.menuProgram.setObjectName(u"menuProgram")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuProgram.menuAction())
        self.menuBar.addAction(self.menuProject.menuAction())
        self.menuProject.addAction(self.actionNew_from_template)
        self.menuProject.addAction(self.actionRename_selected_project)
        self.menuProject.addAction(self.actionRemove_selected_project)
        self.menuProgram.addAction(self.actionExit)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionNew_from_template.setText(QCoreApplication.translate("MainWindow", u"New from template", None))
        self.actionRemove_selected_project.setText(QCoreApplication.translate("MainWindow", u"Remove selected project", None))
        self.actionRename_selected_project.setText(QCoreApplication.translate("MainWindow", u"Rename selected project", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.categoriesLabel.setText(QCoreApplication.translate("MainWindow", u"Categories", None))
        self.addCategoryButton.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.renameCategoryButton.setText(QCoreApplication.translate("MainWindow", u"Rename", None))
        self.removeCategoryButton.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.menuProject.setTitle(QCoreApplication.translate("MainWindow", u"Project", None))
        self.menuProgram.setTitle(QCoreApplication.translate("MainWindow", u"Program", None))
    # retranslateUi

