import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from postProcessing.compositeImages.templateSpecificFunctions.fullscreenCrosses import main as fullscreen
from postProcessing.compositeImages.templateSpecificFunctions.halfscreenCrosses import main as halfscreen
from postProcessing.compositeImages.templateSpecificFunctions.hiAnalysis import main as hi
from postProcessing.compositeImages.templateSpecificFunctions.S import main as s
from postProcessing.compositeImages.helpers.imports import *


def main():
    print('\n\n        Composite images starting now...\n')
    startTime = time.time()
    fullscreen()
    halfscreen()
    hi()
    s()
    print('\n        Runtime for calculating composite images: %.4f seconds'%(time.time() - startTime))

if __name__ == '__main__':
    main()