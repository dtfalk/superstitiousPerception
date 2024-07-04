import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers.imports import *
from helpers.constants import *
from helpers.weightsAndDistances import *
from helpers.loadingAndSaving import *
from helpers.batching import *

# get the save and loading paths
def getPaths():

    # directory of THIS file
    curDir = os.path.dirname(__file__)

    # paths to the templates and the stimuli
    templatePath = os.path.join(curDir, '..', '..', 'arraysAndImages', 'templates', 'hiAnalysis', 'arrays')
    stimuliPath = os.path.join(curDir, '..', '..', 'arraysAndImages', 'stimuli', 'arrays')

    # path to where we will store our results and create the directory if necessary
    savePath = os.path.join(curDir, '..', '..', 'results', 'hiAnalysis')
    os.makedirs(savePath, exist_ok = True)

    # return the paths
    return templatePath, stimuliPath, savePath


# main portion of the code (look here for general code flow/structure)
def main():

    imageDimensions = (51, 51)

    # start time so we can track how long it takes the code to run in the terminal
    startTime = time.time()

    # get the saving and loading paths
    templatesPath, stimuliPath, savePath = getPaths()

    # load the templates and get the template names
    templates, templateNames = loadTemplates(templatesPath, imageDimensions)

    # get the weight matrices and the weighted means of the templates (and the 3-tuple to index crosswalk)
    weightMatrices, weightedMeanDifferences, summedWeightMatrices, indicesDictionary = getWeightMatrices(templates, templateNames, imageDimensions)

    # preload the results array
    results = zeros(shape = (numImages, len(templates) * len(weightingSchemes) * len(relevantPointSchemes)), dtype = float32)


    for arrayPath in os.listdir(stimuliPath):
        processAndStoreResults(os.path.join(stimuliPath, arrayPath), weightMatrices, weightedMeanDifferences, summedWeightMatrices, results)

    # save the fully populated cupy results array as a numpy array
    save(os.path.join(savePath, 'hiAnalysis.npy'), results)

    # write the 3-tuple to indices dictionary to a csv file
    writeIndicesToCsv(savePath, indicesDictionary)
    
    # print runtime for the entire process
    print("        Runtime for H/I/Features: %.4f seconds"%(time.time() - startTime))

 
if __name__ == '__main__':
    main()