import os


def listDirectory(parentPath, childName):
    fullPath = os.path.join(parentPath, childName)
    print(f'\n\n\n\n======== Current subDirectory: {childName} ========')
    i = 0
    for stimulus in os.listdir(fullPath):
        print(f"'{stimulus}'", end = ', ')
        i += 1
    print(f'\n\nCount: {i}')
    # # print block ones
    # i = 0
    # print('\n\nBlock One Hs')
    # for stimulus in os.listdir(fullPath):
    #     if 'BlockOneH' in stimulus:
    #         print(f'{stimulus},')
    #         i += 1
    # print(f'Count: {i}')
    
    # print('\n\nBlock Two Hs')
    # for stimulus in os.listdir(fullPath):
    #     if 'BlockTwoH' in stimulus:
    #         print(f'{stimulus},')
    #         i += 1
    # print(f'Count: {i}')

    # print('\n\nI Stimuli')
    # for stimulus in os.listdir(fullPath):
    #     if f'{childName}I' in stimulus:
    #         print(f'{stimulus},')
    #         i += 1
    # print(f'Count: {i}')
    
    # print('\n\nUncorrelated Stimuli')
    # for stimulus in os.listdir(fullPath):
    #     if 'Uncorrelated' in stimulus:
    #         print(f'{stimulus},')
    #         i += 1
    # print(f'Count: {i}')


def main():

    # path to parent directory of stimuli
    stimuliPath = os.path.join(os.path.dirname(__file__), 'newStimuli')

    # list the images in the unweighted and gaussian subdirectories
    listDirectory(stimuliPath, 'unweighted')
    #listDirectory(stimuliPath, 'gaussian')
if __name__ == '__main__':
    main()