import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from imageProcessing.templateSpecificFunctions.fullscreenCrosses import main as fullscreen
from imageProcessing.templateSpecificFunctions.halfscreenCrosses import main as halfscreen
from imageProcessing.templateSpecificFunctions.hiAnalysis import main as hi
from imageProcessing.templateSpecificFunctions.S import main as S
from helpers.imports import *

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