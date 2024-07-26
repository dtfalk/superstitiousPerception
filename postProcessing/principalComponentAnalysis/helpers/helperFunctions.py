import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.join(os.path.abspath(__file__)))))))
from postProcessing.principalComponentAnalysis.helpers.imports import *
from postProcessing.principalComponentAnalysis.helpers.constants import *

# note that the columns will be in the following order ('linear', 'quadratic', 'logarithmic', 'gaussian', 'central', 'unweighted')
def collectData(loadPath, templateType, templateName, distanceScheme):

    # loads the indices data into a list translating keys into numpy indices
    indicesList = []
    
    with open(os.path.join(loadPath, '..', 'indices.csv'), mode = 'r', newline = '') as f:
        reader = csv.reader(f)
        lines = list(reader)

        for line in lines:
            for weightingScheme in weightingSchemes:
                schemeName = f'{templateName}_{distanceScheme}_{weightingScheme}'
                if schemeName == line[0]:
                    indicesList.append(int(line[1]))
    indicesList.sort()
    
    # load the numpy data 
    data = np.load(os.path.join(loadPath, '..', f'{templateType}.npy'))[:, indicesList]
    return data
    

def performPCA(data, n_components=2):
    # Standardize the data (optional but recommended)
    scaler = StandardScaler()
    data_std = scaler.fit_transform(data)
    
    # Perform PCA
    pca = PCA(n_components=n_components)
    principalComponents = pca.fit_transform(data_std)
    
    # Get the explained variance ratio
    explainedVariance = pca.explained_variance_ratio_
    
    return principalComponents, explainedVariance

# write the data 
def writeData(principalComponents, explainedVariance, savePath):
    
    # save the principal component coordinates as a numpy file
    np.save(os.path.join(savePath, 'principalVectors.npy'), np.array(principalComponents))
    explainedVarianceHeader = ['Principal Component', 'Variance Explained']

    with open(os.path.join(savePath, 'varianceExplained.csv'), mode = 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(explainedVarianceHeader)

        for componentNumber, varianceExplained in enumerate(explainedVariance):
            writer.writerow([componentNumber, varianceExplained])

    return
