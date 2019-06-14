import os
import random
import numpy as np
import cv2

class dataset:
  #in python, don't define any variables here, another it doesn't not belong to the object itself and will get mutated everything another class is called
    
    def __init__(self,path):
        self.PATH=path
        self.x=[]
        self.y=[]
        self.shapes=[]
        self.colours=[]
        self.data=[] #entire dataset
        self.IMG_SIZE=150
        self.medication_array=['Pill1','Pill2','Pill3','Pill4','Pill5','Pill6']
        self.colour_array=['Red','Orange','White','Black','Dark Red','Blue']
        self.shape=['Circular','Elliptical']
        
        
    def create_data(self):
        for pill in self.medication_array:
            #local variables
            my_path=os.path.join(self.PATH,pill)
            classnum=self.medication_array.index(pill) #indexed from 0 to 5 (will add one when showing results)
            pill_shape=self.shape[1]
        
        if classnum==0 or classnum==1 or classnum==3:
            pill_shape=self.shape[0]
            
        for image in os.listdir(my_path):
            try:
                img_array=cv2.imread(os.path.join(my_path,image))
                new_array=crop_image(img_array,self.IMG_SIZE)
                self.data.append([new_array,classnum,pill_shape,self.colour_array[classnum]])
            except Exception as e:
                print('f')
                pass
        random.shuffle(self.data)
    
    def structure_data(self):
        for image, label, pill_shape, colour in self.data:
            self.x.append(image)
            self.y.append(label)
            self.shapes.append(pill_shape)
            self.colours.append(colour)
        self.x=np.array(self.x).reshape(-1,self.IMG_SIZE,self.IMG_SIZE,3)

def crop_image(img_array,IMG_SIZE): 
    crop_img = img_array[250:750, 700:1200] #first crop the image
    
    #next find the contours of the image
    new_array=cv2.resize(crop_img,(IMG_SIZE,IMG_SIZE)) #resize every image before passing it in
    hsv = cv2.cvtColor(new_array, cv2.COLOR_BGR2HSV) #convert image to hsv
        
    return hsv

def np_convert(hsv,IMG_SIZE): 
    
    final=np.array(hsv).reshape(-1,IMG_SIZE,IMG_SIZE,3)
    return final

