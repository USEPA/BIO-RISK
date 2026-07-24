# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RWF_coordinate_box_dialog_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QLineEdit, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(542, 152)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(190, 120, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.longMin_lineEdit = QLineEdit(Dialog)
        self.longMin_lineEdit.setObjectName(u"longMin_lineEdit")
        self.longMin_lineEdit.setGeometry(QRect(370, 50, 161, 21))
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 50, 81, 16))
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(0, 80, 71, 16))
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(280, 50, 81, 16))
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(280, 80, 81, 16))
        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(180, 10, 301, 20))
        self.latMin_lineEdit = QLineEdit(Dialog)
        self.latMin_lineEdit.setObjectName(u"latMin_lineEdit")
        self.latMin_lineEdit.setGeometry(QRect(80, 50, 161, 21))
        self.longMax_lineEdit = QLineEdit(Dialog)
        self.longMax_lineEdit.setObjectName(u"longMax_lineEdit")
        self.longMax_lineEdit.setGeometry(QRect(370, 80, 161, 21))
        self.latMax_lineEdit = QLineEdit(Dialog)
        self.latMax_lineEdit.setObjectName(u"latMax_lineEdit")
        self.latMax_lineEdit.setGeometry(QRect(80, 80, 161, 21))

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Coordinate box selection", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Latitude Min", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Latitude Max", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Longitude Min", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Longitude Max", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Manually adjust region of interest", None))
    # retranslateUi

