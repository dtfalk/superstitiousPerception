import os
import shutil

def main():

    # make new folder for stimuli
    newSavePath = os.path.join(os.path.dirname(__file__), 'newStimuli')
    os.makedirs(os.path.join(newSavePath, 'unweighted'), exist_ok = True)
    os.makedirs(os.path.join(newSavePath, 'gaussian'), exist_ok = True)

    # path to existing stimuli
    stimuliFolderPath = os.path.join(os.path.dirname(__file__), 'stimuli')
    
    # add each stimuli to new folder with new naming scheme
    for folderName in os.listdir(stimuliFolderPath):
        folderPath = os.path.join(stimuliFolderPath, folderName)
        
        if 'unweighted' in folderName:
            savePath = os.path.join(newSavePath, 'unweighted')
        else:
            savePath = os.path.join(newSavePath, 'gaussian')

        for stimulusName in os.listdir(folderPath):
            stimulus = os.path.join(folderPath, stimulusName)
            shutil.copy(stimulus, os.path.join(savePath, f'{folderName}_{stimulusName}'))

if __name__ == '__main__':
    main()