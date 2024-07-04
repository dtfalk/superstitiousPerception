import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from csvGeneration.helpers.imports import *

# Loads the index data from the indices CSV
def loadIndexData(indicesLoadPath):
    indicesDictionary = {}
    with open(indicesLoadPath, mode='r', newline='') as f:
        reader = csv.reader(f)
        for line in reader:
            key, index = line
            indicesDictionary[key] = int(index)  # Convert index to int for direct usage
    return indicesDictionary

# Worker function to create a single CSV file
def create_single_csv(args):
    key, index, pearsonData, savePath = args
    templateName, relevantPointScheme, weightingScheme = key.split('_')
    finalSavePath = os.path.join(savePath, templateName, relevantPointScheme, weightingScheme)
    os.makedirs(finalSavePath, exist_ok=True)

    schemeData = pearsonData[:, index]

    df = pd.DataFrame({
        'Stimulus Number': np.arange(len(schemeData)),
        'Pearson r value': schemeData
    })

    dfSorted = df.sort_values('Pearson r value', ascending=False)
    dfSorted.to_csv(os.path.join(finalSavePath, 'pearsonScores.csv'), index=False)

# Creates a CSV file in the proper folder for each combination
def createCSVs(pearsonData, indicesDictionary, savePath):
    # Create a list of arguments for each worker
    args_list = [(key, index, pearsonData, savePath) for key, index in indicesDictionary.items()]

    # Define chunk size
    chunk_size = 100  # Adjust based on your system's capacity

    # Use a pool of workers to create CSVs in parallel
    with Pool() as pool:
        for i in range(0, len(args_list), chunk_size):
            pool.map(create_single_csv, args_list[i:i + chunk_size])
