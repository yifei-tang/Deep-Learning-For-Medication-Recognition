# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addPill.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from database.setup_database import my_database
from image_processing.Image_processing_functions import process_image, convert_hsv_to_string
from image_processing.image_processing import my_colours_hsv
import cv2


class Dialog(QtWidgets.QDialog):
    def __init__(self,parent,myDB,image):
        super(Dialog,self).__init__(parent)
        self.image=image
        self.myDB=myDB
        self.setObjectName("Dialog")
        self.resize(597, 389)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")


        #Enter Pill Name
        self.enterPillName = QtWidgets.QLabel(self)
        self.enterPillName.setObjectName("enterPillName")
        self.gridLayout.addWidget(self.enterPillName, 0, 0, 1, 1)

        self.pillName = QtWidgets.QLineEdit(self)
        self.pillName.setText("")
        self.pillName.setObjectName("pillName")
        self.gridLayout.addWidget(self.pillName, 1, 0, 1, 1)
        

        #Enter Dosage
        self.enterDosage = QtWidgets.QLabel(self)
        self.enterDosage.setObjectName("enterDosage")
        self.gridLayout.addWidget(self.enterDosage, 2, 0, 1, 1)

        self.pillDosage = QtWidgets.QLineEdit(self)
        self.pillDosage.setObjectName("pillDosage")
        self.gridLayout.addWidget(self.pillDosage, 3, 0, 1, 1)
        
        #Enter Colour
        self.enterColour = QtWidgets.QLabel(self)
        self.enterColour.setObjectName("enterColour")
        self.gridLayout.addWidget(self.enterColour, 4, 0, 1, 1)

        self.pillColour = QtWidgets.QLineEdit(self)
        self.pillColour.setObjectName("pillColour")
        self.gridLayout.addWidget(self.pillColour, 5, 0, 1, 1)

        #Enter Manufacturer
        self.enterManufacturer = QtWidgets.QLabel(self)
        self.enterManufacturer.setObjectName("enterManufacturer")
        self.gridLayout.addWidget(self.enterManufacturer, 7, 0, 1, 1)
        self.pillCountry = QtWidgets.QLineEdit(self)
        self.pillCountry.setObjectName("pillCountry")
        self.gridLayout.addWidget(self.pillCountry, 8, 0, 1, 1)

        #Enter Description
        self.enterUse = QtWidgets.QLabel(self)
        self.enterUse.setObjectName("enterUse")
        self.gridLayout.addWidget(self.enterUse, 16, 0, 1, 1)
        
        self.pillDescription = QtWidgets.QTextEdit(self)
        self.pillDescription.setObjectName("pillDescription")
        self.gridLayout.addWidget(self.pillDescription, 17, 0, 1, 1)

        #Add Complete
        self.addComplete = QtWidgets.QPushButton(self)
        self.addComplete.setObjectName("addComplete")
        self.addComplete.clicked.connect(self.printText)
        self.gridLayout.addWidget(self.addComplete, 18, 0, 1, 1)

        self.retranslateUi(self)
        #self.okay.accepted.connect(Dialog.accept)
        # self.okay.accepted.connect(self.printText(Dialog)) find a way to click okay when you click this
        #self.okay.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def printText(self, Dialog):
        print(self.pillName.text())
        print(self.pillColour.text())
        print(self.pillDescription.toPlainText())
        
        #now use the picture we took previously and process it


        #search database here, look for the pill
        popUp=QtWidgets.QMessageBox()
        #if not found, then you must add it
        if not self.myDB.foundInDB(self.pillName.text()):
            #extract HSV values with image processing
            colours_hsv=process_image(self.image,150,3,3)
            pillColour=my_colours_hsv(3,self.myDB)
            pillColour.identifyColour(colours_hsv,True)
            hueDB=pillColour.hue_array

            try:
                self.myDB.insertDB(self.pillName.text(),self.pillDosage.text(),self.pillColour.text(),int(hueDB[0]),int(hueDB[1]),int(hueDB[2]),self.pillDescription.toPlainText(),self.pillCountry.text())
                popUp.setText('Successfully Added')
                popUp.exec_()
                self.close()

            except:
                popUp.setText('Unable To Insert. Please Try Again')
                popUp.exec_()

            
        else:
            popUp.setText('Pill Name Already In Database. Please Try Again')
            popUp.exec_()
        
        

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.enterDosage.setText(_translate("Dialog", "Enter Dosage: "))
        self.enterUse.setText(_translate("Dialog", "Enter Pill Use"))
        self.enterColour.setText(_translate("Dialog", "Enter Colour:"))
        self.enterPillName.setText(_translate("Dialog", "Enter Pill Name:"))
        self.enterManufacturer.setText(_translate("Dialog", "Enter Manufacturer:"))
        self.addComplete.setText(_translate("Dialog", "Add"))


