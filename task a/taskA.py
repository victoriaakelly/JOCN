from psychopy import os, visual, core, event, gui, data, sound, logging
import sys
import os
import csv
import datetime
import random

# path to working directory, keep images here for now, link to image folder later
directory = os.getcwd()

#get subjID
subjDlg=gui.Dlg(title="JOCN paper- rate items")
subjDlg.addField('Enter Subject ID: ')
subjDlg.show()
subj_id=subjDlg.data[0]

if len(subj_id)<1: # Make sure participant entered name
    core.quit()

# Initialzing Window 
win = visual.Window(fullscr=False, size=[1100, 800], units='pix', monitor='testMonitor')
# Create Insruction and thank you screens
instruction_screen = visual.TextStim(win, text="""Rate how much you prefer the items by clicking on the rating line.
                                     \nPress \'Enter\' or click the button below the line to move on to the next item.
                                     \nThe rating is from: \n  1 (little to no preference)\n  to 7 (very high preference). 
                                      \n Press any key to start""")
thank_you_screen = visual.TextStim(win, text="""Thank you for choosing!""")

# Show instruction screen
event.clearEvents()
instruction_screen.draw()
win.flip

# Lets participant quit at any time by pressing escape button
if 'escape' in event.waitKeys():
    core.quit()

# Initializing rating scale
myRatingScale = visual.RatingScale(win, choices=['1', '2', '3', '4', '5', '6', '7'])

# Initializing image list for 
imageList = []
for file in os.listdir(directory): # os.listdir(directory) opens the 'directory' defined on line 8
    # Here  I'm converting the filenames to lower case and checking if they have
    # a .jpg or .png extension.
    if file.lower().endswith(".jpg")  or file.lower().endswith(".png") :
        #If the file is a jpg or png, add it to our list of images
        imageList.append(file)
# Randomize order of images
random.shuffle(imageList)

# Initializing response list same size as imageList
responses = [""] * len(imageList)

for image in imageList:
    x, y = myRatingScale.win.size 
    # I use the size parameter here to rescale the images, they are a bit stretched in some cases.
    # This can be mitigated by cropping the images into a resolution that would scale to the specified one bellow.
    myItem = visual.ImageStim(win=win, image=image, units='pix', pos=[0, y//7], size = [500,450])

    # rate each image on one dimension
    #for dimension in ['0=Little to no prefernce. . . 50=Very high preference']:
    myRatingScale.reset()  # reset between repeated uses of the same scale
    event.clearEvents()
    while myRatingScale.noResponse:
        myItem.draw()
        myRatingScale.draw()
        win.flip()
        if event.getKeys(['escape']): 
            core.quit()
            # assigns response to corresponding image
    responses[imageList.index(image)] = myRatingScale.getRating() 

        # clear the screen & pause between ratings
    win.flip()
    core.wait(0.35)  # brief pause, slightly smoother for the subject

# Write to .csv file with participants name, subj_id, in file name
f=open( subj_id + ' task a results.csv','w')
for i in range(0,len(imageList)):
    f.write(imageList[i]+","+responses[i]+"\n")
f.close()

# Thank participant
thank_you_screen.draw()
win.flip()
core.wait(1.5)