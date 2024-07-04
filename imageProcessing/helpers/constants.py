# number of images to generate
numImages = 10 ** 6

# defining a color 
WHITE = (255, 255, 255)

# batch size variable
batchSize = 1000

# widths for our template crosses (actual width is [(2 * width) + 1] pixels)
widths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# types of relevant point schemes used for calculating weights matrices
# 1. distance from stimuli returns 0 distance if pixel is within the stimuli
# 2. distance from border returns the pixel's distance from the nearest border
relevantPointSchemes = ['anyAll', 'borders']

# distance metrics we use for calculating weights matrices
weightingSchemes = ['linear', 'quadratic', 'logarithmic', 'gaussian', 'central', 'unweighted']


sigma = 1 # constant for gaussian measure