# takes the numpy (.npy) arrays from our pearson score CSVs and generates CSVs
# so that we as humans can read them
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from compositeImages.helpers.helperFunctions import *


# get paths for loading the data and the overall folder we will save it in
def getPaths():

    # current directory of this file
    curDir = os.path.dirname(__file__)

    # where we load CSV data from about the top stimuli
    CSVPath = os.path.join(curDir, '..', '..', '..', 'results', 'fullscreenCrosses', 'results')

    # data path for the actual arrays given by the stimuli numbers
    arrayPath = os.path.join(curDir, '..', '..', '..', 'arraysAndImages', 'stimuli', 'arrays')

    # parent directory where we will save our data to
    savePath = os.path.join(curDir, '..', '..', '..', 'results', 'fullscreenCrosses', 'results')

    return CSVPath, arrayPath, savePath


def main():

    startTime = time.time()
    
    # get our loading and saving paths
    CSVPath, arrayPath, savePath = getPaths()

    # create the composite images of the top stimuli for each scheme combination
    compositeImages(CSVPath, arrayPath, savePath)
    print('            Runtime for fullscreen crosses composite images: %.4f seconds'%(time.time() - startTime))


if __name__ == '__main__':
    main()