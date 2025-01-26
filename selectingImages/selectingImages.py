import os
import csv
import shutil
import numpy as np
from time import time


# Returns dictionaries with the stimulus number and its pearson result for a scheme
def load_dictionaries():

    # Path to the current directory
    curDir = os.path.dirname(__file__)

    # Paths to the Unweighted Hs and Is
    HPathUnweighted = os.path.join(curDir, '..', 'results', 'hiAnalysis', 'results', 'H', 'anyAll', 'unweighted', 'pearsonScores.csv')
    IPathUnweighted = os.path.join(curDir, '..', 'results', 'hiAnalysis', 'results', 'V', 'anyAll', 'unweighted', 'pearsonScores.csv')
    
    # Paths to the Gaussian-Weighted Hs and Is
    HPathGaussian = os.path.join(curDir, '..', 'results', 'hiAnalysis', 'results', 'H', 'anyAll', 'gaussian', 'pearsonScores.csv')
    IPathGaussian = os.path.join(curDir, '..', 'results', 'hiAnalysis', 'results', 'V', 'anyAll', 'gaussian', 'pearsonScores.csv')

    # Dictionaries to store results for quicker lookups
    H_Unweighted = {}
    I_Unweighted = {}
    H_Gaussian = {}
    I_Gaussian = {}

    # Loads each file into a dictionary
    with open(HPathUnweighted, mode = 'r', newline = '') as f:
        lines = list(csv.reader(f))[1:]
        for line in lines:
            H_Unweighted[line[0]] = line[1]
    with open(IPathUnweighted, mode = 'r', newline = '') as f:
        lines = list(csv.reader(f))[1:]
        for line in lines:
            I_Unweighted[line[0]] = line[1]
    with open(HPathGaussian, mode = 'r', newline = '') as f:
        lines = list(csv.reader(f))[1:]
        for line in lines:
            H_Gaussian[line[0]] = line[1]
    with open(IPathGaussian, mode = 'r', newline = '') as f:
        lines = list(csv.reader(f))[1:]
        for line in lines:
            I_Gaussian[line[0]] = line[1]
    
    return H_Unweighted, I_Unweighted, H_Gaussian, I_Gaussian

# Returns two lists. One with 200 high H-correlated low I-correlated unweighted stimulus, and the other with the same but Gaussian
def selecting_H_stimuli(H_Unweighted_Scores, I_Unweighted_Scores, H_Gaussian_Scores, I_Gaussian_Scores):
    
    used = set()
    unweighted_Hs = [] # storage for our Unweighted Hs
    gaussian_Hs = [] # storage for our Gaussian Hs

    # Initialize two dictionaries to store the filtered stimuli
    unweighted_filtered = {}
    gaussian_filtered = {}

    # Iterate over the unweighted stimuli and apply the condition (I score < 0.01)
    for stimulus, i_score in I_Unweighted_Scores.items():
        h_score = H_Unweighted_Scores.get(stimulus)  # Get the corresponding H score
        if h_score is not None and abs(float(i_score)) < 0.01:  # Check I score is lower than threshhold
            unweighted_filtered[stimulus] = (h_score, i_score)

    # Iterate over the Gaussian stimuli and apply the condition (I score < 0.01)
    for stimulus, i_score in I_Gaussian_Scores.items():
        h_score = H_Gaussian_Scores.get(stimulus)  # Get the corresponding I score
        if h_score is not None and abs(float(i_score)) < 0.01:  # Check I score is lower than threshhold
            gaussian_filtered[stimulus] = (h_score, i_score)
    
    # Sort the filtered dicts of stimuli by the I score in descending order
    sorted_unweighted = dict(sorted(unweighted_filtered.items(), key=lambda item: float(item[1][0]), reverse=True))
    sorted_gaussian = dict(sorted(gaussian_filtered.items(), key=lambda item: float(item[1][0]), reverse=True))

    assert(len(sorted_unweighted) >= 200 and len(sorted_gaussian) >= 200)
    
    selectingUnweighted = True # setting the category we are selecting for

    # Iterate until we get 200 stimulus in each category
    while len(gaussian_Hs) < 201 or len(unweighted_Hs) < 200:

        if selectingUnweighted and len(unweighted_Hs) < 200:
            for stimulus, _ in sorted_unweighted.items():
                
                # if it has already been selected or its I score is too high, then skip it
                if stimulus in used:
                    continue
                
                # add it to the list of unweighted Hs
                unweighted_Hs.append(stimulus)
                used.add(stimulus)
                lastUnweighted = stimulus
                break
        else:
            for stimulus, scores in sorted_gaussian.items():

                # if it has already been selected or its I score is too high, then skip it
                if stimulus in used:
                    continue

                if len(gaussian_Hs) == 200:
                    print(f'\n\nExample Gaussian H Stimulus\nStimulus Number: {stimulus}\n(h_score, i_score): {scores}')
                    gaussian_Hs.append(stimulus)
                    break
                
                # add it to the list of gaussian Hs
                gaussian_Hs.append(stimulus)
                used.add(stimulus)
                lastGaussian = stimulus
                break

        # flip which weighting scheme (unweighted vs gaussian) we are selecting for
        selectingUnweighted = not selectingUnweighted
    gaussian_Hs = gaussian_Hs[:200]
    print(f'Largest index for unweighted Hs: {list(H_Unweighted_Scores.keys()).index(lastUnweighted)}')
    print(f'Largest index for gaussian Hs: {list(H_Gaussian_Scores.keys()).index(lastGaussian)}')
    print(f'Length of H list (unweighted, gaussian): {len(unweighted_Hs)}, {len(gaussian_Hs)}')
    return unweighted_Hs, gaussian_Hs, used

# Selects the top 100 Is from each list 
def selecting_I_stimuli(H_Unweighted_Scores, I_Unweighted_Scores, H_Gaussian_Scores, I_Gaussian_Scores, used):

    # Lists to store our final stimuli
    unweighted_Is = []
    gaussian_Is = []

    # Initialize two dictionaries to store the filtered stimuli
    unweighted_filtered = {}
    gaussian_filtered = {}

    # Iterate over the unweighted stimuli and apply the condition (H score < 0.01)
    for stimulus, h_score in H_Unweighted_Scores.items():
        i_score = I_Unweighted_Scores.get(stimulus)  # Get the corresponding I score
        if i_score is not None and abs(float(h_score)) < 0.01:  # Only check H score condition
            unweighted_filtered[stimulus] = (h_score, i_score)  # Store both scores for unweighted

    # Iterate over the Gaussian stimuli and apply the condition (H score < 0.01)
    for stimulus, h_score in H_Gaussian_Scores.items():
        i_score = I_Gaussian_Scores.get(stimulus)  # Get the corresponding I score
        if i_score is not None and abs(float(h_score)) < 0.01:  # Only check H score condition
            gaussian_filtered[stimulus] = (h_score, i_score)  # Store both scores for gaussian
    
    # Sort the filtered dicts of stimuli by the I score in descending order
    sorted_unweighted = dict(sorted(unweighted_filtered.items(), key=lambda item: float(item[1][1]), reverse=True))
    sorted_gaussian = dict(sorted(gaussian_filtered.items(), key=lambda item: float(item[1][1]), reverse=True))

    # Ensure there are enough stimuli in each category
    assert(len(sorted_gaussian) >= 100 and len(sorted_unweighted) >= 100)

    selectingUnweighted = True # setting the category we are selecting for

    # Iterate until we get 200 stimulus in each category
    while len(gaussian_Is) < 100 or len(unweighted_Is) < 100:

        if selectingUnweighted:
            for stimulus, _ in sorted_unweighted.items():

                # if it has already been selected or its I score is too high, then skip it
                if stimulus in used:
                    continue
                
                # add it to the list of unweighted Hs
                unweighted_Is.append(stimulus)
                used.add(stimulus)
                lastUnweighted = stimulus
                break
        else:
            for stimulus, _ in sorted_gaussian.items():

                # if it has already been selected or its I score is too high, then skip it
                if stimulus in used:
                    continue
                
                # add it to the list of gaussian Hs
                gaussian_Is.append(stimulus)
                used.add(stimulus)
                lastGaussian = stimulus
                break

        # flip which list we are selecting for
        selectingUnweighted = not selectingUnweighted

    print(f'Largest index for unweighted Vs: {list(I_Unweighted_Scores.keys()).index(lastUnweighted)}')
    print(f'Largest index for gaussian Vs: {list(I_Gaussian_Scores.keys()).index(lastGaussian)}')
    print(f'Length of V lists (unweighted, gaussian): {len(unweighted_Is)}, {len(gaussian_Is)}')
    return unweighted_Is, gaussian_Is, used

# Helper function for subsetting the dictionaries for the uncorrelated stimuli
def filter_uncorrelated_stimuli_by_condition(H_Unweighted_Scores, I_Unweighted_Scores, H_Gaussian_Scores, I_Gaussian_Scores):
    # Initialize two dictionaries to store the filtered stimuli
    unweighted_filtered = {}
    gaussian_filtered = {}

    # Iterate over the unweighted stimuli and apply the condition
    for stimulus, h_score in H_Unweighted_Scores.items():
        i_score = I_Unweighted_Scores.get(stimulus)  # Get the corresponding I score
        if i_score is not None and abs(float(h_score)) < 0.00316 and abs(float(i_score)) < 0.00316:
            unweighted_filtered[stimulus] = (h_score, i_score)  # Store both scores for unweighted

    # Iterate over the Gaussian stimuli and apply the condition
    for stimulus, h_score in H_Gaussian_Scores.items():
        i_score = I_Gaussian_Scores.get(stimulus)  # Get the corresponding I score
        if i_score is not None and abs(float(h_score)) < 0.00316 and abs(float(i_score)) < 0.00316:
            gaussian_filtered[stimulus] = (h_score, i_score)  # Store both scores for gaussian

    # Sort the filtered dicts of stimuli by the sum of the two scores in descending order
    sorted_unweighted = dict(sorted(unweighted_filtered.items(), key=lambda item: abs(float(item[1][0])) + abs(float(item[1][1]))))
    sorted_gaussian = dict(sorted(gaussian_filtered.items(), key=lambda item: abs(float(item[1][0])) + abs(float(item[1][1]))))
    assert(len(sorted_gaussian) >= 100 and len(sorted_unweighted) >= 100)

    return sorted_unweighted, sorted_gaussian

# Selects the top 100 Is from each list 
def selecting_uncorrelated_stimuli(H_Unweighted_Scores, I_Unweighted_Scores, H_Gaussian_Scores, I_Gaussian_Scores, used):

    # sort dicts by absolute value and min sum of values 
    sorted_unweighted, sorted_gaussian = filter_uncorrelated_stimuli_by_condition(H_Unweighted_Scores, I_Unweighted_Scores, H_Gaussian_Scores, I_Gaussian_Scores)

    unweighted_uncorrelated = [] # storage for our Unweighted Is
    gaussian_uncorrelated = [] # storage for our Gaussian Is

    selectingUnweighted = True # setting the category we are selecting for

    # Iterate until we get 200 stimulus in each category
    while len(gaussian_uncorrelated) < 101 or len(unweighted_uncorrelated) < 100:

        if selectingUnweighted and len(unweighted_uncorrelated) < 100:
            for stimulus, _ in sorted_unweighted.items():

                # if it has already been selected or its I score is too high, then skip it
                if stimulus in used:
                    continue
                
                # add it to the list of unweighted Hs
                unweighted_uncorrelated.append(stimulus)
                used.add(stimulus)
                break
        else:
            for stimulus, scores in sorted_gaussian.items():

                # if it has already been selected or its I score is too high, then skip it
                if stimulus in used:
                    continue
                
                if len(gaussian_uncorrelated) == 100:
                    print(f'\n\nExample Uncorrelated Stimulus\nStimulus Number: {stimulus}\n(h_score, i_score): {scores}')
                    gaussian_uncorrelated.append(stimulus)
                    break

                # add it to the list of gaussian Hs
                gaussian_uncorrelated.append(stimulus)
                used.add(stimulus)
                break

        # flip which list we are selecting for
        selectingUnweighted = not selectingUnweighted
    gaussian_uncorrelated = gaussian_uncorrelated[:100]
    print(f'Length of uncorrelated lists (unweighted, gaussian): {len(unweighted_uncorrelated)}, {len(gaussian_uncorrelated)}')
    return unweighted_uncorrelated, gaussian_uncorrelated, used

# Prints statistics about a given set of stimuli
def print_statistics(values, H_scores, I_scores):
    
    H_values = [float(H_scores[stimulus]) for stimulus in values]
    I_values = [float(I_scores[stimulus]) for stimulus in values]

    print("H stats: min={}, max={}, mean={}, std={}".format(np.min(H_values), np.max(H_values), np.mean(H_values), np.std(H_values)))
    print("V stats: min={}, max={}, mean={}, std={}\n".format(np.min(I_values), np.max(I_values), np.mean(I_values), np.std(I_values)))

# This function splits the Hs into two blocks to be paired with either the Is or the uncorrelated
# assuming the list in is descending order of pearson scores, split according to a snake
# thingy (maybe explain later) to help preserve statistical shape of blocks one and two
def snake_split_sorted_stimuli(Hs):
    block_1 = []
    block_2 = []

    # Snake approach: assign the stimuli in "snakes" of 1-2, 1-2, ...
    for idx, stimulus in enumerate(Hs):
        # Determine which block the stimulus goes into based on the snake pattern
        if ((idx + 1) // 2) % 2 == 0:
            block_1.append(stimulus)
        else:
            block_2.append(stimulus)

    return block_1, block_2

# Saves a set of stimuli to the proper directory
def save_batch(stimuli, batch_name):

    # Where we will save the results to
    saveFolder = os.path.join(os.path.dirname(__file__), 'stimuli', batch_name)
    os.makedirs(saveFolder, exist_ok = True)

    # Location of the stimuli directory
    sourceDir = os.path.join(os.path.dirname(__file__), '..', 'arraysAndImages', 'stimuli', 'images')

    # Copy each stimulus in the batch from the source directory to the destination directory
    for stimulus in stimuli:
        sourcePath = os.path.join(sourceDir, f'{(int(stimulus) // 1000) * 1000}', f'{stimulus}.png')
        destinationPath = os.path.join(saveFolder, f'{stimulus}.png')
        shutil.copy(sourcePath, destinationPath)

    return

def main():

    # Load in our results for each scheme as dictionaries
    loadTime = time()
    H_Unweighted_Scores, I_Unweighted_Scores, H_Gaussian_Scores, I_Gaussian_Scores = load_dictionaries()
    print('\nLoaded results into dictionaries %.4f seconds\n'%(time() - loadTime))

    # =========================================================================================
    # Retrieving our different types of stimuli
    # =========================================================================================

    # Gets top 200 Gaussian Hs and top 200 Unweighted Hs
    H_Select_Time = time()
    unweighted_Hs, gaussian_Hs, used = selecting_H_stimuli(H_Unweighted_Scores, I_Unweighted_Scores, H_Gaussian_Scores, I_Gaussian_Scores)
    print('Selected H stimuli: %.4f seconds\n'%(time() - H_Select_Time))

    # Gets the top 100 I stimuli for each category
    I_Select_Time = time()
    unweighted_Is, gaussian_Is, used = selecting_I_stimuli(H_Unweighted_Scores, I_Unweighted_Scores, H_Gaussian_Scores, I_Gaussian_Scores, used)
    print('Selected V stimuli: %.4f seconds\n'%(time() - I_Select_Time))

    # Gets the top 100 uncorrelated stimuli for each category 
    Uncorrelated_Select_Time = time()
    uncorrelated_unweighted, uncorrelated_gaussian, used = selecting_uncorrelated_stimuli(H_Unweighted_Scores, I_Unweighted_Scores, H_Gaussian_Scores, I_Gaussian_Scores, used)
    print('Selected Uncorrelated stimuli: %.4f seconds\n'%(time() - Uncorrelated_Select_Time))
    # =========================================================================================
    # =========================================================================================



    # =========================================================================================
    # Printing Statistics about our various choices
    # =========================================================================================
    # Splitting the unweighted H stimuli into blocks and printing stats
    block_one_unweighted_H, block_two_unweighted_H = snake_split_sorted_stimuli(unweighted_Hs)

    print("Unweighted Uncorrelated Hs Statistics")
    print("===========================")
    print_statistics(block_one_unweighted_H, H_Unweighted_Scores, I_Unweighted_Scores)

    print("Unweighted V-Correlated Hs Statistics")
    print("===========================")
    print_statistics(block_two_unweighted_H, H_Unweighted_Scores, I_Unweighted_Scores)

    # Splitting the gaussian H stimuli into blocks and printing stats
    block_one_gaussian_H, block_two_gaussian_H = snake_split_sorted_stimuli(gaussian_Hs)

    print("Gaussian Uncorrelated Hs Statistics")
    print("===========================")
    print_statistics(block_one_gaussian_H, H_Gaussian_Scores, I_Gaussian_Scores)

    print("Gaussian V-Correlated Hs Statistics")
    print("===========================")
    print_statistics(block_two_gaussian_H, H_Gaussian_Scores, I_Gaussian_Scores)

    # Printing the statistics for the unweighted Is
    print("Unweighted Vs Statistics")
    print("===========================")
    print_statistics(unweighted_Is, H_Unweighted_Scores, I_Unweighted_Scores)

    # Printing the statistics for the gaussian Is
    print("Gaussian Vs Statistics")
    print("===========================")
    print_statistics(gaussian_Is, H_Gaussian_Scores, I_Gaussian_Scores)

    # Printing the statistics for the unweighted uncorrelated stimuli
    print("Unweighted Uncorrelated Statistics")
    print("===========================")
    print_statistics(uncorrelated_unweighted, H_Unweighted_Scores, I_Unweighted_Scores)

    # Printing the statistics for the gaussian Is
    print("Gaussian Uncorrelated Statistics")
    print("===========================")
    print_statistics(uncorrelated_gaussian, H_Gaussian_Scores, I_Gaussian_Scores)
    # =========================================================================================
    # =========================================================================================

    # =========================================================================================
    # Copying stimuli to the final directory
    # =========================================================================================
    
    copySaveTime = time()
    save_batch(block_one_unweighted_H, 'unweightedUncorrelatedH')
    save_batch(block_two_unweighted_H, 'unweightedVCorrelatedH')
    save_batch(block_two_gaussian_H, 'gaussianUncorrelatedH')
    save_batch(block_two_gaussian_H, 'gaussianVCorrelatedH')
    save_batch(unweighted_Is, 'unweightedV')
    save_batch(gaussian_Is, 'gaussianV')
    save_batch(uncorrelated_unweighted, 'unweightedUncorrelated')
    save_batch(uncorrelated_gaussian, 'gaussianUncorrelated')
    save_batch(block_one_unweighted_H + block_two_unweighted_H + unweighted_Is + uncorrelated_unweighted, 'unweighted')
    save_batch(block_one_gaussian_H + block_two_gaussian_H + gaussian_Is + uncorrelated_gaussian, 'gaussian')
    print('Copied and saved all stimuli images: %.4f seconds\n'%(time() - copySaveTime))
    # =========================================================================================
    # =========================================================================================
    
    # final check of no overlaps
    allImages = block_one_gaussian_H + block_two_gaussian_H + gaussian_Is + uncorrelated_gaussian + block_one_unweighted_H + block_two_unweighted_H + unweighted_Is + uncorrelated_unweighted
    assert len(set(allImages)) == len(allImages)
    print('No image overlap confirmed!\n')

    # print final runtime 
    print(f'Total Runtime: {time() - loadTime} seconds\n')



if __name__ == '__main__':
    main()