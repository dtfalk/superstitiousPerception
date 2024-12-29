import os
import math
from screeninfo import get_monitors

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

screenCenter = (winWidth // 2, winHeight // 2)


os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (winX, winY)

# Get the size in pixels for 2 degrees of visual angle
# bc the jackasses at psychopy have made this process insufferable
def deg2pix(degrees):
    return 51
    screen_width = monitor.getWidth()
    
    # Calculate the total visual angle subtended by the screen width in degrees
    total_visual_angle_width = 2 * math.degrees(math.atan(screen_width / (2 * monitor.getDistance())))
    
    # Calculate the number of pixels per degree
    pixels_per_degree = monitor.getSizePix()[0] / total_visual_angle_width
    
    return degrees * pixels_per_degree

stim_size_degrees = 2
stimSize = round(deg2pix(stim_size_degrees))


# define some font sizes and colors for easy access

# == Font sizes ==
extraLargeFont = winHeight // 5
largeFont = winHeight // 10
mediumFont = winHeight // 20
smallFont = winHeight // 30

# == Greyscale ==
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREY = [128, 128, 128]
SLATEGREY = [112, 128, 144]
DARKSLATEGREY = [47, 79, 79]


# == Yellows ==
YELLOW = [255, 255, 0]
OLIVE = [128,128,0]
DARKKHAKI = [189,183,107]

# == Greens ==
GREEN = [0, 128, 0]
GREENYELLOW = [173, 255, 47]

RED = [255, 50, 50]


backgroundColor = GREY # background color for screen
textColor = BLACK # text color

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

explanationText = 'In this task you will be shown a series of squares which contain a pattern of black and white dots. \
In half of the trials, a black H will be present in the pattern. You will be asked to determine whether or not the H is in the image. \
It will be very difficult to make this determination, but trust your intuition. \
The H will not be obvious, but it is always centered, and you will be shown an image of the H for reference before you begin.\n\n\
For each image, please press "Y" if you believe that you see the H and \
press "N" if you do not believe that you see the H.\n\n\
Remember, you will be better at this task than you think.\n\n\
Thank you for participating and please let your experimenter know if you encounter any issues or if you would like to terminate your participation in the experiment.\n\n\
Press the spacebar to continue.\n\n\n'
                
realText = 'Remember to press "Y" if you believe that you see an H.\n\n\
Remember to press "N" if you do not believe that you see an H.\n\n\
You will now be shown the template H that will be in half of the stimuli.\n\n\
You will have 10 seconds to view the template H.\n\n\
After those 10 seconds, the first image will automatically appear and you will begin making your selections.\n\n\
Press the spacebar to continue when you are ready.'

breakScreenText = 'You have earned a break.\n\nPlease let the experimenter know.\n\n\
When you are ready you will be shown the template again and resume your task.\n\n'

exitScreenText = 'Thank you for participating in this study!\n\n'\
'Please notify the experimenter that you have completed the study.\n\n'\
# =======================================================================
# =======================================================================



# map the weighting scheme/correlation scheme pair to the actual path to the images
ImageFolderPathDict = {
        ('unweighted', 'icorrelated', 'target'): 'unweightedICorrelatedH',
        ('unweighted', 'icorrelated', 'distractor'): 'unweightedI',
        ('unweighted', 'uncorrelated', 'target'): 'unweightedUncorrelatedH',
        ('unweighted', 'uncorrelated', 'distractor'): 'unweightedUncorrelated',
        ('gaussian', 'icorrelated', 'target'): 'gaussianICorrelatedH',
        ('gaussian', 'icorrelated', 'distractor'): 'gaussianI',
        ('gaussian', 'uncorrelated', 'target'): 'gaussianUncorrelatedH',
        ('gaussian', 'uncorrelated', 'distractor'): 'gaussianUncorrelated',
    }                
    

 