# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ProjectListWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
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
    QLayout, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_widgetMain(object):
    def setupUi(self, widgetMain):
        if not widgetMain.objectName():
            widgetMain.setObjectName(u"widgetMain")
        widgetMain.resize(840, 96)
        widgetMain.setWindowOpacity(1.000000000000000)
        self.verticalLayout_2 = QVBoxLayout(widgetMain)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.favButton = QPushButton(widgetMain)
        self.favButton.setObjectName(u"favButton")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.favButton.sizePolicy().hasHeightForWidth())
        self.favButton.setSizePolicy(sizePolicy)
        icon1 = QIcon()
        icon1.addFile(u"icons/star.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.favButton.setIcon(icon1)
        self.favButton.setIconSize(QSize(24, 24))
        self.favButton.setFlat(True)

        self.horizontalLayout.addWidget(self.favButton)

        self.icon = QLabel(widgetMain)
        self.icon.setObjectName(u"icon")
        sizePolicy.setHeightForWidth(self.icon.sizePolicy().hasHeightForWidth())
        self.icon.setSizePolicy(sizePolicy)
        self.icon.setMinimumSize(QSize(68, 64))
        self.icon.setMaximumSize(QSize(68, 64))
        self.icon.setBaseSize(QSize(68, 64))
        self.icon.setTextInteractionFlags(Qt.NoTextInteraction)

        self.horizontalLayout.addWidget(self.icon)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.projectNameLabel = QLabel(widgetMain)
        self.projectNameLabel.setObjectName(u"projectNameLabel")
        self.projectNameLabel.setMaximumSize(QSize(16777215, 20))
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.projectNameLabel.setFont(font)

        self.verticalLayout.addWidget(self.projectNameLabel)

        self.tagLayout = QHBoxLayout()
        self.tagLayout.setObjectName(u"tagLayout")

        self.verticalLayout.addLayout(self.tagLayout)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.line = QFrame(widgetMain)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)


        self.retranslateUi(widgetMain)

        QMetaObject.connectSlotsByName(widgetMain)
    # setupUi

    def retranslateUi(self, widgetMain):
        widgetMain.setWindowTitle(QCoreApplication.translate("widgetMain", u"Form", None))
        self.favButton.setText("")
        self.icon.setText(QCoreApplication.translate("widgetMain", u"Image", None))
        self.projectNameLabel.setText(QCoreApplication.translate("widgetMain", u"Project name", None))
    # retranslateUi

