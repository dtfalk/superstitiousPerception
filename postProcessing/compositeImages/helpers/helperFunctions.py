import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from compositeImages.helpers.imports import *
from multiprocessing import Pool
import pandas as pd
import numpy as np
import os
from PIL import Image

imageWidth, imageHeight = 51, 51
batchSize = 1000
validFolderNames = ['anyAll', 'borders', 'gaussian', 'linear', 'quadratic', 'unweighted', 'logarithmic', 'central']

# Worker function to process a single folder
def processSingleFolder(args):
    csvPath, arrayPath, savePath, templateFolder, relevantPointSchemeFolder, weightingSchemeFolder = args

    pearsonScoresPath = os.path.join(csvPath, templateFolder, relevantPointSchemeFolder, weightingSchemeFolder, 'pearsonScores.csv')
    
    # Extract the stimulus numbers of the top 1000 and lowest 1000 stimuli for this scheme
    df = pd.read_csv(pearsonScoresPath)
    top1000 = df.head(1000)['Stimulus Number'].to_numpy()
    low1000 = df.abs().sort_values(by='Stimulus Number', ascending=False).head(1000)['Stimulus Number'].to_numpy()

    # Initialize arrays for the composite images
    arrayTop1000 = np.zeros((imageHeight, imageWidth), dtype=np.float32)
    arrayTop100 = np.zeros((imageHeight, imageWidth), dtype=np.float32)
    arrayTop10 = np.zeros((imageHeight, imageWidth), dtype=np.float32)
    arrayLow1000 = np.zeros((imageHeight, imageWidth), dtype=np.float32)
    arrayLow100 = np.zeros((imageHeight, imageWidth), dtype=np.float32)
    arrayLow10 = np.zeros((imageHeight, imageWidth), dtype=np.float32)

    # Function to process a batch of stimuli
    def processStimuli(stimuli, array1000, array100, array10):
        batchCache = {}
        for i, stimulusNumber in enumerate(stimuli):
            batchNumber = (stimulusNumber // batchSize) * batchSize
            batchIndex = stimulusNumber % batchSize

            if batchNumber not in batchCache:
                batchCache[batchNumber] = np.load(os.path.join(arrayPath, f'{batchNumber}.npy'))

            stimulus = batchCache[batchNumber][batchIndex] * 255

            array1000 += stimulus
            if i < 100:
                array100 += stimulus
                if i < 10:
                    array10 += stimulus

    # Process top and low stimuli
    processStimuli(top1000, arrayTop1000, arrayTop100, arrayTop10)
    processStimuli(low1000, arrayLow1000, arrayLow100, arrayLow10)

    # Compute averages for the composite images
    arrayTop1000 /= 1000
    arrayTop100 /= 100
    arrayTop10 /= 10
    arrayLow1000 /= 1000
    arrayLow100 /= 100
    arrayLow10 /= 10

    # Convert arrays to images
    top1000Image = Image.fromarray(arrayTop1000.astype(np.uint8), mode='L')
    top100Image = Image.fromarray(arrayTop100.astype(np.uint8), mode='L')
    top10Image = Image.fromarray(arrayTop10.astype(np.uint8), mode='L')
    low1000Image = Image.fromarray(arrayLow1000.astype(np.uint8), mode='L')
    low100Image = Image.fromarray(arrayLow100.astype(np.uint8), mode='L')
    low10Image = Image.fromarray(arrayLow10.astype(np.uint8), mode='L')

    # Save images
    imageSavePathTop = os.path.join(savePath, templateFolder, relevantPointSchemeFolder, weightingSchemeFolder, 'compositeImages', 'top')
    imageSavePathLow = os.path.join(savePath, templateFolder, relevantPointSchemeFolder, weightingSchemeFolder, 'compositeImages', 'bottom')
    os.makedirs(imageSavePathTop, exist_ok=True)
    os.makedirs(imageSavePathLow, exist_ok=True)

    top1000Image.save(os.path.join(imageSavePathTop, '1000.png'))
    top100Image.save(os.path.join(imageSavePathTop, '100.png'))
    top10Image.save(os.path.join(imageSavePathTop, '10.png'))
    low1000Image.save(os.path.join(imageSavePathLow, '1000.png'))
    low100Image.save(os.path.join(imageSavePathLow, '100.png'))
    low10Image.save(os.path.join(imageSavePathLow, '10.png'))

# Function to create a list of all folder paths to process
def getFolderPaths(csvPath, arrayPath, savePath):
    folderPaths = []
    for templateFolder in os.listdir(csvPath):
        for relevantPointSchemeFolder in os.listdir(os.path.join(csvPath, templateFolder)):
            if relevantPointSchemeFolder in validFolderNames:
                for weightingSchemeFolder in os.listdir(os.path.join(csvPath, templateFolder, relevantPointSchemeFolder)):
                    if weightingSchemeFolder in validFolderNames:
                        folderPaths.append((csvPath, arrayPath, savePath, templateFolder, relevantPointSchemeFolder, weightingSchemeFolder))
    return folderPaths

# Main function for creating the composite images
def compositeImages(csvPath, arrayPath, savePath):
    folderPaths = getFolderPaths(csvPath, arrayPath, savePath)

    # Use a pool of workers to process folders in parallel
    with Pool() as pool:
        pool.map(processSingleFolder, folderPaths)
