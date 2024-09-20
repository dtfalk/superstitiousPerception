# **Author**

**David Tobias Falk**



# **Contact Info**

**Email**: dtfalk@uchicago.edu, davidtobiasfalk@gmail.com

**Cell**: 1-413-884-2553 (please text first or I will assume that you are spam)

# **Document Purpose**
This document is meant to explain how we perform the pearson score computations with the code in the **imageProcessing** folder. This serves as a helpful example for using numpy and other "advanced" python data processing operations. So let's dive in!

# **Overview of what the code does**
This code takes the numpy arrays in the **arraysAndImages** folder and calculates pearson scores for each combination of image, template, relevant point scheme and weighting scheme. It is important to first descrive and motivate the use of a "pearson score". A pearson score is meant to compare two vectors to each other. A high pearson score (value ~ 1) means a high degree of correlation between the two vectors. A low pearson score (value ~ -1) means there is an inverse relationship between the two vectors. A pearson score near 0 means that that their is little to no correlation between the two vectors. So when we compare a template with a stimulus, we are using their pearson score to quantify how similar the two vectors are. When you do this for all of the stimuli, you get to see which images are most similar, most dissimilar, or have no correlation to the template. You may notice that the pearson score is meant for two one-dimensional vectors, but images are two-dimensional matrices. To get around this we simply flatten the arrays from two-dimensions to one dimension. For example, a 50x50 image can be flattened into a vector with 2500 (50 * 50) entries. There are two other aspects I mentioned but have not explained yet: the **relevant point scheme** and the **weighting scheme**. Remember that this experiment is about how people pick up on signal in noisy environments. We hypothesize that when a subject is looking at one of our noisy stimuli, they are giving higher priority to pixels that are closer to where the template image would be and lower priority to pixels far away from the template image. In simple terms, people focus more on the relevant parts of the image and focus less on the irrelevant parts of the image. As a result we want to order the pixels by their distance from the relevant points, give the closer points a higher weight, and give the further points a lower weight. We came up with 6 potential "fall-off functions" for how the weight of a pixel falls off as its distance grows larger. Then we also have the relevant point scheme. There are two relevant point schemes. The difference between the schemes is which points we consider to have maximum weight. In one scheme we consider all points within the template to have maximum weight. In the other scheme we only consider the border points to have maximum weight. Every other pixel's distance is calculated as its distance from the nearest point of maximum weight. Distance is calculated as the euclidian distance ($\sqrt((y_2 - y_1)^2 + (x_2 - x_1)^2)$). So for each combination of stimulus, template, weighting scheme and relevant point scheme we calculate a pearson r score. There are currently 1 million stimuli, 29 templates, 6 weighting schemes, and 2 relevant point schemes. This comes out to 348 million pearson scores. You can see why it might be important to do these calculations efficiently. 

# **Following the control flow of the code**
Let's start by examining the **main.py** file found in the **imageProcessing** folder. 

```
import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from imageProcessing.templateSpecificFunctions.fullscreenCrosses import main as fullscreen
from imageProcessing.templateSpecificFunctions.halfscreenCrosses import main as halfscreen
from imageProcessing.templateSpecificFunctions.hiAnalysis import main as hi
from imageProcessing.templateSpecificFunctions.S import main as S
from imageProcessing.helpers.imports import *

# run the analysis functions
def main():
    print('    Image processing starting now...\n')
    startTime = time.time()
    fullscreen()
    halfscreen()
    hi()
    S()
    print('\n    Runtime for processing all images: %.4f seconds\n\n\n'%(time.time() - startTime))

if __name__ == '__main__':
    main()
```

This is the launching pad for the rest of the code. As you can see it is importing "template specific functions" functions and calling each of them. That is because we have a couple different paradigms we are exploring, and each one of these main functions runs the code for a different paradigm. All of the paradigms are nearly identical with the only difference being the templates that are used. So this bit of code just calls each paradigm's code. Let's follow the hiAnalysis ("hi()" in this function) to see how data flows through this code. 

Looking in the **imageProcessing/templateSpecificFunctions/hiAnalysis** folder we find another **main.py** function. 

```
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from imageProcessing.helpers.imports import *
from imageProcessing.helpers.constants import *
from imageProcessing.helpers.weightsAndDistances import *
from imageProcessing.helpers.loadingAndSaving import *
from imageProcessing.helpers.batching import *

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
```

The **getPaths()** function simply returns loading and saving locations for where we will load the stimuli/templates and where we will save the pearson scores to. The **main()** function is where all the action is. In the next section we will be focusing on/following the following line of code...

```
    # get the weight matrices and the weighted means of the templates (and the 3-tuple to index crosswalk)
    weightMatrices, weightedMeanDifferences, summedWeightMatrices, indicesDictionary = getWeightMatrices(templates, templateNames, imageDimensions)
```

# **Precalculating and Retrieving Weights Matrices**
Since we are doing so many calculations we don't want to unneccesarily recompute values that we have already spent time computing. We want to store them and then reuse them each time we need them. This is massively important. The first time I wrote this code it took 2 days to run. Now this section takes 3 minutes to run. This is because, among other things, I was very conscious about not recalculating values. The block of code above calls the **getWeightMatrices** function in the **imageProcessing/helpers/weightsAndDistances.py** file.
Let's look at the **getWeightMatrices** function.

```

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
```

This function first calculates the number of triplets of templates, relevant point schemes, and weighting schemes and prefills an array with all zeroes. It then iterates over each triplet and calculates 3 computationally relevant values:

1. **The Weight Matrix** (using **getWeightMatrix()**)
2. **The Weighted Mean** (using **getWeightedMean()**)
3. **A Summed Weight Matrix**

Let's dive into each of these and see how they do what they do.

## The Weight Matrix

The weight matrix is calculated using the **getWeightMatrix()** function.

```
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
```

The first thing that this function does is call upon **getDistanceMatrix()**...

```
# gets a distance matrix for each (template, distance metric, relevant point scheme) trio
def getDistanceMatrix(template, relevantPointScheme):

    # gets the indices as a matrix
    rowIndices, colIndices = indices(template.shape)

    # gets the relevant points as a 2d numpy array according to the relevant point scheme
    relevantPoints = getRelevantPoints(template, relevantPointScheme)

    # return an array of size (imageWidth, imageHeight where each entry is the distance from a relevant point)
    distanceMatrix = getDistance(relevantPoints, rowIndices, colIndices)

    return distanceMatrix
```
This function first calls **getRelevantPoints**...

```
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

```
The purpose of **getRelevantPoints()** is to find all of the points that have maximum weight/zero distance. It will return a list of indices (e.g. [(1,1), (2, 7), ...]) that represent the location of the "relevant points". As you can see, there is an if-else statement to handle our two different relevant point schemes. The if portion handles the case where we consider any point inside the template to be of maximum weight/minimal distance. Since the template is black and everything else is white, this amounts to returning the location of all of the black pixels in the image. The else portion of the if-else statement checks for points that are black and border at least one white pixel. These are considered border points which is what we are examining for our other relevant point scheme. Once this function is done we will have a list of indices, with each index being the location of one relevant point. 

This function's return value gets sent back to **getDistanceMatrix()** which then calls on the **getDistance()** function.

```
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

    # TODO: Modularize this assert
    assert(distances.shape == (51, 51))

    return distances
```

This function calculates each pixel's distance to the nearest relevant point. We use the typical euclidian distance function ($\sqrt((y_2 - y_1)^2 + (x_2 - x_1)^2)$). This code uses an important Numpy feature called *braodcasting*. It allows you to perform array operations on matrices of different sizes and get a resulting array of larger dimensions. That probably is not a very illuminating description of broadcasting, so let's look at it in the context of this function to see what I am talking about. Remember that our goal is to find the shortest distance between a pixel and the nearest relevant point. We start by defining **rowDiffs** and **columnDiffs**. As a quick note, **rowIndices** is just an imageHeight x imageWidth sized array where each entry is the number of the row. 

### Row Indices
|   |   |   |   |   |
|---|---|---|---|---|
| 0 | 0 | ... | 0 | 0 |
| 1 | 1 | ... | 1 | 1 |
| ... | ... | ... | ... | ... |
| imageHeight - 2 | imageHeight - 2 | ... | imageHeight - 2 | imageHeight - 2 |
| imageHeight - 1 | imageHeight - 1 | ... | imageHeight - 1 | imageHeight - 1 |

### Col(umn) Indices
|   |   |   |   |   |
|---|---|---|---|---|
| 0 | 1 | ... | imageWidth - 2 | imageWidth - 1 |
| 0 | 1 | ... | imageWidth - 2 | imageWidth - 1 |
| ... | ... | ... | ... | ... |
| 0 | 1 | ... | imageWidth - 2 | imageWidth - 1 |
| 0 | 1 | ... | imageWidth - 2 | imageWidth - 1 |

So the line in **getDistance()** that reads `rowDiffs = rowIndices[:, :, None] - relevantPoints[:, 0]` takes the two dimensional rowIndices array, adds ("broadcasts") a third dimension to it (which is currently set to **None** meaning it is currently empty, but prepared for use). Then it takes **relevantPoints** which is a one dimensional list of points (e.g. (5, 6)). The line `relevantPoints[:, 0]` tells it to take the first entry from each point of the list (the row number of the relevant point) and subtract it from the row number of index in **rowIndices**. It does this for each relevant point. The result is that we get a three dimensional array, **rowDiffs** where each entry is a pixel's distance from a relevant point. The shape of the **rowDiffs** is (imageWidth, imageHeight, number of relevant points). So every entry of the form (5, 3, n) will be the vertical distance of the pixel located at (5, 3) from one of the relevant points. For example, the entry (5, 3, 8) will contain the distance of the pixel at (5, 3) from the 9th relevant point (remember, in computer science we index lists from 0 so index 8 is the 9th entry). 

We do the same for colIndices. So we are left with **rowDiffs** and **colDiffs**. **rowDiffs** contains each pixel's vertical distance from each relevant point and **colDiffs** contains each pixel's horizontal distance from each relevant point. 

Then the lines `squaredDistances = (rowDiffs ** 2) + (colDiffs ** 2)` returns an array with the same shape as **rowDiffs** and **colDiffs** where each entry is the sum of the squares of the corresponding entry in **rowDiffs** and **colDiffs**. For example, entry (3, 4, 7) of **squaredDistances** equals $rowDiffs[3, 4, 7]^2 + colDiffs[3,4,7]^2$. Since taking the square root of numbers greater than one will preserve order (i.e. if m,n > 1, then $m > n$ implies $\sqrt(m) > \sqrt(n)$). So we don't need to calculate square roots to find out which distance is smallest for each pixel. Finally, the ".min(axis = 2)" in `minSquaredDistances = squaredDistances.min(axis = 2)` will take each point's minimum distance along the relevant points axis, giving us an imageHeight x imageWidth size array with each entry being that pixel's minimum distance squared from a relevant point. 

The last step is to take the square root of each distance using `distances = sqrt(minSquaredDistances)` and return the distances object. Thus we are left with an imageHeight x imageWidth array with each pixel's minimum distance from a relevant point. This gets returned back to **getDistanceMatrix()** which returns the same value back to **getWeightMatrix()**.

Let's look at **getWeightMatrix()** again to see where we are...

```
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
```

We have now successfully completed the first line of code in this function, namely, `distanceMatrix = getDistanceMatrix(template, relevantPointScheme)`. We have a imageHeight x imageWidth sized array with each pixel's distance from its nearest relevant point. Remember, relevant points will have the highest possible weighting for the ultimate comparison we do between the stimulus and the template. Furthermore, points with the highest possible weight are considered to have a distance equal to zero.

The next line of code is `nonZeroDistances = distanceMatrix != 0` which just gives us a list of points that are not equal to 0 (relevant points/maximum weight points). Points with distance equal to 0 will be given a weight of 1, while points with a distance greater than 0 will have weight less than 1, with the weights getting smaller as distance increases.

Then we use our if/elif/else statement to retrieve the weight that each pixel (with nonzero distance) gets based on the weighting scheme.

NORMALIZE???

This weight matrix gets returned back to the **getWeightMatrices()** function. Let's revisit that function to see where we are.

```
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
```

We have now successfully completed the `weightMatrix = getWeightMatrix(template, weightingScheme, relevantPointScheme, imageDimensions)' line of code and appended this weight matrix to the the weightsMatrices list at index z. 

We then calculate a weighted mean using the **getWeightedMean()** function. Let's examine that function.

```
def getWeightedMean(array, weightMatrix):
    weightedSum = sum(weightMatrix * array)
    totalWeight = sum(weightMatrix)
    
    if totalWeight > 0:
        return weightedSum / totalWeight

    return 0
```

This function takes the template and the weight matrix and calculates a weighted mean according to $\frac{\sum_{i = 0}^{imageHeight - 1}{\sum_{j = 0}^{imageWidth - 1}{T_{i,j} * WM_{i,j}}}}{\sum_{i = 0}^{imageHeight - 1}{\sum_{j = 0}^{imageWidth - 1}{WM_{i,j}}}}$ where $T_{i,j}$ is the i,jth entry in the template matrix and $WM_{i,j}$ is the i,jth entry in the weight matrix.

This value is returned back to **getWeightMatrices()** and subtracted from the template to get an array that is the template with the weighted mean subtracted off from it. This centers the template around its mean and is important later for when we are calculating standard deviations and covariances for the weighted pearson scores we are using. We store this result in index z of the **weightedMeanDifferences** list.

Additionally, we take a sum of all elements in the weight matrix, calculated as $\sum_{i = 0}^{imageHeight - 1}{\sum_{j = 0}^{imageWidth - 1}{WM_{i,j}}}$ and store that in **summedWeightMatrices** for later use.

Finally, we need to keep track of which index corresponds to which template/relevant point scheme/weighting scheme combination. We do this in this line: `indicesDictionary['%s_%s_%s'%(templateName, relevantPointScheme, weightingScheme)] = z` allows us to translate between triplet names and the index at which we can find that triplet's precalculated data. 

This code runs for all triplets of template, relevant point scheme, and weight scheme. Once it iterates through all possible triplets, we are left with four computationally relevant, precalculated values. For the following description, let's assume that we have **T** total templates, **R** total relevant point schemes and **W** total weighting schemes.

## **Precalculated Values**
1) **Weight Matrices:** This is a large matrix where each layer represents one triplet's weight matrix. It will have a shape of **T** * **R** * **W** x ImageHeight x ImageWidth. For the figure below let's assume that ImageWidth = m and imageHeight = n.
```
Weight Matrix #1:
[

  [w_(0,0,0), w_(0,0,1), ..........., w_(0,0,m-1), w_(0,0,m)],
  [w_(0,1,0), w_(0,1,1), ..........., w_(0,1,m-1), w_(0,1,m)],
  [..., ..., ..., ..., ..., ..........., ..., ..., ..., ....],
  [w_(0,n-1,0), w_(0,n-1,1), ..., w_(0,n-1,m-1), w_(0,n-1,m)],
  [w_(0,n,0), w_(0,n,1), ..........., w_(0,n,m-1), w_(0,n,m)],
  
]

Weight Matrix #2:
[

  [w_(1,0,0), w_(1,0,1), ..........., w_(1,0,m-1), w_(1,0,m)],
  [w_(1,1,0), w_(1,1,1), ..........., w_(1,1,m-1), w_(1,1,m)],
  [..., ..., ..., ..., ..., ..........., ..., ..., ..., ....],
  [w_(1,n-1,0), w_(1,n-1,1), ..., w_(1,n-1,m-1), w_(1,n-1,m)],
  [w_(1,n,0), w_(1,n,1), ..........., w_(1,n,m-1), w_(1,n,m)],

]

.
.
.
.

Weight Matrix #(TRW - 1):
[

  [w_(TRW - 1,0,0), w_(TRW - 1,0,1), ..........., w_(TRW - 1,0,m-1), w_(TRW - 1,0,m)],
  [w_(TRW - 1,1,0), w_(TRW - 1,1,1), ..........., w_(TRW - 1,1,m-1), w_(TRW - 1,1,m)],
  [..., ..., ..., ..., ..., ..................................., ..., ..., ..., ....],
  [w_(TRW - 1,n-1,0), w_(TRW - 1,n-1,1), ..., w_(TRW - 1,n-1,m-1), w_(TRW - 1,n-1,m)],
  [w_(TRW - 1,n,0), w_(TRW - 1,n,1), ..........., w_(TRW - 1,n,m-1), w_(TRW - 1,n,m)],
  
]

Weight Matrix #TRW:
[

  [w_(TRW,0,0), w_(TRW,0,1), ..........., w_(TRW,0,m-1), w_(TRW,0,m)],
  [w_(TRW,1,0), w_(TRW,1,1), ..........., w_(TRW,1,m-1), w_(TRW,1,m)],
  [..., ..., ..., ..., ..., ..................., ..., ..., ..., ....],
  [w_(TRW,n-1,0), w_(TRW,n-1,1), ..., w_(TRW,n-1,m-1), w_(TRW,n-1,m)],
  [w_(TRW,n,0), w_(TRW,n,1), ..........., w_(TRW,n,m-1), w_(TRW,n,m)],
  
]
```

2) **A Template Matrix Centered Around Mean Array:** This is a one dimensional array of shape T * R * W.

```
[
    Centered Template #1,
    Centered Template #2,
    .
    .
    .
    Centered Template #(TRW - 1),
    Centered Template #TRW
]
```

3) **A Sums of Weight Matrices Array:** This is a one dimensional array of shape T * R * W.

```
[
    Sum of Weight Matrix #1,
    Sum of Weight Matrix #2,
    .
    .
    .
    Sum of Weight Matrix #(TRW - 1),
    Sum of Weight Matrix #TRW 
]
```

4) **A Mapping Between Indices and Triplet of Template/Relevant Point Scheme/Weighting Scheme:** 

### Indices Mapping
| Scheme Name  |  Index |
|---|---|
| template_relevantPointScheme_weightingScheme_0 | 0 |
| template_relevantPointScheme_weightingScheme_1 | 1 |
| ... | ... |
| ... | ... |
| ... | ... |
| template_relevantPointScheme_weightingScheme_(TRW-1) | TRW -1 |
| template_relevantPointScheme_weightingScheme_TRW | TRW |

These four objects are returned from **getWeightMatrices()** back to the template specific function in **templateSpecificFunctions**. This wraps up our section on precalculating values. Now we move to the pearson calculations and working with the actual stimuli

## Pearson Calculations and Working With the Stimuli
Let's review the code in the template specific function file.

```
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
```

We have now covered up through the line that reads `weightMatrices, weightedMeanDifferences, summedWeightMatrices, indicesDictionary = getWeightMatrices(templates, templateNames, imageDimensions)`.
The next line `results = zeros(shape = (numImages, len(templates) * len(weightingSchemes) * len(relevantPointSchemes)), dtype = float32)` declares numpy array filled with zeroes. This array will ultimately store the results of our pearson calculations, but we fill it with zeroes to begin with because it is inefficient to update the size of a numpy array as the code runs. Thankfully, we already know the size of our results so we pre-declare the array and just fill it with placeholder zeroes. 

The next bit of code requires a little bit of background. Let's look at the code:

```
for arrayPath in os.listdir(stimuliPath):
        processAndStoreResults(os.path.join(stimuliPath, arrayPath), weightMatrices, weightedMeanDifferences, summedWeightMatrices, results)
```

The **stimuliPath** variable contains a location to where the stimuli arrays are stored. Although we are showing the subjects images, images are just imageHeight x imageWidth arrays. It is much faster to perform operations on numpy arrays than it is to load in and operate on a png file or other image formats. So we store both the images and the arrays in a folder called **arraysAndImages** that is created when you run the code located in the **imageGeneration** folder. Within the **arraysAndImages/stimuli** folder there is an **arrays** subfolder and an **images** subfolder. The numpy arrays are stored in the **arrays** subfolder. If you open up the folder you will see that there are only 1000 numpy files even though we currently have 1 million images. That is because each file is a three dimensional array with a shape of 1000 x imageHeight x imageWidth. You can imagine it as 1000 images stacked on top of each other to form a three dimensional array. 

What the code above does is take the location of the **arrraysAndImages/stimuli/arrays** folder and iterate over all of the files in it. There are 1000 files currently, so this loop iterates 1000 times. It calls the **processAndStoreResults()** function on each iteration with each batch of 1000 images. Notice that it performs all T * R * W operations on the 1000 images. So we do all operations for the 1000 images and then move on to the next 1000. 

Let's look at what is going on in the **processAndStoreResults()** function. This function is located in the **batching.py** file located in the **helpers** folder.

```
def processAndStoreResults(arrayPath, weightMatrices, weightedMeanDifferences, summedWeightMatrices, results):

    # load the stimuli, stimuli numbers, start stimuli number and end stimuli number for the current batch
    stimuli, start, end = loadStimuli(arrayPath)

    # get a cupy array with the results for the current batch
    batchResults = pearsons(stimuli, weightMatrices, weightedMeanDifferences, summedWeightMatrices)
    
    # insert batchResults in results
    results[start: end] = batchResults
    #print('batch runtime for stimuli %d to %d: %f\n\n\n'%(start, end - 1, time.time() - startTimeBatch))

    return
```

The first line of code `stimuli, start, end = loadStimuli(arrayPath)` loads the batch of stimuli, and the start and end indices so we know where to store the results in the results matrix once we compute the values.

The next line `batchResults = pearsons(stimuli, weightMatrices, weightedMeanDifferences, summedWeightMatrices)` calls upong our **pearsons()** function. Let's examine this function and see what it is up to. The function is short, but there are some complex numpy operations in there that it will be good to break down. 

```
def pearsons(stimuli, weightMatrices, weightedMeanDifferences, summedWeightMatrices):
    
    # number of weights matrices we calculated
    numWeightMatrices = len(weightMatrices)

    batchResults = zeros((batchSize, numWeightMatrices), dtype = float32)

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
```

The first two lines of code simply recover the value of T * R * W and intitialize an array with the proper dimensions to store the results for this batch. This moves us to the first line here that will require explanation. But before that, let's look at the equation for the pearson score and our weighted modification.

The original pearson equation for a template T and a stimulus S would be given by 
$$ 
PearsonScore(S, T) = \frac{covariance(S,T)}{standardDeviation(S) * standardDeviation(T)}
$$
This can be rewritten as 
$$
\frac{\sum_{i = 0}^{imageHeight - 1}{\sum_{j = 0}^{imageWidth - 1}{(S_{i,j} - \bar{S}) * (T_{i,j} - \bar{T})}}}{\sqrt{\sum_{i = 0}^{imageHeight - 1}{\sum_{j = 0}^{imageWidth - 1}{(S_{i,j} - \bar{S}) ^ 2}}} * \sqrt{\sum_{i = 0}^{imageHeight - 1}{\sum_{j = 0}^{imageWidth - 1}{(S_{i,j} - \bar{S}) ^ 2}}}}
$$
However, we would like to use a weighted pearson correlation metric. A common weighted version of this is given by the following few equations...

1) **Weighted Mean of Stimulus and Template**
    Let's decide that the notation we use for a weighted mean of a variable X is $\overline{WX}$.
    Then we have weighted means for a stimulus S and a template T given by....
    $$
    \overline{WS} = \frac{\sum_{i = 0}^{imageHeight - 1}{\sum_{j = 0}^{imageWidth - 1}}{weightMatrix_{i,j} * S_{i,j}}}{\sum_{i = 0}^{imageHeight - 1}{\sum_{j = 0}^{imageWidth - 1}{weightMatrix_{i,j}}}}
    $$
    and
    $$
    \overline{WT} = \frac{\sum_{i = 0}^{imageHeight - 1}{\sum_{j = 0}^{imageWidth - 1}}{weightMatrix_{i,j} * T_{i,j}}}{\sum_{i = 0}^{imageHeight - 1}{\sum_{j = 0}^{imageWidth - 1}{weightMatrix_{i,j}}}}
    $$


2) **Weighted Covariance of the Stimulus with the Template** 
    $$
    WeightedCovariance(S, T) = \frac{\sum_{i = 0}^{imageHeight - 1}{\sum_{j = 0}^{imageWidth - 1}{WeightMatrix_{i,j} * (S_{i,j} - \overline{WS}) * (T_{i,j} - \overline{WT})}}}{\sum_{i = 0}^{imageHeight - 1}{\sum_{j = 0}^{imageWidth - 1}{WeightMatrix_{i,j}}}}
    $$

3) **The Weighted Covariance of the Stimulus with itself and the Weighted Covariance of the template with itself**

$$
    WeightedCovariance(S, S) = \frac{\sum_{i = 0}^{imageHeight - 1}{\sum_{j = 0}^{imageWidth - 1}{WeightMatrix_{i,j} * (S_{i,j} - \overline{WS}) * (S_{i,j} - \overline{WS})}}}{\sum_{i = 0}^{imageHeight - 1}{\sum_{j = 0}^{imageWidth - 1}{WeightMatrix_{i,j}}}}
$$

and 

$$
    WeightedCovariance(T, T) = \frac{\sum_{i = 0}^{imageHeight - 1}{\sum_{j = 0}^{imageWidth - 1}{WeightMatrix_{i,j} * (T_{i,j} - \overline{WT}) * (T_{i,j} - \overline{WT})}}}{\sum_{i = 0}^{imageHeight - 1}{\sum_{j = 0}^{imageWidth - 1}{WeightMatrix_{i,j}}}}
$$

Overall, these formulas combine to give the weighted pearson correlation by the equation

$$
WeightedPearsonScore(S,T) = \frac{WeightedCovariance(S,T)}{\sqrt{weightedCovariance(S,S) * WeightedCovariance(T,T)}}
$$

Now let's move on to the crucial block of code in our **pearsons()** function above...

```
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
```

This is quite complicated so let's take it line by line. The first line is as follows...

```
    stimuliMeans = sum(stimuli[:, None, :, :] * weightMatrices, axis = (2, 3)) / summedWeightMatrices
```

This line is meant to calculate the weighted means of the stimuli which would be given by the equation

$$
\overline{WS} = \frac{\sum_{i = 0}^{imageHeight - 1}{\sum_{j = 0}^{imageWidth - 1}}{weightMatrix_{i,j} * S_{i,j}}}{\sum_{i = 0}^{imageHeight - 1}{\sum_{j = 0}^{imageWidth - 1}{weightMatrix_{i,j}}}}
$$

This code is once again making use of numpy's broadcasting feature. It starts by adding a dimension to the **stimuli** array. The **stimuli** array had a shape of (1000, imageHeight, imageWidth). After adding a dimension (using `stimuli[:, None, :, :]`), it has a shape of (1000, 1, imageHeight, imageWidth). Then we multiply this new array by **weightMatrices** which has shape (T * R * W, imageHeight, imageWidth). This will cause the resulting matrix to have a shape of (1000, T * R * W, imageHeight, imageWidth). Before we get to the contents of the resulting matrix, it is important to understand why we seem to randomly add a dimension in the middle of the stimuli matrix. We did this because this array reshaping happens before the calculations begin. So when they are being multiplied together, the now four dimensional stimuli matrix, which I just said has a shape of (1000, 1, imageHeight, imageWidth), actually gets extended to have a shape (1000, T * R * W, imageHeight, imageWidth) and gets multiplied by the **weightMatrices** array with shape (T * R * W, imageHeight, imageWidth). We do this because we need each stimulus to get multiplied by all of the weight matrices which is why the newly broadcast **stimuli** array is the same shape as **weightMatrices** with an extra dimension out front. 

Now let's talk about the contents of this matrix. Let's call this resulting matrix **result**. Let me explain what the result[a, b, c, d] will be...

$$
result[a, b, i, j] = stimulus_a(i, j) * weightMatrix_b(i, j)
$$

where $stimulus_a(i, j)$ is the i,j-th entry of the a'th stimulus and $weightMatrix_b(i, j)$ is the i,jth entry of the b'th weight matrix. This 4 dimensional matrix contains the result of element-wise multiplying every entry of every stimulus by every weight matrix. 

Then, the `sum(..)` and `axis = (2, 3)` bits that surround this matrix sum up each matrix across its second and third axes. The result of summing over the second and third dimensions (the i and j dimensions) is that we get the weighted sum for each stimulus/weight matrix pair. The result of `sum(stimuli[:, None, :, :] * weightMatrices, axis = (2, 3))` is an array with shape (1000, T * R * W) where entry i,j of the matrix is the sum of all of the elements in the matrix that you get by element-wise multiplying a stimulus with a weight matrix for stimulus i and weight matrix j.

The last thing we do in this line of code is divide by **summedWeightMatrices**. Since the numerator is of shape (1000, T * R * W) and **summedWeightMatrices** is of shape (T * R * W), we once again take advantage of numpy broadcasting and thus extend the values in **summedWeightMatrices** to match the shape. The result is that the resulting **stimuliMeans** matrix gets its entries according to the following equation...

$$
stimuliMeans_{i,j} = \frac{numerator_{i,j}}{summedWeightMatrices_{j}}
$$

The next line of code we need to talk about is as follows...
```
stimuliMeanDifferences = stimuli[:, None, :, :] - stimuliMeans[:, :, None, None]
```
This is more numpy broadcasting at work, but this is the part where we calculate the differences between pixels over all 1000 stimuli in the batch and the mean of the stimulus that we see in many of the equations for the weighted pearson score listed above. I won't go into extreme detail about how the broadcasting works here, but I will tell you what you will find in the resulting **stimuliMeanDifferences** matrix.

$$
stimuliMeanDifferences_{b, k, i, j} = stimuli_{b, i, j} - stimuliMeans_{b, k}
$$

which translates to "the i,j'th pixel from the b'th stimulus minus the weighted mean of the b'th stimulus's k'th weight matrix" (or something to that effect). Essentially this just does nice centered stuff around the mean work for us.

Let's examine the following line of code in terms of the part of the weighted pearson function it calculates...

```
numerator = sum(weightMatrices[None, :, :, :] * stimuliMeanDifferences * weightedMeanDifferences, axis=(2, 3))
```

and remember that the numerator of the weighted pearson score is just the weighted covariance of the stimulus S and the template T.

$$
    WeightedCovariance(S, T) = \frac{\sum_{i = 0}^{imageHeight - 1}{\sum_{j = 0}^{imageWidth - 1}{WeightMatrix_{i,j} * (S_{i,j} - \overline{WS}) * (T_{i,j} - \overline{WT})}}}{\sum_{i = 0}^{imageHeight - 1}{\sum_{j = 0}^{imageWidth - 1}{WeightMatrix_{i,j}}}}
$$

If you remember from our precalculating section, **weightedMeanDifferences** accounts for the $(T_{i,j} - \overline{WT})$ part of this equation, the **stimuliMeanDifferences** we calculated earlier in this function accounts for the $(S_{i,j} - \overline{WS})$ part of this equation, and the initial multiplication by **weightMatrices** accounts for the $WeightMatrix_{i,j}$ part of the equation. Then we sum over the second and third axes which accounts for the $\sum_{i = 0}^{imageHeight - 1}{\sum_{j = 0}^{imageWidth - 1}{}}$ part of the equation. You may notice that we do not calculate the denominator of this equation. That is because the denominator here will cancel out with the denominators in the denominator. Feel free to check this yourself using the equations above. You will have a denominator squared in the denominator which you can pull out of the square root we use, and it will perfectly cancel with the denominator from the numerator. We then calculate the Covariance of the stimulus with itself and the covariance of the template with itself and then multiply to get the denominator. Finally, we return the numerators divided by the denominators. This returns a matrix with shape (1000, T * R * W) containing the pearson scores of every stimulus + template/relevant point scheme/weighting scheme combination in this batch. This matrix gets returned to **processAndStoreResults**.

```
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
```
We then insert those results into their proper place within the **results** array using ``results[start: end] = batchResults``. This function then terminates and we are back within the template specific function. 

```
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
```
Specifically we are located in the for loop. Once the for loop terminates, it means that we have calculated the pearson score for all of the stimuli and for all of the templates/relevant point schemes/weighting schemes. Hurray! All of the hard stuff is done. Finally, we use `save(os.path.join(savePath, 'hiAnalysis.npy'), results)` to save the (1 million, T * R * W) array with all of our results, and we save the object that lets us convert between indices and tempalte/relevant point schemes/weighting scheme combinations. Hurray! Now we are done!!!!!







