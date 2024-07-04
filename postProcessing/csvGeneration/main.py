import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from postProcessing.csvGeneration.templateSpecificFunctions.fullscreenCrosses import main as fullscreen
from postProcessing.csvGeneration.templateSpecificFunctions.halfscreenCrosses import main as halfscreen
from postProcessing.csvGeneration.templateSpecificFunctions.hiAnalysis import main as hi
from postProcessing.csvGeneration.templateSpecificFunctions.S import main as s
from helpers.imports import *


def main():
    print('\n        Pearson CSV data extraction starting now...\n')
    startTime = time.time()
    fullscreen()
    halfscreen()
    hi()
    s()
    print('\n        Runtime for extracting Pearson CSV data: %.4f seconds'%(time.time() - startTime))

if __name__ == '__main__':
    main()