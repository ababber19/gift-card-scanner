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




# Checks to see if the value is an int
def representsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False





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






# Creates an excel sheet containing all addresses and serial numbers
def createDF(dirPath, imageFileNames):
    # Initializes dataframe that will contains addresses and serial numbers
    df = pd.DataFrame(columns = ["File Name", "isAddress", "isSingleCard", "isPacket"])
    


    # For loop that goes through all of the image files
    for file in imageFileNames:
        try:
            # Opens the image
            img = Image.open("{}/{}".format(dirPath,file))
        
        except:
            wait = input("Image not available. Please press enter when the cloud downloads.")
            
            # Opens the image
            img = Image.open("{}/{}".format(dirPath,file))


        # Gets the text from the full image
        textFull = tess.image_to_string(img)
        textFull = str.replace(textFull, "\n", " ")
        textFull = textFull.lower()




        # For loop to make sure orientation is correct
        for i in range(3):
            # Checks to see if text can be read; if not, rotates image 270 degrees counterclockwise
            if (("ship" in textFull) or ("quantities" in textFull) or ("weight" in textFull) or ("costco" in textFull) or ("bundle" in textFull) or ("stock" in textFull) or ("event" in textFull) or ("serial" in textFull)) == False:
                # Rotates image
                img = img.rotate(270, expand = 1)

                # Gets the text from the image
                textFull = tess.image_to_string(img)
                textFull = str.replace(textFull, "\n", " ")
                textFull = textFull.lower()

            # Breaks out of while loop when read correctly
            else:
                break
        

        

        # Checks if this is the delivery paper, then gets the address of the store
        if ("shipping" in textFull) or ("quantities" in textFull) or ("weight" in textFull):
            tempDict = {"File Name": file, "isAddress": 1, "isSingleCard": 0, "isPacket": 0}


        # If this is a packet of cards, it gets the range of serial numbers    
        elif ("costco hotstar postcard" in textFull) or ("bundle" in textFull) or ("stock" in textFull) or ("qty" in textFull) or ("job" in textFull):
            tempDict = {"File Name": file, "isAddress": 0, "isSingleCard": 0, "isPacket": 1}


        # If it is a single card, it finds the serial number
        elif ("in the event a pin is non" in textFull) or ("serial #" in textFull) or ("our sole liability" in textFull):
            tempDict = {"File Name": file, "isAddress": 0, "isSingleCard": 1, "isPacket": 0}
            
        

        # Image cannot find information needed (picture is not clear enough)
        else:
            img.show()      
            

            while(True):
                unidentified = input("{} not found. Is this file an address, single serial number, or packet of serial numbers? (1 = address, 2 = single serial number, 3 = packet of serial numbers):\n".format(file))

                if unidentified == "1":
                    tempDict = {"File Name": file, "isAddress": 1, "isSingleCard": 0, "isPacket": 0}
                    break
                

                elif unidentified == "2":
                    tempDict = {"File Name": file, "isAddress": 0, "isSingleCard": 1, "isPacket": 0}
                    break


                elif unidentified == "3":
                    tempDict = {"File Name": file, "isAddress": 0, "isSingleCard": 0, "isPacket": 1}
                    break

                else:
                    print("Incorrect input")
            


        print("Something has been added!!!\n\n")
        df = df.append(tempDict, ignore_index=True)




    # Exports the df
    exportDF(df)






# Exports dataframe to excel file
def exportDF(df):
    # Sets an index to ensure no issues when exporting df
    df.set_index("File Name", inplace = True)



    # Name of excel file
    excelFile = "Image Classifier.csv"


    
    
    # Checks to see if excel file has already been created
    try:
        # Gets data from excel
        excelData = pd.read_excel(excelFile)


        # Sets the index for this df
        excelData.set_index("File Name", inplace = True)

        

        # Combines excel data and new data
        excelData = pd.concat([excelData, df], sort = True)    


        # Exports the dataframe to excel
        excelData.to_csv(excelFile)



    # Exports the dataframe to excel
    except:
        df.to_csv(excelFile)
        


    finally:
        print("FINISHED!!!\n\n")
        
        # Prints total number of serial numbers
        print("Total number of images: {}\n\n".format(len(df.index)))
        
    
        
        




# Main method
def main():
    # Gets directory path of raw images from user
    dirPath = input("Please enter the name of the folder that contains the images: ")

    isScanned = input("Are these images scanned already? (y = yes, n = no): ").lower()


    # If the ima?˘es have not been scanned, program cleans them up
    if (isScanned == "n"):
        # Creates directory name for cleaned images
        dirPathCleaned = "{}_cleaned".format(dirPath)
        

        # Keeps track of how long the program takes to clean the images
        startTimeCleanImages = datetime.now()

        # Prints to user that images are getting cleaned
        print("\n\n\nCleaning images...")

        # Gets list of files names of all raw images
        imageFileNames = getImageFileNames(dirPath)

        
        # Gets cleaned up images from these raw images
        pyimgscan.main(dirPath, imageFileNames, dirPathCleaned)

        # Prints to user that images have finished getting cleaned
        print("\nFinished cleaning images!")

        # Prints the total time taken to clean the images
        print("\nTime taken: {}".format(datetime.now() - startTimeCleanImages))


    # If the images have already been scanned, sets this folder as the cleaned images folder
    elif (isScanned == "y"):
        dirPathCleaned = dirPath


    print("\n\n\n")


    # Gets start time for main df code to run
    startTimeDF = datetime.now()

    # Gets the file names of all the cleaned images
    imageFileNamesCleaned = getImageFileNames(dirPathCleaned)


    # Creates the df containing all serial numbers
    createDF(dirPathCleaned, imageFileNamesCleaned)
    
    print("Total time to run: {}".format(datetime.now() - startTimeDF))







# Runs the main method of program when this file is called
if __name__ == '__main__':
    main()