import os
import matplotlib.pyplot as plt
import cv2
import numpy as np
from image_processing.image_processing import my_colours
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
from sklearn.cluster import KMeans

def process_image(img_array,IMG_SIZE,pill_index): 
  
  crop_img = img_array[250:750, 700:1200] #first crop the image
  #length x width
  hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV) #convert image to hsv
  #cv2_imshow(crop_img)
  #split hsv into separate channels, use the apply otsu on the s channel in order to invert it
  h,s,v=cv2.split(hsv)
  retval2,thresh2 = cv2.threshold(s,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

  if retval2<10: #to account for otsu not being able to find two peaks to approximate a value under 
    new_array=cv2.resize(crop_img,(IMG_SIZE,IMG_SIZE))
    #pillAccuracy.correct_image_count+=1
    print('Image Processing Prediction: White')
    return crop_img #just return the original image of the white pill
  
  kernel = np.ones((5,5),np.uint8)
  
  #apply blurs
  blur = cv2.GaussianBlur(thresh2,(5,5),0) #Gaussian Blur gets rid of the noise from the image
  blur2 = cv2.bilateralFilter(blur,9,75,75) #bilaterial filter on top of that
  closing = cv2.morphologyEx(blur2, cv2.MORPH_CLOSE, kernel) #smooths the image so contours are detected better
  
  #find and draw contours
  contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  
  #cv2.drawContours(hsv,contours,-1,(0,0,255)) #draw contours (red circles in image)
  contour_area=cv2.contourArea(contours[0])

  #poor quality image if the contour is smaller than 200
  if contour_area<200:
    #set some boolean append variable in to false, then in process  image, do not append the image
    return crop_img
    
  #rectangles and crop
  rect=cv2.minAreaRect(contours[0])
  box=cv2.boxPoints(rect)
  box=np.int0(box) #convert all values of box into integers, same array
  #cv2.drawContours(hsv,[box],0,(0,255,0)) #draw green contours around the box to crop the image
  
  
  final_crop=crop_rect(hsv, rect) 
  rgb=show_RGB_from_HSV(final_crop)
  rgb_bright=increase_image_brightness(rgb)
  colours=get_colours(rgb_bright,2,True)
  
  pillColour=my_colours(colours,2)
  print('Image Processing Prediction:', pillColour.image_colour)
#   if pillColour.index==pill_index:
#     pillAccuracy.correct_image_count+=1
    
  new_array=cv2.resize(final_crop,(IMG_SIZE,IMG_SIZE)) #resize array before moving forward
  return new_array

def find_outer_rectangle(IMG_ARRAY,IMG_SIZE):
  hsv = cv2.cvtColor(IMG_ARRAY, cv2.COLOR_BGR2HSV) #convert image to hsv
  
  #split hsv into separate channels, use the apply otsu on the s channel in order to invert it
  h,s,v=cv2.split(hsv)
  retval2,thresh2 = cv2.threshold(s,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
  
  _,contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  
  cv2.drawContours(hsv,contours,-1,(0,0,255)) #draw contours (red circles in image)

def crop_rect(img, rect):
    # get the parameter of the small rectangle
    center, size, angle = rect[0], rect[1], rect[2]
    #print("my rect", rect)
    center, size = tuple(map(int, center)), tuple(map(int, size)) #convert each cooordinate to integers and then convert into tuples
    #print(center," + ",size, " + ", angle)
    # get row and col num in img
    height, width = img.shape[0], img.shape[1]

    # calculate the rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1)
    
    # rotate the original image relative to the rectangle
    img_rot = cv2.warpAffine(img, M, (width, height))

    # now rotated rectangle becomes vertical and we crop it
    img_crop = cv2.getRectSubPix(img_rot, size, center)

    return img_crop

def show_RGB_from_HSV(image_in):
  bgrimg = cv2.cvtColor(image_in, cv2.COLOR_HSV2BGR)
  #cv2_imshow(bgrimg)
  #brgimg=increase_image_brightness(bgrimg)
  image = cv2.cvtColor(bgrimg, cv2.COLOR_BGR2RGB)
  pixels = np.array(image)
  cv2.imshow('PillPicker',bgrimg)
  print(image)
  #plt.imshow(pixels)
  #plt.show()
  return pixels

def RGB2HEX(rgb):
  return "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def increase_image_brightness(image):
  alpha=1.5
  beta=1
  new_image = np.zeros(image.shape, image.dtype)
  for y in range(image.shape[0]):
    for x in range(image.shape[1]):
        for c in range(image.shape[2]):
            new_image[y,x,c] = np.clip(alpha*image[y,x,c] + beta, 0, 255)
  #cv2_imshow(image)
  #cv2_imshow(new_image)
  return new_image


def get_colours(rgb_img,number_of_colours,show_chart):
  #cv2_imshow(rgb_img)
  rgb_img = rgb_img.reshape(rgb_img.shape[0]*rgb_img.shape[1], 3) #must be 2 dimensional
  clf = KMeans(n_clusters = number_of_colours)
  labels = clf.fit_predict(rgb_img)
  #print('labels',labels)
  counts=Counter(labels) #keeps track of how many times equivalent values are added
 # print('counts',counts) #
 # print('keys',counts.keys())
  
  center_colors = clf.cluster_centers_
 # print('center colors',center_colors)
  ordered_colors = [center_colors[i] for i in counts.keys()] 
 # print('ordered',ordered_colors)
  hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
  #print('hex',hex_colors)
  rgb_colors = [ordered_colors[i] for i in counts.keys()]
  
#   if (show_chart):
#       plt.figure(figsize = (8, 6))
#       plt.pie(counts.values(), labels = hex_colors, colors = hex_colors)

  return rgb_colors