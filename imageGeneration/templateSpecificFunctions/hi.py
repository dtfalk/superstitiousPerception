import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from imageGeneration.imports import *
from imageGeneration.constants import *

# consts for height and width of template H
# Note: template I is just template H but rotated
middleBarHeight = 2
sideBarsWidths = 3

# creates/returns the path to where we save the images and the arrays (within a "stimuli" folder).
def createSavePaths():

    # current path to this file
    curDir = os.path.dirname(__file__)

    # paths to the various template folders
    imagePath = os.path.join(curDir, '..', '..', 'arraysAndImages', 'templates', 'hiAnalysis', 'images')
    arrayPath = os.path.join(curDir, '..', '..', 'arraysAndImages', 'templates', 'hiAnalysis','arrays')
    templatePaths = imagePath, arrayPath

    # create the directory for each of the stimlus/template paths defined above
    for path in templatePaths:
        os.makedirs(name = path, exist_ok = True)
    
    # return all of the various paths
    return templatePaths

# returns true if a pixel is in the template H and therefore should be colored black
def inTemplateH(row, col):
    widthCenter = imageWidth // 2
    heightCenter = imageHeight // 2

    # Middle bar of the "H"
    if abs(row - heightCenter) <= middleBarHeight and abs(col - widthCenter) < imageWidth // 4:
        return True
    
    # Side bars of the "H"
    elif ((imageWidth // 4 <= col <= imageWidth // 4 + 2 * sideBarsWidths) or (3 * imageWidth // 4 - 2 * sideBarsWidths <= col <= 3 * imageWidth // 4))\
        and \
         (abs(row - heightCenter) <= imageHeight // 4 or row == 12):
        return True
    
    return False

# returns true if a pixel is in the template V and therefore should be colored black
def inTemplateV(row, col):

    lineThickness = 5

    # Calculate the center of the image
    widthCenter = imageWidth // 2
    heightCenter = imageHeight // 2

    # Define the top and bottom points of the "V"
    topY = heightCenter - imageHeight // 4  - 1 # Top of the "V"
    bottomY = heightCenter + imageHeight // 4 # Bottom of the "V"

    # Define the left and right bounds for the "V"
    rightX = widthCenter + imageWidth // 4  - 1 # Rightmost edge of the "V"

    # Calculate the slopes for the right lines
    rightSlope = (bottomY - topY) / (rightX - widthCenter)

    # just get a mirror image of the left slode
    if col > 24:
        return inTemplateV(row, 49 - col)
    # Check if the pixel lies on the right slanted line of the "V"
    if col <= widthCenter and (bottomY >= row >= topY) and abs((row - bottomY) - rightSlope * (col - widthCenter)) <= lineThickness:
        return True

    return False

# returns true if a pixel is in the template O and therefore should be colored black
def inTemplateO(row, col):

    circleThickness = 5
    radius = 14

    # Calculate the center of the image
    widthCenter = imageWidth // 2
    heightCenter = imageHeight // 2

    if row > 24 and col > 24:
        return inTemplateO(49 - row, 49 - col)
    elif row > 24:
        return inTemplateO(49 - row, col)
    elif col > 24: 
        return inTemplateO(row, 49 - col)
    # Check if the pixel lies on the right slanted line of the "V"
    if (radius - circleThickness) **2 <= abs((row - heightCenter)**2 + (col - widthCenter)**2) <= radius**2:
        if row < 12 or col < 12:
            return False 
        return True

    return False



# creates the full screen template images for comparison
def createHandITemplates(imagePath, arrayPath):

    # create empty array (white)
    arrayH = np.ones((imageHeight, imageWidth), dtype = np.uint8)
    
    for i, row in enumerate(arrayH):
        for j, _ in enumerate(row):
            if inTemplateH(i, j):
                arrayH[i][j] = 0
    
    # create H image and save
    imageNameH = os.path.join(imagePath, 'H.png')
    imageH = Image.fromarray((arrayH * 255).astype(np.uint8), 'L')
    imageH.save(imageNameH)
    imageH.close()
    
    # save H array
    arrayNameH = os.path.join(arrayPath, 'H.npy')
    np.save(arrayNameH, arrayH)

    # create I image and save
    imageNameI = os.path.join(imagePath, 'I.png')
    imageI = Image.fromarray((arrayH * 255).astype(np.uint8).T, 'L')
    imageI.save(imageNameI)
    imageI.close()
    
    # save array
    arrayNameI = os.path.join(arrayPath, 'I.npy')
    np.save(arrayNameI, arrayH.T)


    #################################################
    #################################################

    # create empty array (white)
    arrayV = np.ones((imageHeight, imageWidth), dtype = np.uint8)
    
    for i, row in enumerate(arrayV):
        for j, _ in enumerate(row):
            if inTemplateV(i, j):
                arrayV[i][j] = 0
    
    # create V image and save
    imageNameV = os.path.join(imagePath, 'V.png')
    imageV = Image.fromarray((arrayV * 255).astype(np.uint8), 'L')
    imageV.save(imageNameV)
    imageV.close()
    
    # save V array
    arrayNameV = os.path.join(arrayPath, 'V.npy')
    np.save(arrayNameV, arrayV)

    #################################################
    #################################################

    # create empty array (white)
    arrayO = np.ones((imageHeight, imageWidth), dtype = np.uint8)
    
    for i, row in enumerate(arrayO):
        for j, _ in enumerate(row):
            if inTemplateO(i, j):
                arrayO[i][j] = 0
    
    # create V image and save
    imageNameO = os.path.join(imagePath, 'O.png')
    imageO = Image.fromarray((arrayO * 255).astype(np.uint8), 'L')
    imageO.save(imageNameO)
    imageO.close()
    
    # save V array
    arrayNameO = os.path.join(arrayPath, 'O.npy')
    np.save(arrayNameO, arrayO)


    #################################################
    #################################################

    # Handling the S we created
    imageS = Image.open(os.path.join(os.path.dirname(__file__), 'S.png')).convert('L')
    arrayS = np.array(imageS) // 255
    imageS = Image.fromarray((arrayS * 255).astype(np.uint8), 'L')
    imageS.save(os.path.join(imagePath, 'S.png'))
    np.save(os.path.join(arrayPath, 'S.npy'), arrayS)



def main():
    # clock for checking runtime on the device running the code
    startTime = time.time()

    # the various relevant paths for where to save images
    imagePath, arrayPath = createSavePaths()
    
    createHandITemplates(imagePath, arrayPath)


    # print the total time to estimate overall runtime
    totalTime = time.time() - startTime
    print('        Runtime for H and V templates: %.4f seconds'%totalTime)

if __name__ == '__main__':
    main()