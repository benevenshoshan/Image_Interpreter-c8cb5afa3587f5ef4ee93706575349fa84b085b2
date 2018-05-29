"""
This file is all about sorting files and working directories, filled with useful methods that I wrote.
Each method has good documentation, and does a specific job.
@author = Ben Even-Shoshan
"""

import os
from scipy import misc
import numpy as np
import imageio

path = "C:\\Users\Ben\Documents\GitHub\Image_Interpreter\Oranges"


#This method gets source folder as input and makes a filw for each image in it to train from.
def sortFiles(path):
    list_of_files = {} #Empty array which will be filled with the filenames
    for (dirpath, dirnames, filenames) in os.walk(path): #Going in a loop through the directory.
        for filename in filenames:
            if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
                list_of_files[filename] = os.sep.join([dirpath, filename]) #Adds files to array
    n=0
    for file in list_of_files: #Going through the files
        arr = imageio.imread(list_of_files[filename]) #Creating an array to store the RGB values of each image
        np.save(str(n), arr) #Saving each image's RGB values as text array files to go through later.
        n = n+1


