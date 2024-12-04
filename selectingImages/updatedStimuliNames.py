import os
from time import time
import shutil

def main():

    startTime = time()

    # make new folder for stimuli
    newSavePath = os.path.join(os.path.dirname(__file__), 'cognitionRunNames')
    os.makedirs(os.path.join(newSavePath, 'unweighted'), exist_ok = True)
    os.makedirs(os.path.join(newSavePath, 'gaussian'), exist_ok = True)

    # path to existing stimuli
    stimuliFolderPath = os.path.join(os.path.dirname(__file__), 'stimuli')
    
    # add each stimuli to new folder with new naming scheme
    for folderName in os.listdir(stimuliFolderPath):
        folderPath = os.path.join(stimuliFolderPath, folderName)
        
        # find the overall folder paths for unweighted and gaussian
        if folderName != 'unweighted' and folderName != 'gaussian':
            if 'unweighted' in folderName:
                savePath = os.path.join(newSavePath, 'unweighted')
            else: 
                savePath = os.path.join(newSavePath, 'gaussian')

            # iterate over each file, rename it, and copy to new directory
            for stimulusName in os.listdir(folderPath):
                stimulusPath = os.path.join(folderPath, stimulusName)
                shutil.copy(stimulusPath, os.path.join(savePath, f'{folderName}_{stimulusName}'))
        else:
            continue
    
    # printing each list of stimuli for easy copy and paste
    unweighted = os.listdir(os.path.join(newSavePath, 'unweighted'))
    gaussian = os.listdir(os.path.join(newSavePath, 'gaussian'))

    print('\n\n\nUnweighted List')
    print('===============')
    for i, stimulus in enumerate(unweighted):
        if i == 0:
            print(f"['{stimulus}', ", end = '')
        elif i == len(unweighted) - 1:
            print(f"'{stimulus}]'", end = '')
        else:
            print(f"'{stimulus}', ", end = '')
    
    print('\n\n\nGaussian List')
    print('===============')
    for i, stimulus in enumerate(gaussian):
        if i == 0:
            print(f"'[{stimulus}', ", end = '')
        elif i == len(unweighted) - 1:
            print(f"'{stimulus}]'", end = '')
        else:
            print(f"'{stimulus}', ", end = '')

        
    # assure lengths of lists are as expected
    assert len(unweighted) == 400
    assert len(gaussian) == 400
    print('\n\n\n\nLength of each list confirmed to be 400!')

    # print total runtime
    print('Total Runtime: %.4f seconds\n'%(time() - startTime))

if __name__ == '__main__':
    main()