# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RWF_main_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QProgressBar, QPushButton, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(984, 628)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(0, 0))
        self.actionDemographic_weighting = QAction(MainWindow)
        self.actionDemographic_weighting.setObjectName(u"actionDemographic_weighting")
        self.actionLocation_weighting = QAction(MainWindow)
        self.actionLocation_weighting.setObjectName(u"actionLocation_weighting")
        self.actionInfectivity_exposure_weighting = QAction(MainWindow)
        self.actionInfectivity_exposure_weighting.setObjectName(u"actionInfectivity_exposure_weighting")
        self.actionOutput_format = QAction(MainWindow)
        self.actionOutput_format.setObjectName(u"actionOutput_format")
        self.actionQuick_user_instructions = QAction(MainWindow)
        self.actionQuick_user_instructions.setObjectName(u"actionQuick_user_instructions")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 941, 551))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.verticalLayoutWidget)
        self.frame.setObjectName(u"frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy1)
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.mapView = QWebEngineView(self.frame)
        self.mapView.setObjectName(u"mapView")
        self.mapView.setGeometry(QRect(0, 10, 991, 471))
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.mapView.sizePolicy().hasHeightForWidth())
        self.mapView.setSizePolicy(sizePolicy2)
        self.mapView.setUrl(QUrl(u"about:blank"))
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(10, 350, 161, 131))
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.resetMapButton = QPushButton(self.frame_2)
        self.resetMapButton.setObjectName(u"resetMapButton")
        self.resetMapButton.setGeometry(QRect(10, 10, 141, 31))
        self.confirmBoundingBoxButton = QPushButton(self.frame_2)
        self.confirmBoundingBoxButton.setObjectName(u"confirmBoundingBoxButton")
        self.confirmBoundingBoxButton.setGeometry(QRect(10, 50, 141, 31))
        self.confirmBoundingBoxButton_2 = QPushButton(self.frame_2)
        self.confirmBoundingBoxButton_2.setObjectName(u"confirmBoundingBoxButton_2")
        self.confirmBoundingBoxButton_2.setGeometry(QRect(10, 90, 141, 31))

        self.verticalLayout.addWidget(self.frame)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.outputFolderLineEdit = QLineEdit(self.verticalLayoutWidget)
        self.outputFolderLineEdit.setObjectName(u"outputFolderLineEdit")

        self.gridLayout_3.addWidget(self.outputFolderLineEdit, 4, 2, 1, 1)

        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 3, 1, 1, 1)

        self.selectOutputFolderPushButton = QPushButton(self.verticalLayoutWidget)
        self.selectOutputFolderPushButton.setObjectName(u"selectOutputFolderPushButton")

        self.gridLayout_3.addWidget(self.selectOutputFolderPushButton, 4, 1, 1, 1)

        self.progress_label = QLabel(self.verticalLayoutWidget)
        self.progress_label.setObjectName(u"progress_label")

        self.gridLayout_3.addWidget(self.progress_label, 3, 3, 1, 1)

        self.progressBar = QProgressBar(self.verticalLayoutWidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.gridLayout_3.addWidget(self.progressBar, 3, 2, 1, 1)

        self.openFolderButton = QPushButton(self.verticalLayoutWidget)
        self.openFolderButton.setObjectName(u"openFolderButton")

        self.gridLayout_3.addWidget(self.openFolderButton, 4, 3, 1, 1)

        self.runButton = QPushButton(self.verticalLayoutWidget)
        self.runButton.setObjectName(u"runButton")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.runButton.sizePolicy().hasHeightForWidth())
        self.runButton.setSizePolicy(sizePolicy3)

        self.gridLayout_3.addWidget(self.runButton, 2, 0, 4, 1)


        self.verticalLayout.addLayout(self.gridLayout_3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 984, 33))
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        self.menuInfo = QMenu(self.menubar)
        self.menuInfo.setObjectName(u"menuInfo")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuInfo.menuAction())
        self.menuSettings.addAction(self.actionDemographic_weighting)
        self.menuSettings.addAction(self.actionLocation_weighting)
        self.menuSettings.addAction(self.actionInfectivity_exposure_weighting)
        self.menuSettings.addAction(self.actionOutput_format)
        self.menuInfo.addAction(self.actionQuick_user_instructions)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionDemographic_weighting.setText(QCoreApplication.translate("MainWindow", u"Demographic weighting", None))
        self.actionLocation_weighting.setText(QCoreApplication.translate("MainWindow", u"Location weighting", None))
        self.actionInfectivity_exposure_weighting.setText(QCoreApplication.translate("MainWindow", u"Infectivity/exposure weighting", None))
        self.actionOutput_format.setText(QCoreApplication.translate("MainWindow", u"Output format", None))
        self.actionQuick_user_instructions.setText(QCoreApplication.translate("MainWindow", u"Quick user instructions", None))
        self.resetMapButton.setText(QCoreApplication.translate("MainWindow", u"Reset map", None))
        self.confirmBoundingBoxButton.setText(QCoreApplication.translate("MainWindow", u"Confirm coordinates", None))
        self.confirmBoundingBoxButton_2.setText(QCoreApplication.translate("MainWindow", u"View/edit coordinates ", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Analysis progress", None))
        self.selectOutputFolderPushButton.setText(QCoreApplication.translate("MainWindow", u"Select output folder", None))
        self.progress_label.setText(QCoreApplication.translate("MainWindow", u"Idle", None))
        self.openFolderButton.setText(QCoreApplication.translate("MainWindow", u"Open folder", None))
        self.runButton.setText(QCoreApplication.translate("MainWindow", u"Run (select coordinates)", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.menuInfo.setTitle(QCoreApplication.translate("MainWindow", u"Info", None))
    # retranslateUi

