import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from imageProcessing.helpers.imports import *
from imageProcessing.helpers.constants import *
from imageProcessing.helpers.loadingAndSaving import loadStimuli


def pearsons(stimuli, weightMatrices, weightedMeanDifferences, summedWeightMatrices):
    
    # number of weights matrices we calculated
    numWeightMatrices = len(weightMatrices)

    # Initialize a cupy array to store the batch results
    # array size is (batchSize, number of weight matrices)
    # this is where our results will be saved to. Right now we are just creating
    # a data structure of the proper shape, and we will populate it with our results later
    batchResults = zeros((batchSize, numWeightMatrices), dtype = float32)

    # Compute the stimulus means for all stimuli and all weight matrices at once
    # our "stimuli" array has shape (batchSize, imageHeight, imageWidth). We use "stimuli[:, None, :, :]" to
    # adds a dimension to the stimuli array. We then multiply by weightMatrices to get a matrix of shape
    # (batchSize, number of weight matrices, imageHeight, imageWidth). Then we sum across axis 2 and axis 3,
    # which are the axes for imageWidth and imageHeight. This will be the sums of the pixel values in the image.
    # This sum gets stored in the number of weight matrices dimension, collapsing the array from shape (batchSize, number of weight matrices, imageHeight, imageWidth)
    # to an array of shape (batchSize, number of weights matrices) where each entry in the latter axis is the sum across the dimensions we collapsed.
    # Then we divide by summedWeightMatrices, which is of size (number of weight matrices). numpy/cupy broadcasting copies this array batchSize number of times
    # so we get something of the shape (batchSize, number of weight matrices) where each row is just a copy of summedWeightMatrices
    # Then we do this division and get "stimuliMeans" of size (batchSize, number of weight matrices) where each row is the results for one stimulus and 
    # each entry in the row is the weighted mean of that stimulus with respect to the weight matrix we are comparing it to
    stimuliMeans = sum(stimuli[:, None, :, :] * weightMatrices, axis = (2, 3)) / summedWeightMatrices

    # Compute the difference from weighted mean for all stimuli
    stimuliMeanDifferences = stimuli[:, None, :, :] - stimuliMeans[:, :, None, None]

    # Calculate Pearson correlation for all stimuli and all weight matrices at once
    numerator = sum(weightMatrices[None, :, :, :] * stimuliMeanDifferences * weightedMeanDifferences, axis=(2, 3))
    stimulusDenom = sqrt(sum(weightMatrices[None, :, :, :] * square(stimuliMeanDifferences), axis=(2, 3)))
    templateDenom = sqrt(sum(weightMatrices * square(weightedMeanDifferences), axis=(1, 2)))
    denominator = stimulusDenom * templateDenom[None, :]

    # Compute the Pearson correlation coefficients
    batchResults = numerator / denominator


    return batchResults

# process a batch of stimuli
def processAndStoreResults(arrayPath, weightMatrices, weightedMeanDifferences, summedWeightMatrices, results):

    #startTimeBatch = time.time()
    # load the stimuli, stimuli numbers, start stimuli number and end stimuli number for the current batch
    stimuli, start, end = loadStimuli(arrayPath)
    #print('Running stimuli %d to %d'%(start, end))

    # get a cupy array with the results for the current batch
    batchResults = pearsons(stimuli, weightMatrices, weightedMeanDifferences, summedWeightMatrices)
    
    # insert batchResults in results
    results[start: end] = batchResults
    #print('batch runtime for stimuli %d to %d: %f\n\n\n'%(start, end - 1, time.time() - startTimeBatch))

    return

