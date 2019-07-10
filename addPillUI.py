# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addPill.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(597, 389)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.enterDosage = QtWidgets.QLabel(Dialog)
        self.enterDosage.setObjectName("enterDosage")
        self.gridLayout.addWidget(self.enterDosage, 2, 0, 1, 1)
        self.enterUse = QtWidgets.QLabel(Dialog)
        self.enterUse.setObjectName("enterUse")
        self.gridLayout.addWidget(self.enterUse, 16, 0, 1, 1)
        self.okay = QtWidgets.QDialogButtonBox(Dialog)
        self.okay.setOrientation(QtCore.Qt.Vertical)
        self.okay.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.okay.setObjectName("okay")
        self.gridLayout.addWidget(self.okay, 19, 0, 1, 1)
        self.enterColour = QtWidgets.QLabel(Dialog)
        self.enterColour.setObjectName("enterColour")
        self.gridLayout.addWidget(self.enterColour, 4, 0, 1, 1)
        self.pillDosage = QtWidgets.QLineEdit(Dialog)
        self.pillDosage.setObjectName("pillDosage")
        self.gridLayout.addWidget(self.pillDosage, 3, 0, 1, 1)
        self.pillDescription = QtWidgets.QTextEdit(Dialog)
        self.pillDescription.setObjectName("pillDescription")
        self.gridLayout.addWidget(self.pillDescription, 17, 0, 1, 1)
        self.pillColour = QtWidgets.QLineEdit(Dialog)
        self.pillColour.setObjectName("pillColour")
        self.gridLayout.addWidget(self.pillColour, 5, 0, 1, 1)
        self.pillName = QtWidgets.QLineEdit(Dialog)
        self.pillName.setText("")
        self.pillName.setObjectName("pillName")
        self.gridLayout.addWidget(self.pillName, 1, 0, 1, 1)
        self.enterPillName = QtWidgets.QLabel(Dialog)
        self.enterPillName.setObjectName("enterPillName")
        self.gridLayout.addWidget(self.enterPillName, 0, 0, 1, 1)
        self.enterManufacturer = QtWidgets.QLabel(Dialog)
        self.enterManufacturer.setObjectName("enterManufacturer")
        self.gridLayout.addWidget(self.enterManufacturer, 7, 0, 1, 1)
        self.pillCountry = QtWidgets.QLineEdit(Dialog)
        self.pillCountry.setObjectName("pillCountry")
        self.gridLayout.addWidget(self.pillCountry, 8, 0, 1, 1)
        self.addComplete = QtWidgets.QPushButton(Dialog)
        self.addComplete.setObjectName("addComplete")
        self.gridLayout.addWidget(self.addComplete, 18, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.okay.accepted.connect(Dialog.accept)
        self.okay.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.enterDosage.setText(_translate("Dialog", "Enter Dosage: "))
        self.enterUse.setText(_translate("Dialog", "Enter Pill Use"))
        self.enterColour.setText(_translate("Dialog", "Enter Colour:"))
        self.enterPillName.setText(_translate("Dialog", "Enter Pill Name:"))
        self.enterManufacturer.setText(_translate("Dialog", "Enter Manufacturer:"))
        self.addComplete.setText(_translate("Dialog", "Add"))


