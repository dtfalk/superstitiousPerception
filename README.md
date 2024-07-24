**TODOs**
1. use permutation test to check rank order on top 100 and top 10? Spearman should only be used for >500 samples according to scipy.stats.pearsonr documentation. Should prolly just look into the metric itself.
2. Principal component analysis

**Author**: David Tobias Falk

**Contact Info:**
    Email: dtfalk@uchicago.edu, davidtobiasfalk@gmail.com
    Cell: 1-413-884-2553 (please text first or I will assume that you are spam)

# **Superstitious Perception Task**
Hello! My name is David Falk, currently an employee at the APEX Lab at the University of Chicago. This repo contains a PsychoPy version of an experiment and a lot of code for creating and analyzing images. This README will primarily focus on the image generation and analysis code because the experimental paradigm is currently in flux. When that is sorted out I will make those modifications and (hopefully) update this document. The image creation and analysis code is broken up into three parts: **image generation**, **image processing**, and **post processing**. I will go into how each of these parts of the code work. Every folder has a **main.py** file that runs every bit of code in that folder. So the main file in the root of the directory runs all three of the sections mentioned above and the main file in the image generation folder runs all of the image generation code. All of the main files follow the same format. Below is the main file in the image processing folder.

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

We are using multiple template schemes and it is possible (if not likely) that you will want to only use one type of template scheme, some subset of the existing template schemes, or create your own. Running all of the template schemes will significantly slow down your code. In order to do this all you have to do is comment out the template schemes that you don't want to use. In this example, if you only want to run the hiAnalysis and S template schemes, then just comment out the "fullscreen()" and "halfscreen()" lines. You will want to do this with all of the main files in the code, so it is slightly tedious but shouldn't take too long. All of the main files follow roughly the same structure.

## **Image Generation**
The code for this part of this task is located in the **imageGeneration** folder in this repository. This part of the code will generate our template images, a set number of random images (currently 1 million), and the associated numpy arrays for each template and each image. These images and arrays will be stored in a folder called **arraysAndImages** that is created once the code runs. 

The reason that we store both arrays and images is that images are essentially 2-dimensional arrays. Each pixel of an image (an element of an array) is an RGB value. The format in which images are stored (jpg, png, etc...) are slow in terms of loading and modifying, so for our computations we also store each image as a numpy array because array computations are faster, and numpy array operations are just about as fast as they get. Also note that we can store multiple images as a 3-dimensional array. If I want to store 10 images, with each image being size 51 x 51, then this array would have size of (10, 51, 51). Pretty neat, huh? Maybe not, but I find it neat, and this is my document so if you want to know what is going on, then you will be subjected to me pointing out things I think are fun and neat, even if they may be boring and/or obvious to you. Tough luck.

This folder has three relevant components: the **templateSpecificFunctions** folder, the **stimuli.py** file, and the **constants.py** file. 

### **Template Specific Functions Folder**
This folder contains the code for creating each template scheme. Currently, there are fullscreen crosses, halfscreen crosses, an S template, and the hiAnalysis/features code. The fullscreen crosses are crosses (think of the "+" sign) that extend from all the way to the left of the image to all the way to the right of the image and from the very bottom of the image to the very top of the image. The halfscreen crosses are the same thing except that the crosses extend from halfway to the left to halfway to the right, and half way from the bottom to halfway to the top. All of the template schemes are meant to be centered. The hiAnalysis/features code is a template "H" and template "I", which are identical images, except that they are rotated 90 degrees. The features part is each individual leg or cross in the H/I templates. It lets us analyze the component parts of each image. I will hopefully explain why analyzing the components is important in this or some follow up document, but this document is meant to be about the code, so I won't go on a tangent. The S template is a large S that relates to Shannon Heald/Howard Nusbaums' original go at this experiment.

### **stimuli.py**
This file creates the white noise images that we compare against the templates in the image processing part of the code. Each image is a greyscale image so instead of each pixel taking an RGB value, each pixel is just one number ranging from 0 to 255. We have an even simpler case, where each value is meant to be either a white pixel (pixel value = 255) or a black pixel (pixel value = 0). We implement this by using numpy's random number generator to randomly select a 0 or a 1 for each pixel, then multiply the whole array by 255. 255 * 0 = 0. 255 * 1 = 255. Then we convert to an image. Note that we **don't** multiply by 255 when we save as an array. So the arrays are just 0s or 1s. Since the analysis we do with these arrays involves normalizing the values, the statistical analysis is insensitive to the 0/255 vs 0/1 difference.

### **constants.py**
This contains various constants for easy modification of the code. Some important variables you can change are as follows...
1. *numImages*: This is the number of stimuli images that will be created when you run the main.py file (using "python main.py" in the terminal). It is currently set to 1 million (10 ^ 6)
2. *imageWidth* and *imageHeight*: These control the width and height of the images created. I reccomend keeping them equal if you decide to change them. I do not remember if I built this code to handle them being unequal. I doubt it is too difficult of a change though, but you will have to read and then understand the code.
3. *batchSize*: probably don't mess with this one. I have tried to change it and it results in a bug of some kind. I think it is some sort of memory issue. I haven't felt like examining it further yet. It works fast with batches of 1000, so I don't see much of a reason to change it. But hey, you do you.


## **Image Processing**
This folder is meant to analyze the images using a weighted pearson R score. A pearson R score tests the similarity between two 1-dimenstional vectors in a given vector space. Each image is a 51 x 51 2-dimensional array. If we flatten the array, then it becomes a 1-dimensional array with 2601 entries. The pearson r score gives us some idea of the similarity between the 1-dimensional version of each template and the 1-dimensional version of each of the one million stimuli. We weight the array according to multiple different weighting schemes. The idea is that using an unweighted array gives equal weight to each pixel in the image. However, we are telling subjects that the templates are centered. So we hypothesize that the pixels in the middle of the screen/near the actual template are more relevant to the subject than the pixels that are way off to the side of the image. I will (hopefully) create other documentation explaining each of these weighting schemes, but if you are curious then you can look in the **weightsAndDistances.py** file in the **imageProcessing/helpers** folder if you want to examine the different types of weighting schemes. The results to all these analyses are stored in the results folder as .npy files. In the post processing stage we break up the analyses by weighting scheme as write them to human readable csv files.

### **Important note**
Part of the speed of this program on my personal device relates to it using GPU processing instead of CPU processing. The way to think about the difference between these two is that the CPU is meant to handle a lot of different types of operations on your computer. As a result it has a lot of flexibility in what it can do, but it does each of these things slower. Furthermore, the CPU only has a couple (typically < 10) "cores". Cores are like workers. Having 4 workers means that your computer can do 4 things at a given time. GPUs on the other hand do very few things, and all of the things it does are fast and highly optimized. It also has thousands of cores, meaning it can do thousands of things at the same time. As you can image, if you have a set of tasks that your GPU has the ability to do (e.g. array calculations) and you properly take advantage of the thousands of cores (workers), then your code will run much much quicker. In this case, it likely does things hundreds if not thousands of times faster. This code does just that. It uses a python package called Cupy. It only works with computers that have Cupy compatible Nvidia GPUs. Cupy is basically Numpy, except Numpy does the operations on your CPU and Cupy does the operations on your GPU. If you happen to have a Cupy compatible Nvidia GPU, then use that!! This only applies to the image processing portion of the code, so everything that comes before or after will run at roughly the same speed (on my device this code takes about 10-20 minutes to run with 1 million images and all of the templates/weighting schemes). If your computer does not have such a GPU, then there are two changes you will need to make. First, you will need to use the **noCupySuperstitiousPerceptionEnvironment.yml** file for creating your virtual environment. This excludes the Cupy package from what packages get downloaded. Second, you will need to make a small change to the **imageProcessing/helpers/imports.py** file. Currently this file looks like this:

```
from cupy import sum, sqrt, square, zeros, load, uint8, pad, column_stack, nonzero, indices, ones_like, float32, log, exp, ones, save
#from numpy import sum, sqrt, square, zeros, load, uint8, pad, column_stack, nonzero, indices, ones_like, float32, log, exp, ones, save
import time
import csv
```

You need to comment out the first line by adding a "#" to the beginning of the first line and uncomment the second line by removing the "#" from the beginning of the second line. After doing this your code should look like this: 

```
#from cupy import sum, sqrt, square, zeros, load, uint8, pad, column_stack, nonzero, indices, ones_like, float32, log, exp, ones, save
from numpy import sum, sqrt, square, zeros, load, uint8, pad, column_stack, nonzero, indices, ones_like, float32, log, exp, ones, save
import time
import csv
```

All this does is switch the code from trying to use the Cupy (GPU) version of things to using the Numpy (CPU) version of things. This is all of the changes you should need to make.


## **Post Processing**
This folder contains the code for what we do once we have the pearson r correlation scores for each stimuli/template/weightingScheme combination. There are currently four operations contained in this folder: **generating CSV files with Pearson R scores**, **calculating general statistics**, **calculating composite images**, and **performing cross correlation analyses**. Let's give a description of each one.

### **Generating CSV files with Pearson R scores**
After storing the pearson r scores in numpy (.npy) files, we want them in a human readable format. Numpy files are binary files, so unless you are good at reading that, you will want something more legible with the pearson results. This folder takes each weighting scheme/template combination and creates a CSV file for it. So each file will have 1 million entries. It is ordered from highest score to lowest score and each line contains the stimulus number and its associated pearson r score.

### **Calculating general statistics**
This code takes the pearson r values we extracted in the previous step and calulates a minimum score, a maximum score, the range of scores (max - min), a mean score, a standard deviation of the scores for each template/weighting scheme combination and stores it as its own CSV file.

### **Calculating composite images**
For each template/weighting scheme combination there will be six composite images generated: top 10 stimuli, top 100 stimuli, top 1000 stimuli, bottom 10 stimuli, bottom 100 stimuli, and bottom 1000 stimuli. The top 100 stimuli will be an average of the top 100 stimuli given the template/weighting scheme combination. You will (hopefully) see some outline of the template in this "top" images, and will (hopefully) see a noisy grey image in the "bottom" images. These images are helpful for confirming we did the previous steps correctly, showing that we can extract some signal from the random set of 1 million stimuli, and for showing other people who may be skeptical.

### **Cross correlation Analyses**
An important part of our hypothesis is that changing the weighting scheme of the pixels will result in clearer results regarding which images subjects think that the template is "hidden" in. In part, we want to find out the math behind what subjects are attending to when they examine an image. We want our high scoring images to correspond to a higher probability of getting picked as an image that contains "signal" and we want our low scoring images to correspond to a higher probability of being identified as containing "noise". My preliminary analyses show that the pearson r scores for the weighted schemes are on average higher than the pearson r scores for the unweighted schemes, but that isn't necessarily helpful for proving or disproving our hypothesis. We want to see that *different* images are being selected. If all our weighting scheme does is select the same images but with inflated pearson r scores, then we haven't shown that our weighted approach is any different than our unweighted approach. What we want to see is that our weighted appraoch selects different images. As a result, we want to see that there is some difference in how the different weighting schemes rank the 1 million stimuli. That's what this code does using something called a "spearman r" score. This just takes two lists (the rankings of two different weighting schemes for a given template), and calculates a score ranging from -1 to 1 describing how similar the rankings of the stimuli are across the different weighting schemes. A score near 1 implies that the two weighting schemes produce very similar rankings of the stimuli, a score near -1 implies that the two weighting schemes produce inverted rankings of the stimuli, and a score near 0 implies that there is very little correlation between the rankings of the stimuli.

Thought: we want subjects to come back and analyze a whole bunch of images, not just select the top 100 from one weighting scheme or another. We want to see which weighting scheme is most predictive. We could do this with a couple of subjects as one study, and do the I vs H analysis as another study, and do Julien's study as a different study...
