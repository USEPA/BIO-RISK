# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RWF_risk_classification_dialog_ui.ui'
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
    QDialogButtonBox, QFrame, QLabel, QLineEdit,
    QRadioButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(420, 259)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(70, 220, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(10, 20, 401, 141))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.riskPerUnitAreaRadioButton = QRadioButton(self.frame)
        self.riskPerUnitAreaRadioButton.setObjectName(u"riskPerUnitAreaRadioButton")
        self.riskPerUnitAreaRadioButton.setGeometry(QRect(20, 40, 221, 20))
        self.riskPerStructureTypeRadioButton = QRadioButton(self.frame)
        self.riskPerStructureTypeRadioButton.setObjectName(u"riskPerStructureTypeRadioButton")
        self.riskPerStructureTypeRadioButton.setGeometry(QRect(20, 10, 221, 20))
        self.individualStructureRiskRadioButton = QRadioButton(self.frame)
        self.individualStructureRiskRadioButton.setObjectName(u"individualStructureRiskRadioButton")
        self.individualStructureRiskRadioButton.setGeometry(QRect(20, 70, 221, 20))
        self.bandedRisk_checkbox = QCheckBox(self.frame)
        self.bandedRisk_checkbox.setObjectName(u"bandedRisk_checkbox")
        self.bandedRisk_checkbox.setGeometry(QRect(60, 100, 121, 20))
        self.bandedRisk_lineEdit = QLineEdit(self.frame)
        self.bandedRisk_lineEdit.setObjectName(u"bandedRisk_lineEdit")
        self.bandedRisk_lineEdit.setGeometry(QRect(160, 100, 51, 21))
        self.bandedRisk_label = QLabel(self.frame)
        self.bandedRisk_label.setObjectName(u"bandedRisk_label")
        self.bandedRisk_label.setGeometry(QRect(220, 100, 141, 16))
        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(10, 170, 401, 51))
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.geojson_checkbox = QCheckBox(self.frame_2)
        self.geojson_checkbox.setObjectName(u"geojson_checkbox")
        self.geojson_checkbox.setGeometry(QRect(10, 20, 161, 20))
        self.frame.raise_()
        self.buttonBox.raise_()
        self.frame_2.raise_()

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Risk type", None))
        self.riskPerUnitAreaRadioButton.setText(QCoreApplication.translate("Dialog", u"Average risk per size of structure", None))
        self.riskPerStructureTypeRadioButton.setText(QCoreApplication.translate("Dialog", u"Average risk per structure", None))
        self.individualStructureRiskRadioButton.setText(QCoreApplication.translate("Dialog", u"Local individual structure risk", None))
        self.bandedRisk_checkbox.setText(QCoreApplication.translate("Dialog", u"Banded risk", None))
        self.bandedRisk_label.setText(QCoreApplication.translate("Dialog", u"# of risk banks (max 20)", None))
        self.geojson_checkbox.setText(QCoreApplication.translate("Dialog", u"Geojson output layers", None))
    # retranslateUi

