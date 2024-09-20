import sys
import os

# Add the parent directory to the system path
sys.path.append( os.path.dirname(os.path.dirname(os.path.dirname(os.path.join(os.path.abspath(__file__))))))

from postProcessing.generalStatistics.templateSpecificFunctions.fullscreenCrosses import main as fullscreen
from postProcessing.generalStatistics.templateSpecificFunctions.halfscreenCrosses import main as halfscreen
from postProcessing.generalStatistics.templateSpecificFunctions.hiAnalysis import main as hi
from postProcessing.generalStatistics.templateSpecificFunctions.S import main as s
from postProcessing.generalStatistics.helpers.imports import *


def main():
    print('\n\n        General statistics starting now...\n')
    startTime = time.time()
    # fullscreen()
    # halfscreen()
    hi()
    # s()
    print('\n        Runtime for calculating general statistics: %.4f seconds'%(time.time() - startTime))

if __name__ == '__main__':
    main()