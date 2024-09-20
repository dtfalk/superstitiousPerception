import sys
import os

# # Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from imageGeneration.templateSpecificFunctions.fullCrosses import main as fullCrosses
from imageGeneration.templateSpecificFunctions.halfCrosses import main as halfCrosses
from imageGeneration.templateSpecificFunctions.hi import main as hi
from imageGeneration.templateSpecificFunctions.features import main as features
from imageGeneration.templateSpecificFunctions.sImage import main as sImage
from imageGeneration.stimuli import main as stimuli
from imageGeneration.constants import *
from imageGeneration.imports import *

# run the entire arrays/image making process
def main():
    print('\n\n    Template and stimuli generation starting now...\n')
    # keep track of timing
    startTime = time.time()

    # run code for creating templates
    #fullCrosses()
    #halfCrosses()
    hi()
    features()
    #sImage()

    # run code for creating stimuli
    stimuli()

    # print timing results
    print('\n    Runtime for all templates and %d stimuli: %.4f seconds\n\n\n' %(numImages, time.time() - startTime))

if __name__ == '__main__':
    main()