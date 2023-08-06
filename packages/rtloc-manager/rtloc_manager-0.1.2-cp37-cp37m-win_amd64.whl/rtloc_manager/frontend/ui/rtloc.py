# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rtloc.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PySide2 import QtCore, QtGui, QtWidgets


class Ui_RTLOC(object):
    def setupUi(self, RTLOC):
        RTLOC.setObjectName("RTLOC")
        RTLOC.resize(947, 875)
        self.centralwidget = QtWidgets.QWidget(RTLOC)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.plotGrid = QtWidgets.QGridLayout()
        self.plotGrid.setObjectName("plotGrid")
        self.horizontalLayout_2.addLayout(self.plotGrid)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btn_toggle_alarm = QtWidgets.QPushButton(self.centralwidget)
        self.btn_toggle_alarm.setEnabled(False)
        self.btn_toggle_alarm.setObjectName("btn_toggle_alarm")
        self.horizontalLayout.addWidget(self.btn_toggle_alarm)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        RTLOC.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(RTLOC)
        self.statusbar.setObjectName("statusbar")
        RTLOC.setStatusBar(self.statusbar)

        self.retranslateUi(RTLOC)
        QtCore.QMetaObject.connectSlotsByName(RTLOC)

    def retranslateUi(self, RTLOC):
        _translate = QtCore.QCoreApplication.translate
        RTLOC.setWindowTitle(_translate("RTLOC", "RTLOC"))
        self.btn_toggle_alarm.setText(_translate("RTLOC", "Toggle alarm DISXXXX"))
