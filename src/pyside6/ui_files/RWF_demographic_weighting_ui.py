# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RWF_demographic_weighting_ui.ui'
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
    QGridLayout, QHBoxLayout, QLabel, QSizePolicy,
    QSlider, QSpacerItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(330, 202)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(-30, 160, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.gridLayoutWidget = QWidget(Dialog)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 70, 301, 81))
        self.demographic_weighting_layout = QGridLayout(self.gridLayoutWidget)
        self.demographic_weighting_layout.setObjectName(u"demographic_weighting_layout")
        self.demographic_weighting_layout.setContentsMargins(0, 0, 0, 0)
        self.newborn_label = QLabel(self.gridLayoutWidget)
        self.newborn_label.setObjectName(u"newborn_label")

        self.demographic_weighting_layout.addWidget(self.newborn_label, 0, 0, 1, 1)

        self.elderly_slider = QSlider(self.gridLayoutWidget)
        self.elderly_slider.setObjectName(u"elderly_slider")
        self.elderly_slider.setMaximum(3)
        self.elderly_slider.setOrientation(Qt.Orientation.Horizontal)

        self.demographic_weighting_layout.addWidget(self.elderly_slider, 1, 1, 1, 1)

        self.elderly_label = QLabel(self.gridLayoutWidget)
        self.elderly_label.setObjectName(u"elderly_label")

        self.demographic_weighting_layout.addWidget(self.elderly_label, 1, 0, 1, 1)

        self.vulnerable_slider = QSlider(self.gridLayoutWidget)
        self.vulnerable_slider.setObjectName(u"vulnerable_slider")
        self.vulnerable_slider.setMaximum(3)
        self.vulnerable_slider.setOrientation(Qt.Orientation.Horizontal)

        self.demographic_weighting_layout.addWidget(self.vulnerable_slider, 2, 1, 1, 1)

        self.vulnerable_label = QLabel(self.gridLayoutWidget)
        self.vulnerable_label.setObjectName(u"vulnerable_label")

        self.demographic_weighting_layout.addWidget(self.vulnerable_label, 2, 0, 1, 1)

        self.newborn_slider = QSlider(self.gridLayoutWidget)
        self.newborn_slider.setObjectName(u"newborn_slider")
        self.newborn_slider.setMaximum(3)
        self.newborn_slider.setOrientation(Qt.Orientation.Horizontal)

        self.demographic_weighting_layout.addWidget(self.newborn_slider, 0, 1, 1, 1)

        self.horizontalLayoutWidget = QWidget(Dialog)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(70, 30, 243, 31))
        self.label_layout = QHBoxLayout(self.horizontalLayoutWidget)
        self.label_layout.setObjectName(u"label_layout")
        self.label_layout.setContentsMargins(0, 0, 0, 0)
        self.zero_label = QLabel(self.horizontalLayoutWidget)
        self.zero_label.setObjectName(u"zero_label")

        self.label_layout.addWidget(self.zero_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.label_layout.addItem(self.horizontalSpacer)

        self.low_label = QLabel(self.horizontalLayoutWidget)
        self.low_label.setObjectName(u"low_label")

        self.label_layout.addWidget(self.low_label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.label_layout.addItem(self.horizontalSpacer_2)

        self.medium_label = QLabel(self.horizontalLayoutWidget)
        self.medium_label.setObjectName(u"medium_label")

        self.label_layout.addWidget(self.medium_label)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.label_layout.addItem(self.horizontalSpacer_3)

        self.high_label = QLabel(self.horizontalLayoutWidget)
        self.high_label.setObjectName(u"high_label")

        self.label_layout.addWidget(self.high_label)

        self.title_label = QLabel(Dialog)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setGeometry(QRect(110, 10, 191, 20))

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Demographic weighting", None))
        self.newborn_label.setText(QCoreApplication.translate("Dialog", u"Newborn", None))
        self.elderly_label.setText(QCoreApplication.translate("Dialog", u"Elderly", None))
        self.vulnerable_label.setText(QCoreApplication.translate("Dialog", u"Vulnerable", None))
        self.zero_label.setText(QCoreApplication.translate("Dialog", u"Zero", None))
        self.low_label.setText(QCoreApplication.translate("Dialog", u"Low", None))
        self.medium_label.setText(QCoreApplication.translate("Dialog", u"Medium", None))
        self.high_label.setText(QCoreApplication.translate("Dialog", u"High", None))
        self.title_label.setText(QCoreApplication.translate("Dialog", u"Set demographic weighting", None))
    # retranslateUi

