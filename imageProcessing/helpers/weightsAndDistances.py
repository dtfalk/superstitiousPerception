import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from imageProcessing.helpers.imports import *
from imageProcessing.helpers.constants import *


# ================================================================================================
# =======================   GETTING THE DISTANCE MATRIX   ========================================
# ================================================================================================

# extracts the relevant points that we decide to have distance = 0 based on relevant point scheme
def getRelevantPoints(template, relevantPointScheme):
    if relevantPointScheme == 'anyAll':
        relevantPoints = (template == 0)
    else:
        # Check if the point is zero and if it is a border point
        is_zero = (template == 0)
        padded_template = pad(template, pad_width = 1, mode = 'constant', constant_values = 1)
        
        # Check for neighboring 1's
        neighbors = (
            (padded_template[:-2, 1:-1] == 1) |  # top
            (padded_template[2:, 1:-1] == 1) |   # bottom
            (padded_template[1:-1, :-2] == 1) |  # left
            (padded_template[1:-1, 2:] == 1) |   # right
            (padded_template[:-2, :-2] == 1) |   # top-left
            (padded_template[2:, 2:] == 1) |     # bottom-right
            (padded_template[:-2, 2:] == 1) |    # top-right
            (padded_template[2:, :-2] == 1)      # bottom-left
        )
        
        relevantPoints = is_zero & neighbors

    # Extract the indices of the relevant points
    relevant_indices = column_stack(nonzero(relevantPoints))
    
    return relevant_indices


# returns the minimum distance of a point from any of the relevant point in the stimuli
def getDistance(relevantPoints, rowIndices, colIndices):
    

    # Calculate the difference in rows and columns between each element in array and each relevant point
    # Using broadcasting, this will generate arrays of differences in dimensions [array_shape x num_relevant_points]
    rowDiffs = rowIndices[:, :, None] - relevantPoints[:, 0]
    colDiffs = colIndices[:, :, None] - relevantPoints[:, 1]

    # Calculate squared distances using the differences
    squaredDistances = (rowDiffs ** 2) + (colDiffs ** 2)

    # Find the minimum squared distance for each element in array
    minSquaredDistances = squaredDistances.min(axis = 2)

    # Take the square root to get the actual distances
    distances = sqrt(minSquaredDistances)

    return distances


# gets a distance matrix for each (template, distance metric, relevant point scheme) trio
def getDistanceMatrix(template, relevantPointScheme):

    # gets the indices as a matrix
    rowIndices, colIndices = indices(template.shape)

    # gets the relevant points as a 2d numpy array according to the relevant point scheme
    relevantPoints = getRelevantPoints(template, relevantPointScheme)

    # return an array of size (imageWidth, imageHeight where each entry is the distance from a relevant point)
    distanceMatrix = getDistance(relevantPoints, rowIndices, colIndices)

    return distanceMatrix

# ================================================================================================
# ================================================================================================
# ================================================================================================

# ================================================================================================
# =======================   GETTING THE WEIGHTS MATRIX   =========================================
# ================================================================================================

# get the weighted mean of the image data 
def getWeightedMean(array, weightMatrix):
    weightedSum = sum(weightMatrix * array)
    totalWeight = sum(weightMatrix)
    
    if totalWeight > 0:
        return weightedSum / totalWeight
    
    
    return 0


# gets a weight matrix for each (template, distance metric, relevant point scheme) trio
def getWeightMatrix(template, weightingScheme, relevantPointScheme, imageDimensions):
    
    # calculate a distance matrix for each tuple
    distanceMatrix = getDistanceMatrix(template, relevantPointScheme)

    # get the non-zero distances in the template (distance == 0  ===>  weight == 1)
    nonZeroDistances = distanceMatrix != 0

    # prepare a matrix to fill with the weights for each point
    weightsMatrix = ones_like(template, dtype = float32)

    if weightingScheme == 'linear':
        # linear weighting (1 / distance)
        weightsMatrix[nonZeroDistances] = 1 / distanceMatrix[nonZeroDistances]
    elif weightingScheme == 'quadratic':
        # quadratic weighting (1 / distance ** 2) 
        weightsMatrix[nonZeroDistances] =  1 / square(distanceMatrix[nonZeroDistances])
    elif weightingScheme == 'logarithmic':
        # logarithmic weighting (log(1 + (1 / log(distance))))
        weightsMatrix[nonZeroDistances] = log(1 + (1 / distanceMatrix[nonZeroDistances]))
    elif weightingScheme == 'gaussian':
        # gaussian weighting (e ** (- (distance ** 2) / (2 * sigma ** 2)))
        weightsMatrix[nonZeroDistances] = exp(-1 * square(distanceMatrix[nonZeroDistances]) / (2 * square(sigma)))
    elif 'central' == weightingScheme:
        # distance from center of image weighting scheme
        rowIndices, colIndices = indices(template.shape)
        distanceToCenter = sqrt(square(rowIndices - (imageDimensions[0] // 2)) + square(colIndices - (imageDimensions[1] // 2)))
        distanceToCenter[distanceToCenter == 0] = 1
        weightsMatrix[distanceToCenter != 0] = 1 / distanceToCenter[distanceToCenter != 0]
    else:
        # unweighted weighting scheme (everything has weight == 1)
        weightsMatrix = ones(template.shape, dtype = float32)
    
    
    # return the weights matrix
    return weightsMatrix


# generate all of the weights matrices as a dictionary
def getWeightMatrices(templates, templateNames, imageDimensions):

    # get the number of different weight matrices we will produce
    numWeightMatrices = len(templates) * len(weightingSchemes) * len(relevantPointSchemes)

    # create cupy objects to store the weight matrices and the template means (reduces recalculating)
    weightsMatrices = zeros(shape = (numWeightMatrices, imageDimensions[0], imageDimensions[1]), dtype = float32)
    weightedMeanDifferences = zeros(shape = (numWeightMatrices, imageDimensions[0], imageDimensions[1]), dtype = float32)
    summedWeightMatrices = zeros(shape = (numWeightMatrices), dtype = float32)

    # need to write everything to a csv in the end so we know which index 
    # translates to which template/weighting scheme/relevant point scheme combo
    indicesDictionary = {}

    # variable to store the index
    z = 0

    # iterate over each template
    for i, template in enumerate(templates):

        # store template name to reduce computation
        templateName = templateNames[i]

        # iterate over each relevant point scheme and each weighting scheme
        for relevantPointScheme in relevantPointSchemes:
            for weightingScheme in weightingSchemes:

                # get the weight matrix for the template, relevant point scheme, and weighting scheme
                # and add to cupy array
                weightMatrix = getWeightMatrix(template, weightingScheme, relevantPointScheme, imageDimensions)
                weightsMatrices[z] = weightMatrix

                # get the templates difference from its weighted mean and add to cupy array
                weightedMean = getWeightedMean(template, weightMatrix)
                weightedMeanDifferences[z] = template - weightedMean

                # get the sum each weight matrix and store it
                summedWeightMatrices[z] = sum(weightMatrix)

                # add the name of the 3-tuple and its index to the indices dictionary so we can
                # recover which index translates to which 3-tuple later
                indicesDictionary['%s_%s_%s'%(templateName, relevantPointScheme, weightingScheme)] = z

                # increment out index counter by one
                z += 1

    return weightsMatrices, weightedMeanDifferences, summedWeightMatrices, indicesDictionary

# ================================================================================================
# ================================================================================================
# ================================================================================================