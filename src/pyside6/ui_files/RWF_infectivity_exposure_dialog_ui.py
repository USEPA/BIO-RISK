# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RWF_redesign_infectivity_exposure_dialog_ui.ui'
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
    QLabel, QSizePolicy, QSlider, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(311, 172)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(-70, 130, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.infectivity_slider = QSlider(Dialog)
        self.infectivity_slider.setObjectName(u"infectivity_slider")
        self.infectivity_slider.setGeometry(QRect(110, 70, 160, 18))
        self.infectivity_slider.setMaximum(2)
        self.infectivity_slider.setOrientation(Qt.Orientation.Horizontal)
        self.exposure_slider = QSlider(Dialog)
        self.exposure_slider.setObjectName(u"exposure_slider")
        self.exposure_slider.setGeometry(QRect(110, 100, 160, 18))
        self.exposure_slider.setMaximum(2)
        self.exposure_slider.setOrientation(Qt.Orientation.Horizontal)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 70, 71, 16))
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(30, 100, 49, 16))
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(70, 10, 191, 20))
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(110, 40, 49, 16))
        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(160, 40, 49, 16))
        self.label_6 = QLabel(Dialog)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(240, 40, 49, 16))

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Infectivity and exposure levels", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Infectivity", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Exposure", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Set infectivity and exposure levels", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Low", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Medium", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"High", None))
    # retranslateUi

