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

class define_colours_hsv:
  
  def newPill(self,name_of_colour,image):
    #create a new pill from parameters entered by the user and get_colours from the image, append it to our list
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    HSV_colours=get_colours_hsv(hsv_image,3,True)
    
    new_pill_colours=pill_colour(name_of_colour,HSV_colours)
    
    #update colour_dictionary_hue
    if new_pill_colours not in self.all_pills_hsv and new_pill_colours[0] not in self.colour_dictionary_hue.keys():
      self.all_pills_hsv.append(new_pill_colours) #append to array
      self.colour_dictionary_hue.update({HSV_colours[0]:name_of_colour}) #adds this key value pair to dicitonary
    else:
      print('Pill Already added')

  def deletePill(self,pill):
    try:
      self.all_pills_hsv.remove(pill)
      del self.colour_dictionary_hue[pill.HSV_values[0]] #deletes this key from dictionary
    except:
      print('Pill Not Found')
  
  def __init__(self):
    self.all_pills_hsv=[]
    self.colour_dictionary_hue={23:'Dark Orange',
                                35:'Light Orange',
                                340:'Pink'}
    
    #this is only used for testing accuracy, discard later
    self.colour_array=['Light Orange','Dark Orange','White','Brown','Brown and Orange','Pink']
      
#classify by HSV image:
class my_colours_hsv:
  
  def identifyColour(self,hsv_colours,isNewPill):
    #print('color:',image_colors)
    #print(range(len(Pills)))
    found=False
    greyCount=0
    for j in range(self.number_of_colors): #check each of the colours we found on the screen compare each
      extracted_colour = hsv_colours[j]
      extracted_h=extracted_colour[0]
      extracted_s=extracted_colour[1]
      extracted_v=extracted_colour[2]
      
    #If saturation is under 25, it is the gray colour around the pill, discard colour, continue
      if extracted_s<=25:
        greyCount+=1
        self.hue_array[j]=0
        continue #continue moves on to the next colour we are extracting
        
    #If the V is under 20 it is a darker colour, classify as Dark Brown
      elif extracted_v<=29:
        print('Dark Colour')
        self.addColour('Brown')
        self.hue_array[j]=1000 #brown set hue to arbitarily high value
        continue      

      found=False
      #loop through the hues in database instead, discarding the 0 and 1000s
      hue_list=self.database.getListHueDB()
      for hue in hue_list:
        for hue_value in hue:
          selected_hue = hue_value       
          # H within 5 of 23, classify as orange
          # H within 5 of 35, classify as light orange
          # H within 5 of 340 classify as Pink
          diff=selected_hue-extracted_h

          if abs(diff) < self.threshold and (selected_hue!=0 or selected_hue!=1000):
            #insert into array that hue
            self.hue_array[j]=selected_hue
            found=True
            break
        if found==True:
          break
          
      if not found:
        if isNewPill:
          self.hue_array[j]=extracted_h
        else:
          self.hue_array[j]=0
          
    #if empty, we have not found a colour or discarded 
    if not self.image_colour and greyCount==self.number_of_colors:
      self.image_colour.append('White')
      #hue array is all 0s
        
    return found
  
  #adds to this pill's array of detected colours
  def addColour(self,colour_to_add):
    #if the colour is not already in the image_colour array, append colour to add
    if colour_to_add not in self.image_colour:
      self.image_colour.append(colour_to_add)
          
        
  #hsv_colours
  def __init__(self,num_colours,myDB):
#     self.blister_bounds=self.colours_blister[i]
#     self.single_bounds=self.colours_single[i]
    self.database=myDB
    self.threshold=10
    self.image_colour=[] #list of all the colours in the photographed image
    self.number_of_colors=num_colours
    self.hue_array=[None]*self.number_of_colors #3 elements to fill this array with
    self.index=100000         
  #define the upper and lower bounds for each color
  #returns true
    
# class my_colours:
  
#   colours_blister=[[190,130,90],[210,170,111],[0,0,0],[77,51,42],[100,70,65],[150,95,95]] #range of RGB values
#   colours_single=[[200,100,40],[240,190,105],[0,0,0],[77,45,35],[105,61,47],[160,70,80]]
#   colour_array=['Red','Orange','White','Brown','Red and Yellow','Dark Red']
#    #check if the rgb_colors array is within the bounds
    
#   def withinBounds(self,image_colors):
#     select_image = False
    
    
#     for i in range(len(self.colour_array)): #loop through 6 colours
#       selected_color = rgb2lab(np.uint8(np.asarray([[self.colours_single[i]]])))
#       selected_color_blister=rgb2lab(np.uint8(np.asarray([[self.colours_blister[i]]])))
#       #print(self.colour_array[i],' single',selected_color,' blister', selected_color)
#       for j in range(self.number_of_colors): #check each of the colours we found on the screen
#         print(image_colors)
#         curr_color = rgb2lab(np.uint8(np.asarray([[image_colors[j]]])))
#         diff = deltaE_cie76(selected_color, curr_color)
        
#         if abs(diff) < self.threshold:
# #           if self.colour_array[i]=='Brown' or self.colour_array[i]=='Red and Yellow':
# #             print('rgb:', image_colors[j])
# #             print('single lab:',curr_color, 'single thresh', selected_color, 'diff: ', diff)
          
#           self.image_colour=self.colour_array[i]
#           self.index=i
#           select_image = True
#           return select_image
            
#         diff2=deltaE_cie76(selected_color_blister,curr_color)
#         if abs(diff2) < self.threshold:
# #           if self.colour_array[i]=='Brown' or self.colour_array[i]=='Red and Yellow':
# #             print('rgb:', image_colors[j])
# #             print('blister lab:',curr_color, 'blister thresh', selected_color_blister, 'diff: ',diff2)
#           self.image_colour=self.colour_array[i]
#           self.index=i
#           select_image = True
#           return select_image
          
#     return select_image
          
#   def __init__(self,rgb_colors,num_colours):
# #     self.blister_bounds=self.colours_blister[i]
# #     self.single_bounds=self.colours_single[i]
#     self.threshold=8
#     self.image_colour=None
#     self.number_of_colors=num_colours
#     self.index=100000
#     self.within_bounds=self.withinBounds(rgb_colors)
         
#   #define the upper and lower bounds for each color
