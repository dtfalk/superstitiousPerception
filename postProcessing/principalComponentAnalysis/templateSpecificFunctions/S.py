import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.join(os.path.abspath(__file__))))))
from postProcessing.principalComponentAnalysis.helpers.imports import *
from postProcessing.principalComponentAnalysis.helpers.constants import *
from postProcessing.principalComponentAnalysis.helpers.helperFunctions import *



# gets parent directory for loading data and save path
def getPaths():

    curDir = os.path.dirname(__file__)
    loadPath = os.path.join(curDir, '..', '..', '..', 'results', 'S', 'results')
    savePath = os.path.join(curDir, '..', '..', '..', 'results', 'S', 'results')

    return loadPath, savePath

def main():

    startTime = time.time()

    # base paths for where we will load data from and save results to
    loadPath, savePath = getPaths()

    for templateName in os.listdir(loadPath):
        for distanceScheme in distanceSchemes:

            # collects the data from all of the weighting scheme folders in a given
            # template/distance scheme folder as a numpy array
            data = collectData(loadPath, 'S', templateName, distanceScheme)

            # Perform PCA
            n_components = 6
            principalComponents, explainedVariance = performPCA(data, n_components)

            # write the resulting principal components and explained variance to a file
            templateSaveFolder = os.path.join(savePath, templateName, distanceScheme, 'principalComponentAnalysis')
            os.makedirs(templateSaveFolder, exist_ok = True)
            writeData(principalComponents, explainedVariance, templateSaveFolder)

    print('            Runtime for S Principal Component Analysis: %.4f seconds'%(time.time() - startTime))

if __name__ == '__main__':
    main()