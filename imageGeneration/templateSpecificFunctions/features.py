import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from imports import *
from constants import *

# feature names
features = ['Left', 'Right', 'Top', 'Bottom', 'Horizontal', 'Vertical']

# consts for height and width of template H
# Note: template I is just template H but rotated
middleBarHeight = 2
sideBarsWidths = 3

# creates/returns the path to where we save the images and the arrays (within a "stimuli" folder).
def createSavePaths():

    # current path to this file
    curDir = os.path.dirname(__file__)

    # paths to the various template folders
    imagesPath = os.path.join(curDir, '..', '..', 'arraysAndImages', 'templates', 'hiAnalysis', 'images')
    arraysPath = os.path.join(curDir, '..', '..', 'arraysAndImages', 'templates', 'hiAnalysis', 'arrays')

    templatePaths = [imagesPath, arraysPath]

    # paths to the stimuli folders

    # create the directory for each of the stimlus/template paths defined above
    for path in templatePaths:
        os.makedirs(name = path, exist_ok = True)
    
    # return all of the various paths
    return templatePaths

# checks if a given pixel is within the template feature
def inTemplate(row, col, feature):
    if feature == 'Left' or feature == 'Top':
        if (imageWidth // 4 <= col <= (imageWidth // 4  + 2 * sideBarsWidths)) and abs(row - heightCenter) <= imageHeight // 4:
            return True
    elif feature == 'Right' or feature == 'Bottom':
        if (3 * imageWidth // 4) - 2 * sideBarsWidths <=  col <= 3 * imageWidth // 4 and abs(row - heightCenter) <= imageHeight // 4:
            return True
    elif feature == 'Horizontal' or feature == 'Vertical':
        if abs(row - heightCenter) <= middleBarHeight and abs(col - widthCenter) < imageWidth // 4:
            return True
    return False

# creates the full screen template images for comparison
def createFeaturesTemplates(templateImagePath, templateArrayPath, feature):

    # create empty array (white)
    array = np.ones((imageHeight, imageWidth), dtype = np.uint8)
    
    for i, row in enumerate(array):
        for j, _ in enumerate(row):
            if inTemplate(i, j, feature):
                array[i][j] = 0
    
    if feature == 'Top' or feature == 'Bottom' or feature == 'Vertical':
        arrayNew = array.T
    else:
        arrayNew = array.copy()
    
    # create image and save
    imageName = os.path.join(templateImagePath, '%s.png'%feature)
    image = Image.fromarray((arrayNew * 255).astype(np.uint8), 'L')
    image.save(imageName)
    image.close()
    
    # save array
    arrayName = os.path.join(templateArrayPath, '%s.npy'%feature)
    np.save(arrayName, arrayNew)

def main():
    
    # clock for checking runtime on the device running the code
    startTime = time.time()

    # the various relevant paths for where to save images
    imagesPath, arraysPath = createSavePaths()
    
    for feature in features:
        createFeaturesTemplates(imagesPath, arraysPath, feature)

    # print the total time to estimate overall runtime
    totalTime = time.time() - startTime
    print('        Runtime for features templates: %.4f seconds'%totalTime)

if __name__ == '__main__':
    main()