import pandas as pd
import csv
import os
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.stats import anderson

def perform_anderson_darling_test(data):
    result = anderson(data)
    print('Statistic: %.3f' % result.statistic)
    for i in range(len(result.critical_values)):
        sl, cv = result.significance_level[i], result.critical_values[i]
        if result.statistic < cv:
            print(f"Significance Level: {sl}%, Critical Value: {cv}, Data looks normal (fail to reject H0)")
        else:
            print(f"Significance Level: {sl}%, Critical Value: {cv}, Data does not look normal (reject H0)")

def create_plots(data, folder_name, plot_type, savePath):
    plt.figure(figsize=(10, 6))
    if plot_type == 'histogram':
        plt.hist(data, bins=50, alpha=0.75, color='blue')
        plt.title(f'Histogram of Pearson Scores for {folder_name}')
        plt.xlabel('Pearson r value')
        plt.ylabel('Frequency')
    elif plot_type == 'qq':
        sm.qqplot(data, line='45', fit=True)
        plt.title(f'Q-Q Plot of Pearson Scores for {folder_name}')
    elif plot_type == 'box':
        plt.boxplot(data, vert=False)
        plt.title(f'Box Plot of Pearson Scores for {folder_name}')
        plt.xlabel('Pearson r value')
    plt.savefig(os.path.join(savePath, f'{folder_name}_{plot_type}.png'))
    plt.close()

def main():
    resultsFolder = os.path.join(os.path.dirname(__file__), 'results', 'hiAnalysis', 'results')
    saveFolderUnweighted = os.path.join(os.path.dirname(__file__), 'Howard_Results', 'unweighted')
    saveFolderGaussian= os.path.join(os.path.dirname(__file__), 'Howard_Results', 'gaussian')
    for name in ['H', 'I', 'V', 'S', 'O']:
        os.makedirs(os.path.join(saveFolderUnweighted, name), exist_ok=True)
        os.makedirs(os.path.join(saveFolderGaussian, name), exist_ok=True)
        

    # get all the pearson scores and get general statistics
    header = ['', 'mean', 'std', 'max', 'min', 'range']
    generalStatsUnweighted = []
    generalStatsGaussian = []
    plus_two_std_H_unweighted = None
    plus_two_std_H_gaussian = None
    plus_two_std_I_unweighted = None
    plus_two_std_I_gaussian = None
    plus_two_std_V_unweighted = None
    plus_two_std_V_gaussian = None
    stim_numbers_H_unweighted = None
    stim_numbers_I_unweighted = None
    stim_numbers_V_unweighted = None
    stim_numbers_H_gaussian = None
    stim_numbers_I_gaussian = None
    stim_numbers_V_gaussian = None
    plus_two_std_unweighted_data = []
    plus_two_std_gaussian_data = []
    for folder in os.listdir(resultsFolder):
        
        gaussianPath = os.path.join(resultsFolder, folder, 'anyAll', 'gaussian', 'pearsonScores.csv')
        unweightedPath = os.path.join(resultsFolder, folder, 'anyAll', 'unweighted', 'pearsonScores.csv')
        pearsonScoresUnweighted = pd.read_csv(unweightedPath)
        pearsonScoresGaussian = pd.read_csv(gaussianPath)
        fullPathUnweighted = os.path.join(saveFolderUnweighted, folder)
        fullPathGaussian = os.path.join(saveFolderGaussian, folder)

        # Anderson-Darling test and plots for Unweighted
        print(f"anderson darling test for unweighted {folder}")
        perform_anderson_darling_test(pearsonScoresUnweighted['Pearson r value'])
        create_plots(pearsonScoresUnweighted['Pearson r value'], folder + "_unweighted", 'histogram', fullPathUnweighted)
        create_plots(pearsonScoresUnweighted['Pearson r value'], folder + "_unweighted", 'qq', fullPathUnweighted)
        create_plots(pearsonScoresUnweighted['Pearson r value'], folder + "_unweighted", 'box', fullPathUnweighted)

        # Anderson-Darling test and plots for Gaussian
        print(f"anderson darling test for gaussian {folder}")
        perform_anderson_darling_test(pearsonScoresGaussian['Pearson r value'])
        create_plots(pearsonScoresGaussian['Pearson r value'], folder + "_gaussian", 'histogram', fullPathGaussian)
        create_plots(pearsonScoresGaussian['Pearson r value'], folder + "_gaussian", 'qq', fullPathGaussian)
        create_plots(pearsonScoresGaussian['Pearson r value'], folder + "_gaussian", 'box', fullPathGaussian)

        meanUnweighted = pearsonScoresUnweighted['Pearson r value'].mean()
        stdUnweighted = pearsonScoresUnweighted['Pearson r value'].std()
        maxUnweighted = pearsonScoresUnweighted['Pearson r value'].max()
        minUnweighted = pearsonScoresUnweighted['Pearson r value'].min()
        rangeUnweighted = maxUnweighted - minUnweighted
        dataUnweighted = [folder, meanUnweighted, stdUnweighted, maxUnweighted, minUnweighted, rangeUnweighted]
        generalStatsUnweighted.append(dataUnweighted.copy())

        meanGaussian = pearsonScoresGaussian['Pearson r value'].mean()
        stdGaussian = pearsonScoresGaussian['Pearson r value'].std()
        maxGaussian = pearsonScoresGaussian['Pearson r value'].max()
        minGaussian = pearsonScoresGaussian['Pearson r value'].min()
        rangeGaussian = maxGaussian - minGaussian
        dataGaussian = [folder, meanGaussian, stdGaussian, maxGaussian, minGaussian, rangeGaussian]
        generalStatsGaussian.append(dataGaussian.copy())

        # looking at the set of things with +2std above mean
        threshold_unweighted = 2 * stdUnweighted
        threshold_gaussian = 2 * stdGaussian
        if folder == 'H':
            plus_two_std_H_unweighted = pearsonScoresUnweighted[pearsonScoresUnweighted['Pearson r value'] > threshold_unweighted]
            plus_two_std_H_gaussian = pearsonScoresGaussian[pearsonScoresGaussian['Pearson r value'] > threshold_gaussian]
            
            
            meanUnweighted = plus_two_std_H_unweighted['Pearson r value'].mean()
            stdUnweighted = plus_two_std_H_unweighted['Pearson r value'].std()
            maxUnweighted = plus_two_std_H_unweighted['Pearson r value'].max()
            minUnweighted = plus_two_std_H_unweighted['Pearson r value'].min()
            rangeUnweighted = maxUnweighted - minUnweighted
            
            meanGaussian = plus_two_std_H_gaussian['Pearson r value'].mean()
            stdGaussian = plus_two_std_H_gaussian['Pearson r value'].std()
            maxGaussian = plus_two_std_H_gaussian['Pearson r value'].max()
            minGaussian = plus_two_std_H_gaussian['Pearson r value'].min()
            rangeGaussian = maxGaussian - minGaussian


            plus_two_std_unweighted_data.append(['H', meanUnweighted, stdUnweighted, maxUnweighted, minUnweighted, rangeUnweighted, len(plus_two_std_H_unweighted)])
            plus_two_std_gaussian_data.append(['H', meanGaussian, stdGaussian, maxGaussian, minGaussian, rangeGaussian, len(plus_two_std_H_gaussian)])

            stim_numbers_H_unweighted = plus_two_std_H_unweighted['Stimulus Number'].tolist().copy()
            stim_numbers_H_gaussian = plus_two_std_H_gaussian['Stimulus Number'].tolist().copy()

        if folder == 'I':
            plus_two_std_I_unweighted = pearsonScoresUnweighted[pearsonScoresUnweighted['Pearson r value'] > threshold_unweighted]
            plus_two_std_I_gaussian = pearsonScoresGaussian[pearsonScoresGaussian['Pearson r value'] > threshold_gaussian]


            meanUnweighted = plus_two_std_I_unweighted['Pearson r value'].mean()
            stdUnweighted = plus_two_std_I_unweighted['Pearson r value'].std()
            maxUnweighted = plus_two_std_I_unweighted['Pearson r value'].max()
            minUnweighted = plus_two_std_I_unweighted['Pearson r value'].min()
            rangeUnweighted = maxUnweighted - minUnweighted
            
            meanGaussian = plus_two_std_I_gaussian['Pearson r value'].mean()
            stdGaussian = plus_two_std_I_gaussian['Pearson r value'].std()
            maxGaussian = plus_two_std_I_gaussian['Pearson r value'].max()
            minGaussian = plus_two_std_I_gaussian['Pearson r value'].min()
            rangeGaussian = maxGaussian - minGaussian

            plus_two_std_unweighted_data.append(['I', meanUnweighted, stdUnweighted, maxUnweighted, minUnweighted, rangeUnweighted, len(plus_two_std_I_unweighted)])
            plus_two_std_gaussian_data.append(['I', meanGaussian, stdGaussian, maxGaussian, minGaussian, rangeGaussian, len(plus_two_std_I_gaussian)])

            stim_numbers_I_unweighted = plus_two_std_I_unweighted['Stimulus Number'].tolist().copy()
            stim_numbers_I_gaussian = plus_two_std_I_gaussian['Stimulus Number'].tolist().copy()
        
        if folder == 'V':
            plus_two_std_V_unweighted = pearsonScoresUnweighted[pearsonScoresUnweighted['Pearson r value'] > threshold_unweighted]
            plus_two_std_V_gaussian = pearsonScoresGaussian[pearsonScoresGaussian['Pearson r value'] > threshold_gaussian]

            meanUnweighted = plus_two_std_V_unweighted['Pearson r value'].mean()
            stdUnweighted = plus_two_std_V_unweighted['Pearson r value'].std()
            maxUnweighted = plus_two_std_V_unweighted['Pearson r value'].max()
            minUnweighted = plus_two_std_V_unweighted['Pearson r value'].min()
            rangeUnweighted = maxUnweighted - minUnweighted
            
            meanGaussian = plus_two_std_V_gaussian['Pearson r value'].mean()
            stdGaussian = plus_two_std_V_gaussian['Pearson r value'].std()
            maxGaussian = plus_two_std_V_gaussian['Pearson r value'].max()
            minGaussian = plus_two_std_V_gaussian['Pearson r value'].min()
            rangeGaussian = maxGaussian - minGaussian

            plus_two_std_unweighted_data.append(['V', meanUnweighted, stdUnweighted, maxUnweighted, minUnweighted, rangeUnweighted, len(plus_two_std_V_unweighted)])
            plus_two_std_gaussian_data.append(['V', meanGaussian, stdGaussian, maxGaussian, minGaussian, rangeGaussian, len(plus_two_std_V_gaussian)]) 

            stim_numbers_V_unweighted = plus_two_std_V_unweighted['Stimulus Number'].tolist().copy()
            stim_numbers_V_gaussian = plus_two_std_V_gaussian['Stimulus Number'].tolist().copy()


    with open(os.path.join(saveFolderUnweighted, 'general_statistics.csv'), mode = 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for line in generalStatsUnweighted:
            writer.writerow(line)

    with open(os.path.join(saveFolderGaussian, 'general_statistics.csv'), mode = 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for line in generalStatsGaussian:
            writer.writerow(line) 
    
    with open(os.path.join(saveFolderUnweighted, 'plus_two_std_statistics.csv'), mode = 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(header + ['n'])
        for line in  plus_two_std_unweighted_data:
            writer.writerow(line)

    with open(os.path.join(saveFolderGaussian, 'plus_two_std_statistics.csv'), mode = 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(header + ['n'])
        for line in plus_two_std_gaussian_data:
            writer.writerow(line) 
    
    with open(os.path.join(saveFolderUnweighted, 'overlaps_2_std.csv'), mode = 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(['H_I_overlaps', 'H_V_overlaps', 'I_V overlaps', 'H_I_V_overlaps'])
        data = [len(set(stim_numbers_H_unweighted).intersection(stim_numbers_I_unweighted)), 
                len(set(stim_numbers_H_unweighted).intersection(stim_numbers_V_unweighted)),
                len(set(stim_numbers_I_unweighted).intersection(stim_numbers_V_unweighted)),
                len(set(stim_numbers_H_unweighted).intersection(stim_numbers_I_unweighted).intersection(stim_numbers_V_unweighted))]
        #data = [len(stim_numbers_H_unweighted) + len(stim_numbers_I_unweighted) - len(set(stim_numbers_H_unweighted + stim_numbers_I_unweighted)), len(stim_numbers_H_unweighted) + len(stim_numbers_V_unweighted) - len(set(stim_numbers_H_unweighted + stim_numbers_V_unweighted)),len(stim_numbers_I_unweighted) + len(stim_numbers_V_unweighted) -  len(set(stim_numbers_I_unweighted + stim_numbers_V_unweighted))]
        writer.writerow(data)

    with open(os.path.join(saveFolderUnweighted, 'overlaps_top1000.csv'), mode = 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(['H_I_overlaps', 'H_V_overlaps', 'I_V overlaps', 'H_I_V_overlaps'])
        data = [len(set(stim_numbers_H_unweighted[:1000]).intersection(stim_numbers_I_unweighted[:1000])), 
                len(set(stim_numbers_H_unweighted[:1000]).intersection(stim_numbers_V_unweighted[:1000])),
                len(set(stim_numbers_I_unweighted[:1000]).intersection(stim_numbers_V_unweighted[:1000])),
                len(set(stim_numbers_H_unweighted[:1000]).intersection(stim_numbers_I_unweighted[:1000]).intersection(stim_numbers_V_unweighted[:1000]))]
        #data = [len(stim_numbers_H_unweighted) + len(stim_numbers_I_unweighted) - len(set(stim_numbers_H_unweighted + stim_numbers_I_unweighted)), len(stim_numbers_H_unweighted) + len(stim_numbers_V_unweighted) - len(set(stim_numbers_H_unweighted + stim_numbers_V_unweighted)),len(stim_numbers_I_unweighted) + len(stim_numbers_V_unweighted) -  len(set(stim_numbers_I_unweighted + stim_numbers_V_unweighted))]
        writer.writerow(data)

    with open(os.path.join(saveFolderGaussian, 'overlaps_2_std.csv'), mode = 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(['H_I_overlaps', 'H_V_overlaps', 'I_V overlaps', 'H_I_V_overlaps'])
        data = [len(set(stim_numbers_H_gaussian).intersection(stim_numbers_I_gaussian)), 
                len(set(stim_numbers_H_gaussian).intersection(stim_numbers_V_gaussian)),
                len(set(stim_numbers_I_gaussian).intersection(stim_numbers_V_gaussian)),
                len(set(stim_numbers_H_gaussian).intersection(stim_numbers_I_gaussian).intersection(stim_numbers_V_gaussian))]
        # data = [len(stim_numbers_H_gaussian) + len(stim_numbers_I_gaussian) - len(set(stim_numbers_H_gaussian + stim_numbers_I_gaussian)), len(stim_numbers_H_gaussian) + len(stim_numbers_V_gaussian) - len(set(stim_numbers_H_gaussian + stim_numbers_V_gaussian)),len(stim_numbers_I_gaussian) + len(stim_numbers_V_gaussian) - len(set(stim_numbers_I_gaussian + stim_numbers_V_gaussian))]
        writer.writerow(data)

    with open(os.path.join(saveFolderGaussian, 'overlaps_top1000.csv'), mode = 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(['H_I_overlaps', 'H_V_overlaps', 'I_V overlaps', 'H_I_V_overlaps'])
        data = [len(set(stim_numbers_H_gaussian[:1000]).intersection(stim_numbers_I_gaussian[:1000])), 
                len(set(stim_numbers_H_gaussian[:1000]).intersection(stim_numbers_V_gaussian[:1000])),
                len(set(stim_numbers_I_gaussian[:1000]).intersection(stim_numbers_V_gaussian[:1000])),
                len(set(stim_numbers_H_gaussian[:1000]).intersection(stim_numbers_I_gaussian[:1000]).intersection(stim_numbers_V_gaussian[:1000]))]
        # data = [len(stim_numbers_H_gaussian) + len(stim_numbers_I_gaussian) - len(set(stim_numbers_H_gaussian + stim_numbers_I_gaussian)), len(stim_numbers_H_gaussian) + len(stim_numbers_V_gaussian) - len(set(stim_numbers_H_gaussian + stim_numbers_V_gaussian)),len(stim_numbers_I_gaussian) + len(stim_numbers_V_gaussian) - len(set(stim_numbers_I_gaussian + stim_numbers_V_gaussian))]
        writer.writerow(data)
 
    

  


    
    
        




if __name__ == '__main__':
    main()