import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from generalStatistics.helpers.imports import *

validFolderNames = ['anyAll', 'borders', 'gaussian', 'linear', 'quadratic', 'unweighted', 'logarithmic', 'central']

# Worker function to process a single folder
def processSingleFolder(args):
    templateFolder, relevantPointSchemeFolder, weightSchemeFolder, loadAndSavePath = args

    curPath = os.path.join(loadAndSavePath, templateFolder, relevantPointSchemeFolder, weightSchemeFolder)
    filename = os.path.join(curPath, 'pearsonScores.csv')

    # Load the existing data into a pandas dataframe
    existingData = pd.read_csv(filename)

    # Get the min, max, range of the data set
    minVal = existingData.iloc[:, 1].min()
    maxVal = existingData.iloc[:, 1].max()
    rangeVal = abs(maxVal - minVal)

    # Get the mean and standard deviation of the data set
    meanVal = existingData.iloc[:, 1].mean()
    stdVal = existingData.iloc[:, 1].std()

    # Collect header and data as lists
    header = ['mean', 'std', 'max', 'min', 'range']
    data = [meanVal, stdVal, maxVal, minVal, rangeVal]

    # Write data to the CSV
    with open(os.path.join(curPath, 'statistics.csv'), mode = 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(data)

# Function to create a list of all folder paths to process
def getFolderPaths(loadAndSavePath):
    folderPaths = []
    for templateFolder in os.listdir(loadAndSavePath):
        templateFolderPath = os.path.join(loadAndSavePath, templateFolder)
        if os.path.isdir(templateFolderPath):
            for relevantPointSchemeFolder in os.listdir(templateFolderPath):
                if relevantPointSchemeFolder in validFolderNames:
                    relevantPointSchemeFolderPath = os.path.join(templateFolderPath, relevantPointSchemeFolder)
                    if os.path.isdir(relevantPointSchemeFolderPath):
                        for weightSchemeFolder in os.listdir(relevantPointSchemeFolderPath):
                            if weightSchemeFolder in validFolderNames:
                                weightSchemeFolderPath = os.path.join(relevantPointSchemeFolderPath, weightSchemeFolder)
                                if os.path.isdir(weightSchemeFolderPath):
                                    folderPaths.append((templateFolder, relevantPointSchemeFolder, weightSchemeFolder, loadAndSavePath))
    return folderPaths

# Main function to load existing CSV data, extract statistics, and save them
def loadAndSave(loadAndSavePath):
    folderPaths = getFolderPaths(loadAndSavePath)

    # Use a pool of workers to process folders in parallel
    with Pool() as pool:
        pool.map(processSingleFolder, folderPaths)
