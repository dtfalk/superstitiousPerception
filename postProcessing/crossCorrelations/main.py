import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.join(os.path.abspath(__file__))))))

from postProcessing.crossCorrelations.templateSpecificFunctions.fullscreenCrosses import main as fullscreen
from postProcessing.crossCorrelations.templateSpecificFunctions.halfscreenCrosses import main as halfscreen
from postProcessing.crossCorrelations.templateSpecificFunctions.hiAnalysis import main as hi
from postProcessing.crossCorrelations.templateSpecificFunctions.S import main as s
from postProcessing.crossCorrelations.helpers.imports import *


def main():
    print('\n\n        Cross-correlations starting now...\n')
    startTime = time.time()
    # fullscreen()
    # halfscreen()
    hi()
    # s()
    print('\n        Runtime for calculating cross-correlations: %.4f seconds'%(time.time() - startTime))

if __name__ == '__main__':
    main()