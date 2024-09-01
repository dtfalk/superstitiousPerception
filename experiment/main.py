# tests have been run and there is no overlapping stimuli
from psychopy import visual, core, monitors
from helperFunctions import *

# The experiment itself
def experiment(subjectName, subjectNumber, weightingScheme, blockType, targetStimuli, distractorStimuli, savePath, win, mouse, stimSize):
    win.color = altBackgroundColor

    # various variables for handling the game
    reset = False
    startTime = core.Clock()
    
    # select an initial image
    image, stimulusNumber, imageType = selectStimulus(targetStimuli, distractorStimuli, weightingScheme, win, stimSize)

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
                recordResponse(subjectName, subjectNumber, weightingScheme, blockType, stimulusNumber, imageType, response, str(responseTime), savePath)
                event.clearEvents()
                win.color = altBackgroundColor
                win.flip()
                time.sleep(2)
            
        # while the trial continues on just keep the image on the screen until they give a response
        if not reset:
            mouse.setVisible(False)
            image.draw()
            mouse.setVisible(False)
            win.flip()
            mouse.setVisible(False)
            
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
            image, stimulusNumber, imageType = selectStimulus(targetStimuli, distractorStimuli, weightingScheme, win, stimSize)
            mouse.setVisible(False)

            # reset the trial timer
            startTime.reset()


# handles the overall experiment flow
def main():

    monitor = monitors.Monitor('main')

    # Specify the physical size of the monitor in centimeters (width, height)
    monitor.setSizePix([winWidth, winHeight]) 
    monitor.setWidth(30.15)  
    monitor.setDistance(60.96)  

    # Get the size in pixels for 2 degrees of visual angle
    stim_size_degrees = 2
    stimSize = round(deg2pix(stim_size_degrees, monitor))

    # Calculate the size of the stimulus in pixels
    #stimSize = monitor.getSizePix()[0] * (stim_size_cm / monitor.getWidth())

    # initialize window and mouse object (set mouse to invisible)
    win = visual.Window(size = (winWidth, winHeight), pos = (winX, winY), fullscr = True, monitor = monitor, color = backgroundColor)
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
    weightingScheme, initialBlockType = selectExperimentType()

    experimentExplanation(win, 'H', mouse)
    event.clearEvents()
    realInstructions(win, 'H', mouse, stimSize)
    event.clearEvents()
    if weightingScheme == 'gaussian':
        if initialBlockType == 'noCorrelation':
            experiment(subjectName, subjectNumber, 'gaussian', 'noCorrelation', blockOneGaussianHStimuli, gaussianNoCorrelationStimuli, saveFolder, win, mouse, stimSize)
            event.clearEvents()
            breakScreen(win, mouse)
            event.clearEvents()
            showTemplate('H', win, mouse, stimSize)
            event.clearEvents()
            experiment(subjectName, subjectNumber, 'gaussian', 'iCorrelation', blockTwoGaussianHStimuli, gaussianIStimuli, saveFolder, win, mouse, stimSize)
            event.clearEvents()
        else:
            experiment(subjectName, subjectNumber, 'gaussian', 'iCorrelation', blockOneGaussianHStimuli, gaussianIStimuli, saveFolder, win, mouse, stimSize)
            event.clearEvents()
            breakScreen(win, mouse)
            event.clearEvents()
            showTemplate('H', win, mouse, stimSize)
            event.clearEvents()
            experiment(subjectName, subjectNumber, 'gaussian', 'noCorrelation', blockTwoGaussianHStimuli, gaussianNoCorrelationStimuli, saveFolder, win, mouse, stimSize)
            event.clearEvents()

    else:
        if initialBlockType == 'noCorrelation':
            experiment(subjectName, subjectNumber, 'unweighted', 'noCorrelation', blockOneUnweightedHStimuli, unweightedNoCorrelationStimuli, saveFolder, win, mouse, stimSize)
            event.clearEvents()
            breakScreen(win, mouse)
            event.clearEvents()
            showTemplate('H', win, mouse, stimSize)
            event.clearEvents()
            experiment(subjectName, subjectNumber, 'unweighted', 'iCorrelation', blockTwoUnweightedHStimuli, unweightedIStimuli, saveFolder, win, mouse, stimSize)
            event.clearEvents()
        else:
            experiment(subjectName, subjectNumber, 'unweighted', 'iCorrelation', blockOneUnweightedHStimuli, unweightedIStimuli, saveFolder, win, mouse, stimSize)
            event.clearEvents()
            breakScreen(win, mouse)
            event.clearEvents()
            showTemplate('H', win, mouse, stimSize)
            event.clearEvents()
            experiment(subjectName, subjectNumber, 'unweighted', 'noCorrelation', blockTwoUnweightedHStimuli, unweightedNoCorrelationStimuli, saveFolder, win, mouse, stimSize)
            event.clearEvents()
        

    # exit screen thanking participant
    exitScreen(win, mouse)

    writeSummaryData(subjectName, subjectNumber, weightingScheme, initialBlockType, saveFolder)

if __name__ == '__main__':
    main()