import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from imports import *
from constants import *

# add the template S image and create the array
def addSTemplate(imagesPath, arraysPath):
    
    # path to the template S used by Shannon and co.
    curDir = os.path.dirname(__file__)
    OGImagePath = os.path.join(curDir, 'S_temp.png')

    # create the array and then save it
    image = Image.open(OGImagePath).convert('L')
    array = np.array(image, dtype = np.uint8) // 255
    image.close()

    # Pad the array to 51x51 with white pixels (value 1) at the bottom and right edges
    padWidth = ((0, 1), (0, 1))
    paddedArray = np.pad(array, padWidth, mode = 'constant', constant_values = 1)
    for i, pixel in enumerate(paddedArray[-1]):
        if abs(i - (imageWidth // 2)) <= 4:
            paddedArray[-1][i] = 0
    arraySavePath = os.path.join(arraysPath, 'S.npy')
    np.save(arraySavePath, paddedArray)

    # copy the image to the image directory
    paddedImage = Image.fromarray(paddedArray * 255, mode = 'L')
    paddedImage.save(os.path.join(imagesPath, 'S.png'))
    paddedImage.close()

def main():
    startTime = time.time()

    # get save path for images and arrays
    curDir = os.path.dirname(__file__)
    imagesPath = os.path.join(curDir, '..', '..', 'arraysAndImages', 'templates', 'S', 'images')
    arraysPath = os.path.join(curDir, '..', '..', 'arraysAndImages', 'templates', 'S', 'arrays')
    os.makedirs(imagesPath, exist_ok = True)
    os.makedirs(arraysPath, exist_ok = True)

    # copy image and create array
    addSTemplate(imagesPath, arraysPath)

    print('        Runtime for S template: %.4f seconds'%(time.time() - startTime))


if __name__ == '__main__':
    main()