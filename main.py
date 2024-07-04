from imageGeneration.main import main as generateImagesAndArrays
from imageProcessing.main import main as imageProcessing
from postProcessing.main import main as postProcessing
import time

def main():
    print('\n\nImage generation and analysis starting now...')
    startTime = time.time()
    generateImagesAndArrays()
    imageProcessing()
    postProcessing()
    print('\n\nOverall Runtime: %.4f\n\n'%(time.time() - startTime))

if __name__ == '__main__':
    main()