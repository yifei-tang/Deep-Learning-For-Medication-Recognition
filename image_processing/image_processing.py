import os
import matplotlib.pyplot as plt
import cv2
import numpy as np
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
from sklearn.cluster import KMeans

class accuracy:
  def __init__(self):
    self.total_image_count=0
    self.correct_image_count=0
    self.accuracy=0
    
class my_colours:
  
  colours_blister=[[190,130,90],[210,170,111],[0,0,0],[77,51,42],[100,70,65],[150,95,95]] #range of RGB values
  colours_single=[[200,100,40],[240,190,105],[0,0,0],[77,45,35],[105,61,47],[160,70,80]]
  colour_array=['Red','Orange','White','Brown','Red and Yellow','Dark Red']
   #check if the rgb_colors array is within the bounds
    
  def withinBounds(self,image_colors):
    select_image = False
    
    
    for i in range(len(self.colour_array)): #loop through 6 colours
      selected_color = rgb2lab(np.uint8(np.asarray([[self.colours_single[i]]])))
      selected_color_blister=rgb2lab(np.uint8(np.asarray([[self.colours_blister[i]]])))
      #print(self.colour_array[i],' single',selected_color,' blister', selected_color)
      for j in range(self.number_of_colors): #check each of the colours we found on the screen
        
        curr_color = rgb2lab(np.uint8(np.asarray([[image_colors[j]]])))
        diff = deltaE_cie76(selected_color, curr_color)
        
        if abs(diff) < self.threshold:
#           if self.colour_array[i]=='Brown' or self.colour_array[i]=='Red and Yellow':
#             print('rgb:', image_colors[j])
#             print('single lab:',curr_color, 'single thresh', selected_color, 'diff: ', diff)
          
          self.image_colour=self.colour_array[i]
          self.index=i
          select_image = True
          return select_image
            
        diff2=deltaE_cie76(selected_color_blister,curr_color)
        if abs(diff2) < self.threshold:
#           if self.colour_array[i]=='Brown' or self.colour_array[i]=='Red and Yellow':
#             print('rgb:', image_colors[j])
#             print('blister lab:',curr_color, 'blister thresh', selected_color_blister, 'diff: ',diff2)
          self.image_colour=self.colour_array[i]
          self.index=i
          select_image = True
          return select_image
          
    return select_image
          
  def __init__(self,rgb_colors,num_colours):
#     self.blister_bounds=self.colours_blister[i]
#     self.single_bounds=self.colours_single[i]
    self.threshold=8
    self.image_colour=None
    self.number_of_colors=num_colours
    self.index=100000
    self.within_bounds=self.withinBounds(rgb_colors)
         
  #define the upper and lower bounds for each color
