# takes the numpy (.npy) arrays from our pearson score CSVs and generates CSVs
# so that we as humans can read them
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crossCorrelations.helpers.helperFunctions import *


# get paths for loading the data and the overall folder we will save it in
def getPaths():

    # current directory of this file
    curDir = os.path.dirname(__file__)

    # where we load CSV data from about the top stimuli
    loadPath = os.path.join(curDir, '..', '..', '..', 'results', 'S', 'results')

    # parent directory where we will save our data to
    savePath = os.path.join(curDir, '..', '..', '..', 'results', 'S', 'results')

    return loadPath, savePath


def main():

    startTime = time.time()

    # get our loading and saving paths
    loadPath, savePath = getPaths()

    # create the composite images of the top stimuli for each scheme combination
    crossCorrelations(loadPath, savePath)

    print('            Runtime for S template cross-correlations: %.4f seconds'%(time.time() - startTime))


if __name__ == '__main__':
    main()