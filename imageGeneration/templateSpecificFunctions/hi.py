import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from imports import *
from constants import *

# consts for height and width of template H
# Note: template I is just template H but rotated
middleBarHeight = 2
sideBarsWidths = 3

# creates/returns the path to where we save the images and the arrays (within a "stimuli" folder).
def createSavePaths():

    # current path to this file
    curDir = os.path.dirname(__file__)

    # paths to the various template folders
    ImagePathH = os.path.join(curDir, '..', '..', 'arraysAndImages', 'templates', 'hiAnalysis', 'images')
    ArrayPathH = os.path.join(curDir, '..', '..', 'arraysAndImages', 'templates', 'hiAnalysis','arrays')
    ImagePathI = os.path.join(curDir, '..', '..', 'arraysAndImages', 'templates', 'hiAnalysis', 'images')
    ArrayPathI = os.path.join(curDir, '..', '..', 'arraysAndImages', 'templates', 'hiAnalysis','arrays')
    templatePaths = [ImagePathH, ArrayPathH, ImagePathI, ArrayPathI]

    # create the directory for each of the stimlus/template paths defined above
    for path in templatePaths:
        os.makedirs(name = path, exist_ok = True)
    
    # return all of the various paths
    return templatePaths

# returns true if a pixel is in the template H and therefore should be colored black
def inTemplate(row, col):
    widthCenter = imageWidth // 2
    heightCenter = imageHeight // 2

    # Middle bar of the "H"
    if abs(row - heightCenter) <= middleBarHeight and abs(col - widthCenter) < imageWidth // 4:
        return True
    # Side bars of the "H"
    elif ((imageWidth // 4 <= col <= imageWidth // 4 + 2 * sideBarsWidths) or
          (3 * imageWidth // 4 - 2 * sideBarsWidths <= col <= 3 * imageWidth // 4)) and \
         abs(row - heightCenter) <= imageHeight // 4:
        return True
    
    return False



# creates the full screen template images for comparison
def createHandITemplates(templateImagePathH, templateArrayPathH, templateImagePathI, templateArrayPathI):

    # create empty array (white)
    array = np.ones((imageHeight, imageWidth), dtype = np.uint8)
    
    for i, row in enumerate(array):
        for j, _ in enumerate(row):
            if inTemplate(i, j):
                array[i][j] = 0
    
    # create H image and save
    imageNameH = os.path.join(templateImagePathH, 'H.png')
    imageH = Image.fromarray((array * 255).astype(np.uint8), 'L')
    imageH.save(imageNameH)
    imageH.close()
    
    # save H array
    arrayNameH = os.path.join(templateArrayPathH, 'H.npy')
    np.save(arrayNameH, array)

    # create I image and save
    imageNameI = os.path.join(templateImagePathI, 'I.png')
    imageI = Image.fromarray((array * 255).astype(np.uint8).T, 'L')
    imageI.save(imageNameI)
    imageI.close()
    
    # save array
    arrayNameI = os.path.join(templateArrayPathI, 'I.npy')
    np.save(arrayNameI, array.T)

def main():
    # clock for checking runtime on the device running the code
    startTime = time.time()

    # the various relevant paths for where to save images
    ImagePathH, ArrayPathH, ImagePathI, ArrayPathI = createSavePaths()
    
    createHandITemplates(ImagePathH, ArrayPathH, ImagePathI, ArrayPathI)


    # print the total time to estimate overall runtime
    totalTime = time.time() - startTime
    print('        Runtime for H and I templates: %.4f seconds'%totalTime)

if __name__ == '__main__':
    main()