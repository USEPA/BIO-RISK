# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RWF_redesign_output_format_dialog_ui.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QLabel, QLineEdit, QSizePolicy,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(357, 155)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(-10, 110, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.bandedRisk_checkbox = QCheckBox(Dialog)
        self.bandedRisk_checkbox.setObjectName(u"bandedRisk_checkbox")
        self.bandedRisk_checkbox.setGeometry(QRect(30, 40, 121, 20))
        self.geojson_checkbox = QCheckBox(Dialog)
        self.geojson_checkbox.setObjectName(u"geojson_checkbox")
        self.geojson_checkbox.setGeometry(QRect(30, 80, 161, 20))
        self.bandedRisk_lineEdit = QLineEdit(Dialog)
        self.bandedRisk_lineEdit.setObjectName(u"bandedRisk_lineEdit")
        self.bandedRisk_lineEdit.setGeometry(QRect(140, 40, 51, 21))
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(200, 40, 141, 16))
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(130, 10, 131, 20))

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Output format", None))
        self.bandedRisk_checkbox.setText(QCoreApplication.translate("Dialog", u"Banded risk", None))
        self.geojson_checkbox.setText(QCoreApplication.translate("Dialog", u"Geojson output layers", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"# of risk banks (max 20)", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Choose output format", None))
    # retranslateUi

