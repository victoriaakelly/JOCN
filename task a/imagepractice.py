import os,random
from psychopy import visual,core,event

directory = os.getcwd()

images = []
for file in os.listdir(directory):
    #Here  I'm converting the filenames to lower case and checking if they have a .jpg or .png extension
    if file.lower().endswith(".jpg")  or file.lower().endswith(".png") :
        #If the file is a jpg or png, add it to our list of images
        images.append(file)
random.shuffle(images)

print ', '.join(images)
print len(images)