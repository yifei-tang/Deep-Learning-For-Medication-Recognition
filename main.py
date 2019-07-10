import tensorflow as tf
import os
import matplotlib.pyplot as plt
import cv2
import sys
import numpy as np
import random
import pickle
from neural_network.working_model import load_pretrained_model, evaluate_model
from neural_network.create_dataset import crop_image, np_convert
from image_processing.image_processing import my_colours_hsv, accuracy
from image_processing.Image_processing_functions import process_image, show_RGB_from_HSV, crop_rect, RGB2HEX, get_colours_hsv, HSV_REGULARIZED
from database.setup_database import my_database
from PyQt5 import QtCore, QtGui, QtWidgets
from UI.addPillUI import Dialog

class Window(QtWidgets.QMainWindow):
    def __init__(self,myDatabase,parent=None):
        super(Window,self).__init__(parent)
        self.myWidget=Widget(self,myDatabase)
        self.setGeometry(50,50,798,800)
        self.setCentralWidget(self.myWidget)
        self.setWindowTitle('PillPicker')
        self.setWindowIcon(QtGui.QIcon('pillIcon.png'))



class Widget(QtWidgets.QWidget):
    def __init__(self,parent,myDatabase):
        super(Widget,self).__init__(parent)
        self.myDatabase=myDatabase
        self.setObjectName("MainWindow")
        self.resize(789, 688)
        #self.centralwidget = QtWidgets.QWidget()
        #self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        #Add Button
        self.addButton = QtWidgets.QPushButton(self)
        self.addButton.clicked.connect(self.pauseTimer)
        self.addButton.clicked.connect(self.addClick)
        self.addButton.setObjectName("addButton")
        self.verticalLayout_2.addWidget(self.addButton)

        #Classify Button
        self.classifyButton = QtWidgets.QPushButton(self)
        self.classifyButton.setObjectName("classifyButton")
        self.classifyButton.clicked.connect(self.pauseTimer)
        self.classifyButton.clicked.connect(self.classifyClick)
        self.verticalLayout_2.addWidget(self.classifyButton)

        #Remove Button
        self.removeButton = QtWidgets.QPushButton(self)
        self.removeButton.setObjectName("removeButton")
        self.verticalLayout_2.addWidget(self.removeButton)
        self.removeButton.clicked.connect(self.pauseTimer)
        self.removeButton.clicked.connect(self.removeClick)


        #pixmap on the label
        self.label = QtWidgets.QLabel(self)
        #pixmap = QtGui.QPixmap('pillIcon.png')
        #self.label.setPixmap(pixmap)

        self.label.setObjectName("label")
        self.timer = QtCore.QTimer()


        #when the timer times out, display the current image on the cam
        self.startTimer()
        self.timer.timeout.connect(self.viewCam) #repeats

        self.verticalLayout_2.addWidget(self.label)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        #self.setCentralWidget(self.centralwidget)

        # self.menubar = QtWidgets.QMenuBar(MainWindow)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 789, 22))
        # self.menubar.setObjectName("menubar")
        # self.menuFile = QtWidgets.QMenu(self.menubar)
        # self.menuFile.setObjectName("menuFile")
        # MainWindow.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)
        # self.actionSave = QtWidgets.QAction(MainWindow)
        # self.actionSave.setObjectName("actionSave")
        # self.menuFile.addAction(self.actionSave)
        # self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi()
        #QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def viewCam(self):
        
        #higher resolution
        self.cap.set(3,1920)
        self.cap.set(4,1080)

        #read image in bgr format
        ret, self.image = self.cap.read()
        # convert image to RGB format
        RBG_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        # get image infos
        height, width, channel = self.image.shape
        step = channel * width
        # create QImage from image
        qImg = QtGui.QImage(RBG_image.data, width, height, step, QtGui.QImage.Format_RGB888)
        # show image in img_label
        self.label.setPixmap(QtGui.QPixmap.fromImage(qImg))

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.addButton.setText(_translate("MainWindow", "Add New Pill"))
        self.classifyButton.setText(_translate("MainWindow", "Classify Pill"))
        self.removeButton.setText(_translate("MainWindow", "Remove Pill"))
        #self.actionSave.setText(_translate("MainWindow", "Save"))

    def addClick(self):
        #mydata=dataEntered()
        # popUp=QtWidgets.QDialog()

        ui=Dialog(self,self.myDatabase)
        ui.show()
        ui.exec_()
        # ui.setupUi(popUp)

        # popUp.show()
        # popUp.exec_()
        self.startTimer()

    def classifyClick(self):
        popUp=QtWidgets.QMessageBox()

        #predict the pill here
        pillColour=process_image(self.image,150,3,3) #select an image
        string1='Pill classified as '
        string2=''
        for colour in pillColour.image_colour:
            if pillColour.image_colour.index(colour)==0:
                string2= string2+colour
            else:
                string2=string2+', '+colour

        string=string1+string2
        popUp.setText(string)
        popUp.exec_()
        self.startTimer()

    def removeClick(self):
        popUp=QtWidgets.QMessageBox()
        #predict the pill here

        popUp.setText('Removed Pill')
        popUp.exec_()
        self.startTimer()


    def startTimer(self):
        # if timer is stopped, we start it up again
        if not self.timer.isActive():
            self.timer.start(1) #20 milliseconds
            self.cap = cv2.VideoCapture(0)

    def pauseTimer(self):
        self.timer.stop()
        self.cap.release()

class dataEntered:
    def __init__(self):
        self.name=""
        self.dosage="" 
        self.colour="" 
        self.hue=0
        self.description="" 
        self.countryOfOrigin=""


if __name__ == "__main__":
    import sys
    myDB=my_database()
    app = QtWidgets.QApplication(sys.argv)
    GUI=Window(myDB)
    GUI.show()
    # MainWindow = QtWidgets.QMainWindow()
    # ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    sys.exit(app.exec_())



# colour_array=['Red','Orange','White','Brown','Red and Yellow','Dark Red']
# model=load_pretrained_model()
# evaluate_model(model)
# #capture from webcam
# cap = cv2.VideoCapture(2)
# cap.set(3,1920)
# cap.set(4,1080)


# #read from webcam 
# while True:
#     ret, frame=cap.read()
#     cv2.imshow('PillCheck',frame)
#     if cv2.waitKey(1) & 0xFF == ord('c'): #crop
#             break
# image=frame
# #cv2.imshow('my picture',image)
# k=cv2.waitKey(0)
# # if k=='q' :
# #     cv2.destroyAllWindows()
    

# #image processing method
# image_processing=process_image(image,150,3,3) #select an image
# print('image processed')

# #using neural network
# cropped_image=crop_image(image,150)
# cropped_image=cropped_image/255.0
# cropped_image_np=np_convert(cropped_image,150)
# ypr=model.predict(cropped_image_np)
# print('Neural Net:',ypr)
# print('Neural Network Prediction: ',colour_array[np.argmax(ypr)])

# k=cv2.waitKey(0)
# if k=='q' :
#     cv2.destroyAllWindows()
