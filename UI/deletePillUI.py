
from PyQt5 import QtCore, QtGui, QtWidgets
from database.setup_database import my_database
from image_processing.Image_processing_functions import process_image, convert_hsv_to_string
from image_processing.image_processing import my_colours_hsv
import cv2


class delete_dialog(QtWidgets.QDialog):
    def __init__(self,parent,myDB):
        super(delete_dialog,self).__init__(parent)
        self.myDB=myDB
        self.setObjectName("Delete Dialog")
        self.resize(500, 100)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        self.enterSearch = QtWidgets.QLabel(self)
        self.enterSearch.setObjectName("enterPillName")
        self.gridLayout.addWidget(self.enterSearch, 0, 0, 1, 1)

        self.model = QtCore.QStringListModel()
        nameTupleList=self.myDB.getListNamesDB() #returns name list as a tuple 
        nameList=[]
        for myTuple in nameTupleList:
            nameList.append(self.convertTupleToString(myTuple))

        self.model.setStringList(nameList)

        self.completer = QtWidgets.QCompleter()
        self.completer.setModel(self.model)

        self.search = QtWidgets.QLineEdit()
        self.search.setCompleter(self.completer)

        #add a button that says okay, get the line from line edit, search database and delete pill from database
        self.removeComplete = QtWidgets.QPushButton(self)
        self.removeComplete.setObjectName("removeComplete")
        self.removeComplete.clicked.connect(self.remove)
        #self.removeComplete.clicked.connect(self.printText)

        self.gridLayout.addWidget(self.removeComplete, 18, 0, 1, 1)
        self.gridLayout.addWidget(self.search, 1, 0, 1, 1)

        self.retranslateUi(self)
        #self.okay.accepted.connect(Dialog.accept)
        # self.okay.accepted.connect(self.printText(Dialog)) find a way to click okay when you click this
        #self.okay.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(self)
        
    def convertTupleToString(self, myTuple):
        str =  ''.join(myTuple) 
        return str

    def remove(self, Dialog):
        name=self.search.text()
        print(self.search.text())
        popUp=QtWidgets.QMessageBox()

        try:
            self.myDB.removeDB(name)
            popUp.setText('Removed Successfully')
            popUp.exec_()
            self.close()

        except:
            popUp.setText('Remove Failed. Try again')
            popUp.exec_()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.enterSearch.setText(_translate("Dialog", "Enter Pill Name To Delete:"))
        self.removeComplete.setText(_translate("Dialog","Done"))


