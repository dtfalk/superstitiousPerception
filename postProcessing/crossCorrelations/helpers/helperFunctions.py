import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crossCorrelations.helpers.imports import *

imageWidth, imageHeight = 51, 51
batchSize = 1000
validFolderNames = ['anyAll', 'borders', 'central', 'linear', 'gaussian', 'quadratic', 'logarithmic', 'unweighted']

# Worker function to process a single template folder
def processTemplateFolder(args):
    loadPath, savePath, templateFolder, relevantPointSchemeFolder = args

    dataDictAll = {}
    dataDict1000 = {}
    dataDict100 = {}
    dataDict10 = {}

    baseFolder = os.path.join(loadPath, templateFolder, relevantPointSchemeFolder)

    for weightingSchemeName in os.listdir(baseFolder):
        if weightingSchemeName not in validFolderNames:
            continue

        dataPath = os.path.join(baseFolder, weightingSchemeName, 'pearsonScores.csv')
        curData = pd.read_csv(dataPath)['Stimulus Number'].tolist()
        dataDictAll[weightingSchemeName] = curData
        dataDict1000[weightingSchemeName] = curData[:1000]
        dataDict100[weightingSchemeName] = curData[:100]
        dataDict10[weightingSchemeName] = curData[:10]

    header = ['']
    dataAllStats = []
    data1000Stats = []
    data100Stats = []
    data10Stats = []
    dataAllPValue = []
    data1000PValue = []
    data100PValue = []
    data10PValue = []

    for key1, value1 in dataDictAll.items():
        header.append(key1)
        rowAllStats = [key1]
        row1000Stats = [key1]
        row100Stats = [key1]
        row10Stats = [key1]
        rowAllPValue = [key1]
        row1000PValue = [key1]
        row100PValue = [key1]
        row10PValue = [key1]

        for key2, value2 in dataDictAll.items():
            crossCorrelationAll = spearmanr(value1, value2)
            rowAllStats.append(round(crossCorrelationAll.statistic, 5))
            rowAllPValue.append(round(crossCorrelationAll.pvalue, 5))

            crossCorrelation1000 = spearmanr(dataDict1000[key1], dataDict1000[key2])
            row1000Stats.append(round(crossCorrelation1000.statistic, 5))
            row1000PValue.append(round(crossCorrelation1000.pvalue, 5))

            crossCorrelation100 = spearmanr(dataDict100[key1], dataDict100[key2])
            row100Stats.append(round(crossCorrelation100.statistic, 5))
            row100PValue.append(round(crossCorrelation100.pvalue, 5))

            crossCorrelation10 = spearmanr(dataDict10[key1], dataDict10[key2])
            row10Stats.append(round(crossCorrelation10.statistic, 5))
            row10PValue.append(round(crossCorrelation10.pvalue, 5))

        dataAllStats.append(rowAllStats)
        data1000Stats.append(row1000Stats)
        data100Stats.append(row100Stats)
        data10Stats.append(row10Stats)
        dataAllPValue.append(rowAllPValue)
        data1000PValue.append(row1000PValue)
        data100PValue.append(row100PValue)
        data10PValue.append(row10PValue)

    filenames = ['all.csv', '1000.csv', '100.csv', '10.csv']
    overallDataStats = [dataAllStats, data1000Stats, data100Stats, data10Stats]
    overallDataPValues = [dataAllPValue, data1000PValue, data100PValue, data10PValue]
    saveFolderPathSpearman = os.path.join(savePath, templateFolder, relevantPointSchemeFolder, 'crossCorrelations', 'spearmanValues')
    saveFolderPathPValues = os.path.join(savePath, templateFolder, relevantPointSchemeFolder, 'crossCorrelations', 'pValues')
    os.makedirs(saveFolderPathSpearman, exist_ok=True)
    os.makedirs(saveFolderPathPValues, exist_ok=True)

    for i, filename in enumerate(filenames):
        with open(os.path.join(saveFolderPathSpearman, filename), mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for row in overallDataStats[i]:
                writer.writerow(row)

    for i, filename in enumerate(filenames):
        with open(os.path.join(saveFolderPathPValues, filename), mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for row in overallDataPValues[i]:
                writer.writerow(row)

# Function to create a list of all folder paths to process
def getFolderPaths(loadPath, savePath):
    folderPaths = []
    for templateFolder in os.listdir(loadPath):
        templateFolderPath = os.path.join(loadPath, templateFolder)
        if os.path.isdir(templateFolderPath):
            for relevantPointSchemeFolder in os.listdir(templateFolderPath):
                if relevantPointSchemeFolder in validFolderNames:
                    folderPaths.append((loadPath, savePath, templateFolder, relevantPointSchemeFolder))
    return folderPaths

# Main function for creating the composite images
def crossCorrelations(loadPath, savePath):
    folderPaths = getFolderPaths(loadPath, savePath)

    # Use a pool of workers to process folders in parallel
    with Pool() as pool:
        pool.map(processTemplateFolder, folderPaths)
