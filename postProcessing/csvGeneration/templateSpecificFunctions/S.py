# takes the numpy (.npy) arrays from our pearson score CSVs and generates CSVs
# so that we as humans can read them
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from csvGeneration.helpers.helperFunctions import *


# get paths for loading the data and the overall folder we will save it in
def getPaths():

    # current directory of this file
    curDir = os.path.dirname(__file__)

    # where we load numpy (npy) data from about the S image and the stored indices data
    dataLoadPath = os.path.join(curDir, '..', '..', '..', 'results', 'S', 'S.npy')
    indicesLoadPath = os.path.join(curDir, '..', '..', '..', 'results', 'S', 'indices.csv')

    # folder where we will save csv files to
    savePath = os.path.join(curDir, '..', '..', '..', 'results', 'S', 'results')
    os.makedirs(savePath, exist_ok = True)

    return dataLoadPath, indicesLoadPath, savePath

    
def main():

    # get our loading and saving paths
    startTime = time.time()

    # get our loading and saving paths
    dataLoadPath, indicesLoadPath, savePath = getPaths()

    # get indices data as a dicitonary with keys being of the form templateName_relevantPointScheme_weightingScheme
    indicesDictionary = loadIndexData(indicesLoadPath)

    # loads the numpy file with the pearson correlation data
    pearsonData = np.load(dataLoadPath)

    # create the CSVs for each scheme combination
    createCSVs(pearsonData, indicesDictionary, savePath)

    print('            Runtime for extracting S template Pearson CSV data: %.4f seconds'%(time.time() - startTime))

if __name__ == '__main__':
    main()