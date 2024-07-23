import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from imageGeneration.imports import *
from imageGeneration.constants import *



# creates/returns the path to where we save the images and the arrays (within a "stimuli" folder).
def createSavePaths():

    # current path to this file
    curDir = os.path.dirname(__file__)

    # generate and create path to full screen cross images
    imagesPath = os.path.join(curDir, '..', '..', 'arraysAndImages', 'templates', 'fullscreenCrosses', 'images')
    os.makedirs(name = imagesPath, exist_ok = True)

    # generate and create path to full screen images
    arraysPath = os.path.join(curDir, '..', '..', 'arraysAndImages', 'templates', 'fullscreenCrosses', 'arrays')
    os.makedirs(name = arraysPath, exist_ok = True)

    
    # return iamges and arrays path
    return imagesPath, arraysPath

# creates the full screen template images for comparison
def createFullScreenTemplates(imagesPath, arraysPath):
    
    # find screen center (// is floor division)
    widthCenter = imageWidth // 2
    heightCenter = imageHeight // 2

    # make template images for all widths
    for width in widths:
        
         # create empty array (white)
        array = np.ones((imageHeight, imageWidth), dtype = np.uint8)
        
        for j, row in enumerate(array):
            for k, _ in enumerate(row):

                # Note: heightCenter is the horizontal line and widthCenter is the vertical line
                if abs(j - heightCenter) <= width or abs(k - widthCenter) <= width:
                    array[j][k] = 0
    
        # create image and save
        imageName = os.path.join(imagesPath, '%d.png'%((width * 2) + 1))
        image = Image.fromarray((array * 255).astype(np.uint8), 'L')
        image.save(imageName)
        image.close()
        
        # save array
        arrayName = os.path.join(arraysPath, '%d.npy'%((width * 2) + 1))
        np.save(arrayName, array)

def main():
    
    # clock for checking runtime on the device running the code
    startTime = time.time()

    # the various relevant paths for where to save images
    imagesPath, arraysPath = createSavePaths()

    # create the template crosses that span the full screen
    createFullScreenTemplates(imagesPath, arraysPath)

    # print the total time to estimate overall runtime
    totalTime = time.time() - startTime
    print('        Runtime for fullscreen crosses: %.4f seconds'%totalTime)

if __name__ == '__main__':
    main()