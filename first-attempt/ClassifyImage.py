# Imports for converting from image to text
import pytesseract as tess
from pytesseract import Output
from PIL import Image
import re
# Imports for gettings file names
from os import listdir
import os
from os.path import isfile, join
# Imports for df
import pandas as pd
import numpy as np
from openpyxl import load_workbook
# Imports for tracking time program takes to run
from datetime import datetime
import time
# Imports for cleaning images
import pyimgscan
import subprocess
# Imports for copying files
import shutil




# Used to sort the file names in the images directory
def numericalSort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts





# Creates a list of the files names of all images
def getImageFileNames(dirPath):
    # Gets all the image file names
    imageFileNames = [f for f in listdir(dirPath) if isfile(join(dirPath, f))]
    imageFileNames = sorted(imageFileNames, key = numericalSort)
    
    # Removes the hidden file in each folder ".DS_Store"
    if ".DS_Store" in imageFileNames:
        imageFileNames.remove(".DS_Store")
 
    return imageFileNames








def imageToMatrix(dirPath, imageFileNames):
    df = pd.read_csv()
    # For loop that goes through all of the image files
    for file in imageFileNames:
        try:
            # Opens the image
            img = Image.open("{}/{}".format(dirPath,file))
        
        except:
            wait = input("Image not available. Please press enter when the cloud downloads.")
            
            # Opens the image
            img = Image.open("{}/{}".format(dirPath,file))
        imgResize = img.resize((200,200), Image.ANTIALIAS)

    
    
        data = np.asarray(imgResize)

        print(data.shape)






def main():
    # Gets directory path of raw images from user
    dirPath = input("Please enter the name of the folder that contains the images: ")


    # Gets the file names of all the cleaned images
    imageFileNamesCleaned = getImageFileNames(dirPath)


    imageToMatrix(dirPath, imageFileNamesCleaned)

    





#main()


df = pd.read_excel("/Users/aryamanbabber/Desktop/Folders/Costco Giftcards Project/ML Classification/Image Classifier.xlsx")




print((df["isAddress"][1]))

