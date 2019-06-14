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
from image_processing.image_processing import my_colours, accuracy
from image_processing.Image_processing_functions import process_image, show_RGB_from_HSV, find_outer_rectangle, crop_rect, RGB2HEX, increase_image_brightness, get_colours

colour_array=['Red','Orange','White','Black','Dark Red','Blue']
model=load_pretrained_model()

image=cv2.imread('pill1ex.jpg')

#image processing method
image_processing=process_image(image,150,0) #select an image

#using neural network
cropped_image=crop_image(image,150)
cropped_image_np=np_convert(cropped_image,150)
ypr=model.predict(cropped_image_np)
print('Neural Network Prediction: ',colour_array[np.argmax(ypr)])

k=cv2.waitKey(0)
if k=='q' :
    cv2.destroyAllWindows()
