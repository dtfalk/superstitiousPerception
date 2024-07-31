import os
import csv
import time
import random
from scipy.stats import norm
from psychopy import visual, core, event
from constants import *

imageWidth, imageHeight = 51, 51
imageSize = imageWidth * imageHeight
scaleFactor = 0.5 * (winHeight / imageHeight)
scaledImageSize = (imageWidth * scaleFactor, imageHeight * scaleFactor)

# This block of code handles lab streaming layer functionality
# =======================================================================
# =======================================================================

# # Initializes lab streaming layer outlet
# def initializeOutlet():
#     infoEvents = StreamInfo('eventStream', 'events', 1, 0, 'string')
#     outlet = StreamOutlet(infoEvents)
#     return outlet

# # pushes a sample to the outlet
# def pushSample(outlet, tag):
#     outlet.push_sample([tag])

# =======================================================================
# =======================================================================



# These functions are for collecting/saving user/experiment data
# =======================================================================
# =======================================================================

# gets the subject name, subject number, metric type and distance type
def getSubjectInfo(win, mouse):
    subjectName = getSubjectName(win, mouse)
    subjectNumber = getSubjectNum(win, mouse)
    
    return subjectName, subjectNumber

# gets the subject's name
def getSubjectName(win, mouse):
    mouse.setVisible(False)
    namePrompt = 'Subject Name: '
    subjectName = ''
    
    while True:
        mouse.setVisible(False)
        keys = event.getKeys()
        for key in keys:
            if key == quitKey:
                win.close()
                core.quit()
                return
            elif key == 'return':
                return subjectName
            elif key == 'backspace':
                if subjectName != '':
                    subjectName = subjectName[:-1]
            elif key == 'space':
                subjectName = subjectName + ' '
            elif key in validLetters:
                subjectName = subjectName + key
        mouse.setVisible(False)
        prompt = visual.TextStim(win = win, text = namePrompt + subjectName, height = 0.2, color = textColor)
        mouse.setVisible(False)
        prompt.draw()
        mouse.setVisible(False)
        win.flip()
        mouse.setVisible(False)

# gets the subject number
def getSubjectNum(win, mouse):
    mouse.setVisible(False)
    numPrompt = 'Subject Number: '
    subjectNum = ''
    
    while True:
        mouse.setVisible(False)
        keys = event.getKeys()
        for key in keys:
            if key == quitKey:
                win.close()
                core.quit()
                return
            elif key == 'return':
                return subjectNum
            elif key == 'backspace':
                if subjectNum != '':
                    subjectNum = subjectNum[:-1]
            elif key in validNumbers:
                subjectNum = subjectNum + key
        mouse.setVisible(False)
        prompt = visual.TextStim(win = win, text = numPrompt + subjectNum, height = 0.2, color = textColor)
        mouse.setVisible(False)
        prompt.draw()
        mouse.setVisible(False)
        win.flip()
        mouse.setVisible(False)

# records a user's response to a given trial
def recordResponse(subjectName, subjectNumber, weightingScheme, blockType, stimulusNumber, stimulusType, response, responseTime, savePath):
    
    # path to the save file
    filePath = os.path.join(savePath, f'{blockType}.csv')

    # prepare the header and the data
    header = ['Subject Name', 'Subject Number', 'Weighting Scheme', 'Distractor Type', 'Stimulus Number', 'Stimulus Type', 'Subject Response', 'Response Time']
    data = [subjectName, subjectNumber, weightingScheme, blockType, stimulusNumber, stimulusType, response, responseTime]

    # if csv file does not exist, then write the header and the data
    if not os.path.exists(filePath):
        with open(filePath, 'w', newline = '') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerow(data)

    # otherwise just write the data
    else:
        with open(filePath, 'a', newline = '') as file:
            writer = csv.writer(file)
            writer.writerow(data)
    return

# calculates a dprime score
def calculateDprime(hits, misses, correctRejections, falseAlarms):
    
    hitRate = hits / (hits + misses)
    falseAlarmRate = falseAlarms / (falseAlarms + correctRejections)

    # values for fixing extreme d primes
    halfHit = 0.5 / (hits + misses)
    halfFalseAlarm = 0.5 / (misses + correctRejections)

    if hitRate == 1:
        hitRate = 1 - halfHit
    if hitRate == 0:
        hitRate = halfHit
    if falseAlarmRate == 1:
        falseAlarmRate = 1 - halfFalseAlarm
    if falseAlarmRate == 0:
        falseAlarmRate = halfFalseAlarm

    # calculate z values
    hitRateZScore = norm.ppf(hitRate)
    falseAlarmRateZScore = norm.ppf(falseAlarmRate)

    # calculate d prime
    dprime = hitRateZScore - falseAlarmRateZScore

    return dprime

# writes summary data about user's performance
def writeSummaryData(subjectName, subjectNumber, weightingScheme, initialBlockType, savePath):

    filePath = os.path.join(savePath, 'summaryData.csv')
    loadPathUncorrelated = os.path.join(savePath, 'noCorrelation.csv')
    loadPathIcorrelated = os.path.join(savePath, 'iCorrelation.csv')

    # prepare header and data (minus dprimes)
    summaryDataHeader = ['Subject Name', 'Subject Number', 'Weighting Scheme', 'First Block Type', 'No Correlation Block Dprime', 'I-Correlated Block Dprime']
    summaryDatadata = [subjectName, subjectNumber, weightingScheme, initialBlockType]

    # caclulate dprimes for uncorrelated distractors
    with open(loadPathUncorrelated, mode = 'r', newline = '') as f:
        reader = csv.reader(f)
        lines = list(reader)
        header = lines[0]
        data = lines[1:]

        # create a dictionary to easily access data entries
        indices = {}
        for i, entry in enumerate(header):
            indices[entry] = i

        # collecting relevant data for calculating dprime
        hits = 0
        misses = 0
        falseAlarms = 0
        correctRejections = 0

        for entry in data:
            if entry[indices['Stimulus Type']] == 'target' and entry[indices['Subject Response']] == 'target':
                hits += 1
            elif entry[indices['Stimulus Type']] == 'target' and entry[indices['Subject Response']] == 'distractor':
                misses += 1
            elif entry[indices['Stimulus Type']] == 'distractor' and entry[indices['Subject Response']] == 'target':
                falseAlarms += 1
            else:
                correctRejections += 1
        
        dprime = calculateDprime(hits, misses, correctRejections, falseAlarms)
        summaryDatadata.append(str(dprime))


    # caclulate dprimes for uncorrelated distractors
    with open(loadPathIcorrelated, mode = 'r', newline = '') as f:
        reader = csv.reader(f)
        lines = list(reader)
        header = lines[0]
        data = lines[1:]

        # create a dictionary to easily access data entries
        indices = {}
        for i, entry in enumerate(header):
            indices[entry] = i


        # collecting relevant data for calculating dprime
        hits = 0
        misses = 0
        falseAlarms = 0
        correctRejections = 0

        for entry in data:
            if entry[indices['Stimulus Type']] == 'target' and entry[indices['Subject Response']] == 'target':
                hits += 1
            elif entry[indices['Stimulus Type']] == 'target' and entry[indices['Subject Response']] == 'distractor':
                misses += 1
            elif entry[indices['Stimulus Type']] == 'distractor' and entry[indices['Subject Response']] == 'target':
                falseAlarms += 1
            else:
                correctRejections += 1
        
        dprime = calculateDprime(hits, misses, correctRejections, falseAlarms)
        summaryDatadata.append(str(dprime))

    # write results to summary data file
    with open(filePath, mode = 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(summaryDataHeader)
        writer.writerow(summaryDatadata)
        


# =======================================================================
# =======================================================================
        
# a lists of the stimuli
def getStimuli():
    
    # get the current file's path
    curDir = os.path.dirname(__file__)

    # get paths to the gaussian stimuli
    gaussianHPath = os.path.join(curDir, 'stimuli', 'gaussianH')
    gaussianIPath = os.path.join(curDir, 'stimuli', 'gaussianI')
    gaussianNoCorrelationPath = os.path.join(curDir, 'stimuli', 'gaussianUncorrelated')

    # get the paths to the unweighted stimuli
    unweightedHPath = os.path.join(curDir, 'stimuli', 'unweightedH')
    unweightedIPath = os.path.join(curDir, 'stimuli', 'unweightedI')
    unweightedNoCorrelationPath = os.path.join(curDir, 'stimuli', 'unweightedUncorrelated')

    # get the gaussian stimuli as lists of file names
    gaussianHStimuli = os.listdir(gaussianHPath)
    gaussianIStimuli = os.listdir(gaussianIPath)
    gaussianNoCorrelationStimuli = os.listdir(gaussianNoCorrelationPath)

    # get the unweighted stimuli as lists of file names
    unweightedHStimuli = os.listdir(unweightedHPath)
    unweightedIStimuli = os.listdir(unweightedIPath)
    unweightedNoCorrelationStimuli = os.listdir(unweightedNoCorrelationPath)

    return gaussianHStimuli, gaussianIStimuli, gaussianNoCorrelationStimuli, unweightedHStimuli, unweightedIStimuli, unweightedNoCorrelationStimuli

# split an uncorrelated bunch of stimuli into two lists
def splitStimuli(stimuli):
    blockOneStimuli = [stimulus for i, stimulus in enumerate(stimuli) if i % 2 == 0]
    blockTwoStimuli = [stimulus for i, stimulus in enumerate(stimuli) if i % 2 == 1]

    return blockOneStimuli, blockTwoStimuli


# This code is for showing various message screens (e.g. experiment explanation)
# =======================================================================
# =======================================================================

# explains the experiment to the subject
def experimentExplanation(win, letter, mouse):
    
    # text height and preparing the explanation text
    win.color = backgroundColor
    height = 0.07
    prompt = visual.TextStim(win = win, text = explanationText(letter), height = height,
                            color = textColor, wrapWidth = 1.9, alignText = 'left')
    
    # wait for the user to press spacebar before the experiment continues
    while True:
        mouse.setVisible(False)
        keys = event.getKeys()
        for key in keys:
            if key == quitKey:
                win.close()
                core.quit()
            if key == continueKey:
                return
        prompt.draw()
        win.flip()

# instructions for the real trials
def realInstructions(win, letter, mouse):
    
    # text height and preparing the instructions text
    win.color = backgroundColor
    height = 0.07
    prompt = visual.TextStim(win = win, text = realText(letter), height = height,
                            color = textColor, wrapWidth = 1.9, alignText = 'left')
    
    # wait for the user to press spacebar before the experiment continues
    while True:
        mouse.setVisible(False)
        keys = event.getKeys()
        for key in keys:
            if key == quitKey:
                win.close()
                core.quit()
                return
            if key == continueKey:
                showTemplate(letter, win, mouse)
            return
        prompt.draw()
        win.flip()

# shows the stimulus in the "show template once" condition
def showTemplate(letter, win, mouse):

    win.color = altBackgroundColor
    startTime = time.time()
    curDir = os.path.dirname(__file__)
    templateImagePath = os.path.join(curDir, 'templates', f'{letter}.png')
    image = visual.ImageStim(win = win, image = templateImagePath, size = scaledImageSize, units = 'pix')

    # wait for the user to press spacebar before the experiment continues
    while time.time() - startTime < 10:
        mouse.setVisible(False)
        keys = event.getKeys()
        for key in keys:
            if key == quitKey:
                win.close()
                core.quit()
                return
        image.draw()
        win.flip()
    return
    
# exit screen thanking the participant
def breakScreen(win, mouse):

    win.color = backgroundColor
    # text height and preparing the exit screen text
    height = 0.07
    prompt = visual.TextStim(win = win, text = breakScreenText, height = height,
                            color = textColor, wrapWidth = 1.9, alignText = 'left')
    prompt.draw()
    win.flip()
    # wait for the user to press spacebar before the experiment continues
    while True:
        mouse.setVisible(False)
        keys = event.getKeys()
        for key in keys:
            if key == quitKey:
                win.close()
                core.quit()
                return
            if key == breakScreenKey:
                return
        prompt.draw()
        win.flip()

# exit screen thanking the participant
def exitScreen(win, mouse):

    # text height and preparing the exit screen text
    win.color = backgroundColor
    height = 0.07
    prompt = visual.TextStim(win = win, text = exitScreenText, height = height,
                            color = textColor, wrapWidth = 1.9, alignText = 'left')
    prompt.draw()
    win.flip()
    # wait for the user to press spacebar before the experiment continues
    while True:
        mouse.setVisible(False)
        keys = event.getKeys()
        for key in keys:
            if key == quitKey:
                win.close()
                core.quit()
                return
            if key == continueKey:
                return
        prompt.draw()
        win.flip()

# =======================================================================
# =======================================================================
    
def selectStimulus(targetStimuli, distractorStimuli, weightingScheme, win):

    # select a stimulus and remove it from its associated list
    masterList = targetStimuli.copy() + distractorStimuli.copy()
    stimulus = random.choice(masterList)
    if stimulus in targetStimuli:
        imageType = 'target'
        targetStimuli.remove(stimulus)
    else:
        imageType = 'distractor'
        distractorStimuli.remove(stimulus)

    # get the path to the image selected
    imagePath = os.path.join(os.path.dirname(__file__), 'stimuli', weightingScheme,  stimulus)

    # present the image
    image = visual.ImageStim(win = win, image = imagePath, size = scaledImageSize, units = 'pix')

    return image, stimulus.replace('.png', ''), imageType
    