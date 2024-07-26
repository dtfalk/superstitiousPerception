import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from postProcessing.compositeImages.main import main as compositeImages
from postProcessing.crossCorrelations.main import main as crossCorrelation
from postProcessing.generalStatistics.main import main as generalStatistics
from postProcessing.csvGeneration.main import main as csvGeneration
from postProcessing.principalComponentAnalysis.main import main as principalComponentAnalysis
import time


def main():
    print('    Post-processing starting now...')
    startTime = time.time()
    csvGeneration()
    generalStatistics()
    compositeImages()
    crossCorrelation()
    principalComponentAnalysis()
    print('\n    Post-processing runtime: %.4f'%(time.time() - startTime))

if __name__ == '__main__':
    main()