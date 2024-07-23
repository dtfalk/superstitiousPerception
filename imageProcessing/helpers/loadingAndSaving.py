import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from imageProcessing.helpers.imports import *
from imageProcessing.helpers.constants import *


# loads templates into a cuda data object
def loadTemplates(templatesPath, imageDimensions):

    # extract the templates from the folder
    folderContents = os.listdir(templatesPath)

    # initialize cupy arrays to store the templates and the template names
    templates = zeros(shape = (len(folderContents), imageDimensions[0], imageDimensions[1]), dtype = uint8)
    templateNames = []

    # iterate over each file in the templates directory (iterate over each template)
    for i, filename in enumerate(folderContents):

        # load the template
        templatePath = os.path.join(templatesPath, filename)
        template = load(templatePath)

        # insert it to the array of templates and store its name
        templates[i] = template
        templateNames.append(filename.replace('.npy', ''))
                
    # return a cuda object storing all of the templates as a (numTemplaes x imageWidth x imageHeight)) sized array
    return templates, templateNames


# load stimuli into cuda objects
def loadStimuli(arrayPath):

    # load our numpy array with stimuli
    stimuli = load(arrayPath)

    # get the start and end index for these stimuli
    start = int(os.path.basename(arrayPath).replace('.npy', ''))
    end = start + batchSize

    return stimuli, start, end


# saves the indices info in a csv file
def writeIndicesToCsv(savePath, indicesDictionary):

    # file path for where to save the csv
    indicesFileCSVPath = os.path.join(savePath, 'indices.csv')

    # open the file and initialize a csv writing object
    with open(indicesFileCSVPath, 'w', newline='') as f:
        writer = csv.writer(f)

        # create and collect indices info
        for key, value in indicesDictionary.items():
            writer.writerow([key, value])
