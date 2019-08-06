import tensorflow as tf
import os
import matplotlib.pyplot as plt
import cv2
import sys
import numpy as np
import random
import pickle
#from neural_network.working_model import load_pretrained_model, evaluate_model
#from neural_network.create_dataset import crop_image, np_convert
from image_processing.image_processing import my_colours_hsv, accuracy
from image_processing.Image_processing_functions import process_image, convert_hsv_to_string, show_RGB_from_HSV, crop_rect, RGB2HEX, get_colours_hsv, HSV_REGULARIZED
from database.setup_database import my_database
from PyQt5 import QtCore, QtGui, QtWidgets
from UI.addPillUI import Dialog
from UI.classifyUI import Ui_Dialog
from UI.deletePillUI import delete_dialog

class Window(QtWidgets.QMainWindow):
    def __init__(self,myDatabase,parent=None):
        super(Window,self).__init__(parent)
        self.myWidget=Widget(self,myDatabase)
        self.setGeometry(50,50,798,800)
        self.setCentralWidget(self.myWidget)
        self.setWindowTitle('PillSafe')
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
        self.label.setObjectName("label")
        self.timer = QtCore.QTimer()


        #when the timer times out, display the current image on the cam
        self.startTimer()
        self.timer.timeout.connect(self.viewCam) #repeats

        self.verticalLayout_2.addWidget(self.label)
        self.verticalLayout.addLayout(self.verticalLayout_2)
     
        self.retranslateUi()

    def viewCam(self):
        #lag occurs here if you resize frame
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

        ui=Dialog(self,self.myDatabase,self.image)
        ui.show()
        ui.exec_()
        # ui.setupUi(popUp)

        # popUp.show()
        # popUp.exec_()
        self.startTimer()

    def classifyClick(self):
        
        try:
            #predict the pill here
            colour_hsv=process_image(self.image,150,3,3) #select an image
            pillColour=convert_hsv_to_string(colour_hsv,self.myDatabase)
            #get the actual name of the pill from database using pillColour.hue_array
            pillData=self.myDatabase.getMatchingPillDB(pillColour.hue_array)
            print(pillData)
            ui=Ui_Dialog(self,pillData[0])
            ui.show()
            ui.exec_()
        except:
            popUp=QtWidgets.QMessageBox()
            popUp.setText("Did Not Classify")
            popUp.exec_()
        self.startTimer()

    def removeClick(self):
        
        delete_ui=delete_dialog(self,self.myDatabase)
        delete_ui.show()
        delete_ui.exec_()

        # popUp=QtWidgets.QMessageBox()
        # popUp.setText('Removed Pill')
        # popUp.exec_()
        self.startTimer()


    def startTimer(self):
        # if timer is stopped, we start it up again
        if not self.timer.isActive():
            self.timer.start(10) #10 milliseconds
            self.cap = cv2.VideoCapture(-1) #had to manually adjust this to get the right camera from laptop (I used 2)
            #higher resolution
            self.cap.set(3,1920) 
            self.cap.set(4,1080)

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
    stylesheet= """
            QPushButton{
                position: absolute;
                color: #555;
                background: #fff;
                font-family: Lato;
                font-size: 30px;
                font-weight: 300;
            }
            QPushButton#addComplete{
                font-size:20px;
                font-family: Arial;
            }
            QDialog{
                background: #abdfff;
            }
            QMainWindow{
                background: #abdfff;
            }
            QTextEdit{
                background-color: none;
            }
            QLineEdit{
                background-color: none;
            }
            """
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    GUI=Window(myDB)
    GUI.show()
    sys.exit(app.exec_())


# Functioning Code without GUI with Neural Net and Image Processing

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
