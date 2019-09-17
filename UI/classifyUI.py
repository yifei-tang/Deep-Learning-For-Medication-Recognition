# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'classifyGUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(QtWidgets.QDialog):
    def __init__(self, parent, pillCharacteristics):
        super(Ui_Dialog,self).__init__(parent)
        self.setObjectName("Dialog")
        self.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setAlternatingRowColors(True)
        
        pillCharLabels= ['Pill Name','Colour','Dosage','H1','H2','H3','Usage','Manufacturer']
        for i in pillCharacteristics:
            ind=pillCharacteristics.index(i)
            if ind != 3 and ind!=4 and ind!=5:
                self.listWidget.addItem(str(pillCharLabels[ind]+': '+i))
        self.gridLayout.addWidget(self.listWidget, 1, 0, 1, 1)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Pill Classified As"))


