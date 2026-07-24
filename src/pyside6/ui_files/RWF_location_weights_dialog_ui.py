# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RWF_location_weights_dialog_ui.ui'
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
        Dialog.resize(377, 416)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(20, 380, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.gridLayoutWidget = QWidget(Dialog)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(20, 60, 341, 311))
        self.location_weighting_layout = QGridLayout(self.gridLayoutWidget)
        self.location_weighting_layout.setObjectName(u"location_weighting_layout")
        self.location_weighting_layout.setContentsMargins(0, 0, 0, 0)
        self.park_label = QLabel(self.gridLayoutWidget)
        self.park_label.setObjectName(u"park_label")

        self.location_weighting_layout.addWidget(self.park_label, 16, 0, 1, 1)

        self.primary_road_slider = QSlider(self.gridLayoutWidget)
        self.primary_road_slider.setObjectName(u"primary_road_slider")
        self.primary_road_slider.setMaximum(10)
        self.primary_road_slider.setOrientation(Qt.Orientation.Horizontal)

        self.location_weighting_layout.addWidget(self.primary_road_slider, 13, 1, 1, 1)

        self.secondary_road_slider = QSlider(self.gridLayoutWidget)
        self.secondary_road_slider.setObjectName(u"secondary_road_slider")
        self.secondary_road_slider.setMaximum(10)
        self.secondary_road_slider.setOrientation(Qt.Orientation.Horizontal)

        self.location_weighting_layout.addWidget(self.secondary_road_slider, 14, 1, 1, 1)

        self.commercial_slider = QSlider(self.gridLayoutWidget)
        self.commercial_slider.setObjectName(u"commercial_slider")
        self.commercial_slider.setMaximum(10)
        self.commercial_slider.setOrientation(Qt.Orientation.Horizontal)

        self.location_weighting_layout.addWidget(self.commercial_slider, 9, 1, 1, 1)

        self.primary_road_label = QLabel(self.gridLayoutWidget)
        self.primary_road_label.setObjectName(u"primary_road_label")

        self.location_weighting_layout.addWidget(self.primary_road_label, 13, 0, 1, 1)

        self.agricultural_slider = QSlider(self.gridLayoutWidget)
        self.agricultural_slider.setObjectName(u"agricultural_slider")
        self.agricultural_slider.setMaximum(10)
        self.agricultural_slider.setOrientation(Qt.Orientation.Horizontal)

        self.location_weighting_layout.addWidget(self.agricultural_slider, 6, 1, 1, 1)

        self.industrial_slider = QSlider(self.gridLayoutWidget)
        self.industrial_slider.setObjectName(u"industrial_slider")
        self.industrial_slider.setMaximum(10)
        self.industrial_slider.setOrientation(Qt.Orientation.Horizontal)

        self.location_weighting_layout.addWidget(self.industrial_slider, 8, 1, 1, 1)

        self.local_road_label = QLabel(self.gridLayoutWidget)
        self.local_road_label.setObjectName(u"local_road_label")

        self.location_weighting_layout.addWidget(self.local_road_label, 15, 0, 1, 1)

        self.residential_label = QLabel(self.gridLayoutWidget)
        self.residential_label.setObjectName(u"residential_label")

        self.location_weighting_layout.addWidget(self.residential_label, 5, 0, 1, 1)

        self.park_slider = QSlider(self.gridLayoutWidget)
        self.park_slider.setObjectName(u"park_slider")
        self.park_slider.setMaximum(10)
        self.park_slider.setOrientation(Qt.Orientation.Horizontal)

        self.location_weighting_layout.addWidget(self.park_slider, 16, 1, 1, 1)

        self.industrial_label = QLabel(self.gridLayoutWidget)
        self.industrial_label.setObjectName(u"industrial_label")

        self.location_weighting_layout.addWidget(self.industrial_label, 8, 0, 1, 1)

        self.religious_slider = QSlider(self.gridLayoutWidget)
        self.religious_slider.setObjectName(u"religious_slider")
        self.religious_slider.setMaximum(10)
        self.religious_slider.setOrientation(Qt.Orientation.Horizontal)

        self.location_weighting_layout.addWidget(self.religious_slider, 11, 1, 1, 1)

        self.office_slider = QSlider(self.gridLayoutWidget)
        self.office_slider.setObjectName(u"office_slider")
        self.office_slider.setMaximum(10)
        self.office_slider.setOrientation(Qt.Orientation.Horizontal)

        self.location_weighting_layout.addWidget(self.office_slider, 10, 1, 1, 1)

        self.hospital_label = QLabel(self.gridLayoutWidget)
        self.hospital_label.setObjectName(u"hospital_label")

        self.location_weighting_layout.addWidget(self.hospital_label, 1, 0, 1, 1)

        self.office_label = QLabel(self.gridLayoutWidget)
        self.office_label.setObjectName(u"office_label")

        self.location_weighting_layout.addWidget(self.office_label, 10, 0, 1, 1)

        self.hospital_slider = QSlider(self.gridLayoutWidget)
        self.hospital_slider.setObjectName(u"hospital_slider")
        self.hospital_slider.setMaximum(10)
        self.hospital_slider.setOrientation(Qt.Orientation.Horizontal)

        self.location_weighting_layout.addWidget(self.hospital_slider, 1, 1, 1, 1)

        self.agricultural_label = QLabel(self.gridLayoutWidget)
        self.agricultural_label.setObjectName(u"agricultural_label")

        self.location_weighting_layout.addWidget(self.agricultural_label, 6, 0, 1, 1)

        self.secondary_road_label = QLabel(self.gridLayoutWidget)
        self.secondary_road_label.setObjectName(u"secondary_road_label")

        self.location_weighting_layout.addWidget(self.secondary_road_label, 14, 0, 1, 1)

        self.commercial_label = QLabel(self.gridLayoutWidget)
        self.commercial_label.setObjectName(u"commercial_label")

        self.location_weighting_layout.addWidget(self.commercial_label, 9, 0, 1, 1)

        self.eldercare_slider = QSlider(self.gridLayoutWidget)
        self.eldercare_slider.setObjectName(u"eldercare_slider")
        self.eldercare_slider.setMaximum(10)
        self.eldercare_slider.setOrientation(Qt.Orientation.Horizontal)

        self.location_weighting_layout.addWidget(self.eldercare_slider, 12, 1, 1, 1)

        self.religious_label = QLabel(self.gridLayoutWidget)
        self.religious_label.setObjectName(u"religious_label")

        self.location_weighting_layout.addWidget(self.religious_label, 11, 0, 1, 1)

        self.education_slider = QSlider(self.gridLayoutWidget)
        self.education_slider.setObjectName(u"education_slider")
        self.education_slider.setMaximum(3)
        self.education_slider.setOrientation(Qt.Orientation.Horizontal)

        self.location_weighting_layout.addWidget(self.education_slider, 0, 1, 1, 1)

        self.local_road_slider = QSlider(self.gridLayoutWidget)
        self.local_road_slider.setObjectName(u"local_road_slider")
        self.local_road_slider.setMaximum(10)
        self.local_road_slider.setOrientation(Qt.Orientation.Horizontal)

        self.location_weighting_layout.addWidget(self.local_road_slider, 15, 1, 1, 1)

        self.residential_slider = QSlider(self.gridLayoutWidget)
        self.residential_slider.setObjectName(u"residential_slider")
        self.residential_slider.setMaximum(10)
        self.residential_slider.setOrientation(Qt.Orientation.Horizontal)

        self.location_weighting_layout.addWidget(self.residential_slider, 5, 1, 1, 1)

        self.eldercare_label = QLabel(self.gridLayoutWidget)
        self.eldercare_label.setObjectName(u"eldercare_label")

        self.location_weighting_layout.addWidget(self.eldercare_label, 12, 0, 1, 1)

        self.education_label = QLabel(self.gridLayoutWidget)
        self.education_label.setObjectName(u"education_label")

        self.location_weighting_layout.addWidget(self.education_label, 0, 0, 1, 1)

        self.horizontalLayoutWidget = QWidget(Dialog)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(110, 30, 251, 31))
        self.level_layout = QHBoxLayout(self.horizontalLayoutWidget)
        self.level_layout.setObjectName(u"level_layout")
        self.level_layout.setContentsMargins(0, 0, 0, 0)
        self.zero_label = QLabel(self.horizontalLayoutWidget)
        self.zero_label.setObjectName(u"zero_label")

        self.level_layout.addWidget(self.zero_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.level_layout.addItem(self.horizontalSpacer)

        self.low_label = QLabel(self.horizontalLayoutWidget)
        self.low_label.setObjectName(u"low_label")

        self.level_layout.addWidget(self.low_label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.level_layout.addItem(self.horizontalSpacer_2)

        self.medium_label = QLabel(self.horizontalLayoutWidget)
        self.medium_label.setObjectName(u"medium_label")

        self.level_layout.addWidget(self.medium_label)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.level_layout.addItem(self.horizontalSpacer_3)

        self.high_label = QLabel(self.horizontalLayoutWidget)
        self.high_label.setObjectName(u"high_label")

        self.level_layout.addWidget(self.high_label)

        self.title_label = QLabel(Dialog)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setGeometry(QRect(150, 10, 191, 20))

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Location weighting", None))
        self.park_label.setText(QCoreApplication.translate("Dialog", u"Park", None))
        self.primary_road_label.setText(QCoreApplication.translate("Dialog", u"Primary Road", None))
        self.local_road_label.setText(QCoreApplication.translate("Dialog", u"Local Road", None))
        self.residential_label.setText(QCoreApplication.translate("Dialog", u"Residential", None))
        self.industrial_label.setText(QCoreApplication.translate("Dialog", u"Industrial", None))
        self.hospital_label.setText(QCoreApplication.translate("Dialog", u"Hospital", None))
        self.office_label.setText(QCoreApplication.translate("Dialog", u"Office", None))
        self.agricultural_label.setText(QCoreApplication.translate("Dialog", u"Agricultural", None))
        self.secondary_road_label.setText(QCoreApplication.translate("Dialog", u"Secondary Road", None))
        self.commercial_label.setText(QCoreApplication.translate("Dialog", u"Commercial", None))
        self.religious_label.setText(QCoreApplication.translate("Dialog", u"Religious", None))
        self.eldercare_label.setText(QCoreApplication.translate("Dialog", u"Eldercare", None))
        self.education_label.setText(QCoreApplication.translate("Dialog", u"Education", None))
        self.zero_label.setText(QCoreApplication.translate("Dialog", u"Zero", None))
        self.low_label.setText(QCoreApplication.translate("Dialog", u"Low", None))
        self.medium_label.setText(QCoreApplication.translate("Dialog", u"Medium", None))
        self.high_label.setText(QCoreApplication.translate("Dialog", u"High", None))
        self.title_label.setText(QCoreApplication.translate("Dialog", u"Set location weighting", None))
    # retranslateUi

