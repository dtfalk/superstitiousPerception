import sys
import os

# Add the parent directory to the system path
sys.path.append( os.path.dirname(os.path.dirname(os.path.dirname(os.path.join(os.path.abspath(__file__))))))

from postProcessing.principalComponentAnalysis.templateSpecificFunctions.fullscreenCrosses import main as fullscreen
from postProcessing.principalComponentAnalysis.templateSpecificFunctions.halfscreenCrosses import main as halfscreen
from postProcessing.principalComponentAnalysis.templateSpecificFunctions.hiAnalysis import main as hi
from postProcessing.principalComponentAnalysis.templateSpecificFunctions.S import main as s
from postProcessing.principalComponentAnalysis.helpers.imports import *

def main():
    print('\n\n        Principal Component Analysis starting now...\n')
    startTime = time.time()
    fullscreen()
    halfscreen()
    hi()
    s()
    print('\n        Runtime for Principal Component Analysis: %.4f seconds'%(time.time() - startTime))


if __name__ == '__main__':
    main()