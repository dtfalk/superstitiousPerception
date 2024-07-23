import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from imageGeneration.imports import *
from imageGeneration.constants import *

# Creates/returns the path to where we save the images and the arrays (within a "stimuli" folder).
def createSavePaths():
    # current path to this file
    curDir = os.path.dirname(__file__)
    imagesPath = os.path.join(curDir, '..', 'arraysAndImages', 'stimuli', 'images')
    arraysPath = os.path.join(curDir, '..', 'arraysAndImages', 'stimuli', 'arrays')
    stimulusPaths = [imagesPath, arraysPath]
    for path in stimulusPaths:
        os.makedirs(name=path, exist_ok=True)
    return stimulusPaths


# Function to save a single image and its array
def saveImage(image, stimuliNumber, imagesFolderPath):
    imageName = os.path.join(imagesFolderPath, f'{stimuliNumber}.png')
    image.save(imageName)
    image.close()

# takes an array and turns it into batchSize number of images
def createImages(array):
    images = []
    for imageArray in array:
        image = Image.fromarray((imageArray * 255), mode = 'L')
        images.append(image) 
    return images

# Function to save a batch of images using threading
def saveBatch(images, start, imagesPath):
    with concurrent.futures.ThreadPoolExecutor() as thread_executor:
        futures = []
        for k, image in enumerate(images):
            futures.append(thread_executor.submit(saveImage, image, start + k, imagesPath))
        for future in concurrent.futures.as_completed(futures):
            future.result()

# Function to create and save a batch of images
def createAndSaveBatch(start, imagesPath, arraysPath):

    # current batch starting number
    batchNumber = start
    
    # Create batch directories
    imageBatchPath = os.path.join(imagesPath, str(batchNumber))
    os.makedirs(imageBatchPath, exist_ok = True)

    # create our large array and save it
    array = np.random.randint(2, size = (batchSize, imageHeight, imageWidth), dtype = np.uint8)
    np.save(os.path.join(arraysPath, '%d.npy'%start), array)

    # create the images from each batch
    images = createImages(array)
    
    # save the images
    saveBatch(images, start, imageBatchPath)

def main():
    # clock for checking runtime on the device running the code
    startTime = time.time()

    # the various relevant paths for where to save images and arrays
    imagesPath, arraysPath = createSavePaths()

    # number of available cpus
    numCores = os.cpu_count()

    # Use ProcessPoolExecutor to parallelize image creation
    with concurrent.futures.ProcessPoolExecutor(max_workers = numCores) as executor:
        # Create a list of tasks for each image to be generated
        tasks = [executor.submit(createAndSaveBatch, i, imagesPath, arraysPath) for i in range(0, numImages, batchSize)]
        
        # Wait for all tasks to complete
        for task in concurrent.futures.as_completed(tasks):
            task.result()

    # print the total time to estimate overall runtime
    totalTime = time.time() - startTime
    print('        Runtime for %d stimuli: %.4f seconds' % (numImages, totalTime))

if __name__ == '__main__':
    main()
