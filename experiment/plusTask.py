# tests have been run and there is no overlapping stimuli
from psychopy import visual, core
from helperFunctions import *
import random

# The experiment itself
def experiment(weightingScheme, blockType, targetStimuli, distractorStimuli, savePath, win, mouse):
    win.color = altBackgroundColor

    # various variables for handling the game
    reset = False
    startTime = core.Clock()
    
    # select an initial image
    image, stimulusNumber, imageType = selectStimulus(targetStimuli, distractorStimuli, weightingScheme, win)

    # Loop for handling events
    while True:
        mouse.setVisible(False)

        # handling key presses
        for key in event.getKeys():

            # quit the experiment key
            if key == 'escape':
                win.close()
                core.quit()

            # handle response keys (y for "yes, the stimulus is here". "n" otherwise)
            elif key == 'y' or key == 'n':

                # indicates we will reset the experiment once a response is selected
                reset = True

                # user's response to a stimulus
                if key == 'y':
                    response = 'target'
                else:
                    response = 'distractor'

                # saves user's response
                responseTime = startTime.getTime()
                recordResponse(subjectName, subjectNumber, weightingScheme, blockType, stimulusNumber, imageType, response, responseTime, savePath)
            
        # while the trial continues on just keep the image on the screen until they give a response
        if not reset:
            mouse.setVisible(False)
            image.draw()
            mouse.setVisible(False)
            win.flip()
            
        # end of a trial
        else:

            # clear the events 
            reset = False
            win.flip()
            event.clearEvents()
            
            # end experiment if we have shown all of the images
            if (len(targetStimuli) == 0 and len(distractorStimuli) == 0):
                return
            
            # otherwise select a new image
            image, stimulusNumber, imageType = selectStimulus(targetStimuli, distractorStimuli, weightingScheme, win)
            mouse.setVisible(False)

            # reset the trial timer
            startTime.reset()


# handles the overall experiment flow
if __name__ == '__main__':
    
    # initialize window and mouse object (set mouse to invisible)
    win = visual.Window(size = (winWidth, winHeight), pos = (winX, winY), fullscr = True, color = backgroundColor)
    mouse = event.Mouse(win = win)
    mouse.setVisible(False)
    
    # get user info and where to store their results
    subjectName, subjectNumber = getSubjectInfo(win, mouse)
    saveFolder = os.path.join(os.path.dirname(__file__), 'results', subjectNumber)
    os.makedirs(saveFolder, exist_ok = True)

    # gets the top rated Hs, top rated Is and noisy images
    gaussianHStimuli, gaussianIStimuli, gaussianNoCorrelationStimuli, unweightedHStimuli, unweightedIStimuli, unweightedNoCorrelationStimuli = getStimuli()
    blockOneGaussianHStimuli, blockTwoGaussianHStimuli = splitStimuli(gaussianHStimuli)
    blockOneUnweightedHStimuli, blockTwoUnweightedHStimuli = splitStimuli(unweightedHStimuli)

    # selecting different experimental and block schemes
    weightingSchemes = ['gaussian', 'unweighted']
    blocktypes = ['noCorrelation', 'iCorrelation']

    weightingScheme = random.choice(weightingSchemes)
    initialBlockType = random.choice(blocktypes)

    experimentExplanation(win, 'H', mouse)
    realInstructions(win, 'H', mouse)
    if weightingScheme == 'gaussian':
        if initialBlockType == 'noCorrelation':
            experiment('gaussian', 'noCorrelation', blockOneGaussianHStimuli, gaussianNoCorrelationStimuli, saveFolder, win, mouse)
            breakScreen(win, mouse)
            showTemplate('H', win, mouse)
            experiment('gaussian', 'iCorrelation', blockTwoGaussianHStimuli, gaussianIStimuli, saveFolder, win, mouse)
        else:
            experiment('gaussian', 'iCorrelation', blockOneGaussianHStimuli, gaussianIStimuli, saveFolder, win, mouse)
            breakScreen(win, mouse)
            showTemplate('H', win, mouse)
            experiment('gaussian', 'noCorrelation', blockTwoGaussianHStimuli, gaussianNoCorrelationStimuli, saveFolder, win, mouse)

    else:
        if initialBlockType == 'noCorrelation':
            experiment('unweighted', 'noCorrelation', blockOneUnweightedHStimuli, unweightedNoCorrelationStimuli, saveFolder, win, mouse)
            breakScreen(win, mouse)
            showTemplate('H', win, mouse)
            experiment('unweighted', 'iCorrelation', blockTwoUnweightedHStimuli, unweightedIStimuli, saveFolder, win, mouse)
        else:
            experiment('unweighted', 'iCorrelation', blockOneUnweightedHStimuli, unweightedIStimuli, saveFolder, win, mouse)
            breakScreen(win, mouse)
            showTemplate('H', win, mouse)
            experiment('unweighted', 'noCorrelation', blockOneUnweightedHStimuli, unweightedNoCorrelationStimuli, saveFolder, win, mouse)
        

    # exit screen thanking participant
    exitScreen(win, mouse)

    writeSummaryData(subjectName, subjectNumber, weightingScheme, initialBlockType, saveFolder)