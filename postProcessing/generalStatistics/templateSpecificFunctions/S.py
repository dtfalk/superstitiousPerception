# takes the numpy (.npy) arrays from our pearson score CSVs and generates CSVs
# so that we as humans can read them
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from generalStatistics.helpers.helperFunctions import *


# get paths for loading the data and the overall folder we will save it in
def getPaths():

    # current directory of this file
    curDir = os.path.dirname(__file__)

    # where we load numpy (npy) data from about the S template and the stored indices data
    loadAndSavePath = os.path.join(curDir, '..', '..', '..', 'results', 'S', 'results')

    return loadAndSavePath


def main():

    startTime = time.time()

    # get our loading and saving paths
    loadAndSavePath = getPaths()

    # create the statistic CSVs for each scheme combination
    loadAndSave(loadAndSavePath)

    print('            Runtime for S template general statistics: %.4f seconds'%(time.time() - startTime))

if __name__ == '__main__':
    main()