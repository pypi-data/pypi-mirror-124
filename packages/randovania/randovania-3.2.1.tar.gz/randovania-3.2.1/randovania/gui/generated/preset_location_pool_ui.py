# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preset_location_pool.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_PresetLocationPool(object):
    def setupUi(self, PresetLocationPool):
        if not PresetLocationPool.objectName():
            PresetLocationPool.setObjectName(u"PresetLocationPool")
        PresetLocationPool.resize(505, 463)
        self.centralWidget = QWidget(PresetLocationPool)
        self.centralWidget.setObjectName(u"centralWidget")
        self.centralWidget.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.randomization_mode_group = QGroupBox(self.centralWidget)
        self.randomization_mode_group.setObjectName(u"randomization_mode_group")
        self.verticalLayout_2 = QVBoxLayout(self.randomization_mode_group)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.check_major_minor = QCheckBox(self.randomization_mode_group)
        self.check_major_minor.setObjectName(u"check_major_minor")

        self.verticalLayout_2.addWidget(self.check_major_minor)

        self.randomization_mode_label = QLabel(self.randomization_mode_group)
        self.randomization_mode_label.setObjectName(u"randomization_mode_label")
        self.randomization_mode_label.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.randomization_mode_label)


        self.verticalLayout.addWidget(self.randomization_mode_group)

        self.locations_scroll_area = QScrollArea(self.centralWidget)
        self.locations_scroll_area.setObjectName(u"locations_scroll_area")
        self.locations_scroll_area.setWidgetResizable(True)
        self.locations_scroll_area_contents = QWidget()
        self.locations_scroll_area_contents.setObjectName(u"locations_scroll_area_contents")
        self.locations_scroll_area_contents.setGeometry(QRect(0, 0, 499, 343))
        self.locations_scroll_area_layout = QVBoxLayout(self.locations_scroll_area_contents)
        self.locations_scroll_area_layout.setSpacing(6)
        self.locations_scroll_area_layout.setContentsMargins(11, 11, 11, 11)
        self.locations_scroll_area_layout.setObjectName(u"locations_scroll_area_layout")
        self.locations_scroll_area_layout.setContentsMargins(0, 0, 0, 0)
        self.locations_scroll_area.setWidget(self.locations_scroll_area_contents)

        self.verticalLayout.addWidget(self.locations_scroll_area)

        PresetLocationPool.setCentralWidget(self.centralWidget)

        self.retranslateUi(PresetLocationPool)

        QMetaObject.connectSlotsByName(PresetLocationPool)
    # setupUi

    def retranslateUi(self, PresetLocationPool):
        PresetLocationPool.setWindowTitle(QCoreApplication.translate("PresetLocationPool", u"Location Pool", None))
        self.randomization_mode_group.setTitle(QCoreApplication.translate("PresetLocationPool", u"Randomization Mode", None))
        self.check_major_minor.setText(QCoreApplication.translate("PresetLocationPool", u"Enable major/minor split", None))
        self.randomization_mode_label.setText(QCoreApplication.translate("PresetLocationPool", u"<html><head/><body><p>If this setting is enabled, major items (i.e., major upgrades, Energy Tanks, Dark Temple Keys, and Energy Transfer Modules) and minor items (i.e, expansions) will be shuffled separately.<br/>Major items in excess of the number of major locations will be placed in minor locations, and vice versa.</p></body></html>", None))
    # retranslateUi

