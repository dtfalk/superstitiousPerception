import os
from screeninfo import get_monitors

backgroundColor = (1,1,1) # background color for screen
altBackgroundColor = (int((253 * 2/ 255)) - 1 , int((253 * 2/ 255)) - 1, int((150 * 2/ 255)) - 1)
textColor = (0, 0, 0) # text color

continueKey = 'space'
quitKey = 'escape'
breakScreenKey = 'k'

# This block of code gets info about the subject's monitor
# =======================================================================
# =======================================================================

# get screen size for each monitor in the system
winfo = get_monitors()
if len(winfo) > 1:
    winX = winfo[1].x
    winY = winfo[1].y
    winWidth = winfo[1].width
    winHeight = winfo[1].height

else:
    winX = winfo[0].x
    winY = winfo[0].y
    winWidth = winfo[0].width
    winHeight = winfo[0].height


os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (winX, winY)

# =======================================================================
# =======================================================================

# This block of code defines the valid characters and numbers for text entry
# =======================================================================
# =======================================================================

# getting the valid letters and numbers for user info.
def getValidChars():
    validLetters = []
    validNumbers = []
    
    # valid digits (0 - 9)
    for i in range(48, 58):
        validNumbers.append(chr(i))
        
    # valid lowercase letters (a - z)
    for i in range(97, 123):
        validLetters.append(chr(i))
        
    # valid uppercase letters (A - Z)
    for i in range(65, 91):
        validLetters.append(chr(i))
    
    return validLetters, validNumbers

validLetters, validNumbers = getValidChars()

# =======================================================================
# =======================================================================


# This block of code contains the text for explanation screens
# =======================================================================
# =======================================================================

def explanationText(letter):
    return f'In this task we will show you images for you to judge as a part of ongoing research into the limits of human perception. \
Many people have described this task as feeling impossible, but do your best and you will do great. \
Indeed, our previous research shows that you will perform much better than you think you are performing while you play. \
Trust your intuitions and listen to that little voice in your head that is trying to tell you the answer! It is right more often than you think. \
This task may feel like trying to read a street sign that is a little bit too far away, listening for your phone to buzz while you are in the shower, or wondering if you heard someone mention you in a conversation in the next room. \n\n\
This task will ask you to identify which images have an "{letter}" hidden in them. The "{letter}" will not be obvious, but it is always centered and looks exactly like the template "{letter}" we will show you before you begin.\n\n\
For each image, please press "Y" if you believe that you see an "{letter}" in the middle of the image and \
press "N" if you do not believe that you see an "{letter}" hidden in the middle of the image.\n\n\
Remember, humans are better at this sort of task than one might think!\n\n\
Thank you for participating and please let your experimenter know if you encounter any issues or if you would like to terminate your participation in the experiment.\n\n\
Press the spacebar to continue.\n\n\n'
                
def realText(letter): 
    return f'Remember to press "Y" if you believe that you see an "{letter}".\n\n\
Remember to press "N" if you do not believe that you see an "{letter}".\n\n\
You will now be shown the template "{letter}" that will be hidden in some of the stimuli.\n\n\
You will have 10 seconds to view the template "{letter}".\n\n\
After those 10 seconds, the first image will automatically appear and you will begin making your selections.\n\n\
Press the spacebar to continue when you are ready.'

breakScreenText = 'You have earned a break.\n\nPlease let the experimenter know.\n\n\
When you are ready you will be shown the template again and resume your task.\n\n'

exitScreenText = 'Thank you for participating in this study!\n\n'\
'Please notify the experimenter that you have completed the study.\n\n'\
# =======================================================================
# =======================================================================



                        
    

 