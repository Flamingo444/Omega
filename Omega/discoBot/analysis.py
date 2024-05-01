import pandas as pd
import numpy as np
import math
from scipy.stats import norm

#Looping the script
while True:

    while True:
        try:
            #Choose file to interact with
            filename = input("Enter the name of the target csv file:")
            df = pd.read_csv(filename +'.csv')
            break
        except FileNotFoundError:
            print(f"File '{filename}.csv' not found. Please try again.")

    #get the data columns needed for base analysis
    data_cols = [
        '3p',
        'ft',
        'trb',
        'ast',
        'stl',
        'blk',
        'tov',
        'pts'
    ]

    #update the columns needed
    new_df = df.reindex(columns=data_cols)

    #calculate the SD and Mean of dataset
    std_devs = {}
    means = {}
    for col in new_df.columns:
        #convert non-numeric values to NaN
        new_df[col] = pd.to_numeric(new_df[col], errors='coerce')
        std_devs[col] = np.nanstd(new_df[col])
        means[col] = np.nanmean(new_df[col])

    #get the user's target input for each column
    targets = {}
    print("Select from the list below or type `ALL` for all stats\n")
    tempX = 0
    for i in data_cols:
        tempX = tempX + 1
        print(f"{tempX}. {i}")

    mainChoice = input("\n-----\n> ")

    if mainChoice.lower() == "all":
        for col in new_df.columns:
            target = float(input(f"Enter target value for {col}: "))
            targets[col] = target

        #Additional columns for specified data
        additional_cols = {
            'ast+trb': ['ast', 'trb'],
            'pts+ast': ['pts', 'ast'],
            'pts+trb': ['pts', 'trb'],
            'pts+trb+ast': ['pts', 'trb', 'ast']
        }
        #asks user what their target goal data is
        for k, v in additional_cols.items():
            target_1 = float(input(f"Enter target value for {k}:"))
            targets[k] = target_1

        #Calculate the over and under probabilities using normal distribution
        probs = {}
        for col in new_df.columns:
            z_score_over = (targets[col] - means[col]) / std_devs[col]
            prob_over = 1 - norm.cdf(z_score_over)

            z_score_under = (targets[col] - means[col]) / std_devs[col]
            prob_under = norm.cdf(z_score_under)

            probs[col] = {'over': prob_over, 'under': prob_under}
            
        #calculate the over and under probabilities using normal distribution
        for k, v in additional_cols.items():
            if k not in targets:
                continue
            combined_col = new_df[v].sum(axis=1)
            combined_mean = np.mean(combined_col)
            combined_std_dev = np.std(combined_col)

            z_scores_over = []
            z_scores_under = []
            for col in v:
                z_score = (targets[k] - means[col]) / std_devs[col]
                z_scores_over.append(z_score)
                z_scores_under.append(z_score)

            z_score_combined = (targets[k] - combined_mean) / combined_std_dev
            prob_over = (1 - norm.cdf(z_score_combined)) * 100
            prob_under = (norm.cdf(z_score_combined)) * 100
            print(f"Probabilities for {k}:\nOver: {prob_over:.2f}%\nUnder: {prob_under:.2f}%\n")
            probs[k] = {'over': prob_over / 100, 'under': prob_under / 100}


        #print final probabilities
        for col in new_df.columns:
            over = probs[col]['over']
            under = probs[col]['under']
            print(f"{col}:")
            print("Probability of hitting over " + str(targets[col]) + ": " + str(round(over * 100.00,2)) + "%")
            print("Probability of hitting under " + str(targets[col]) + ": " + str(round(under * 100.00,2)) + "%\n")
            
        for k, v  in additional_cols.items():
            over = probs[k]['over']
            under = probs[k]['under']
            print(f"{k}:")
            print("Probability of hitting over " + str(targets[k]) + ": " + str(round(over * 100.00,2)) + "%")
            print("Probability of hitting under " + str(targets[k]) + ": " + str(round(under * 100.00,2)) + "%\n")

        #print the best over and under picks
        best_prob = max(probs.items(), key=lambda x: x[1]['over'])
        print(f"The best over probability is {str(round(best_prob[1]['over']*100.00,2))}% for column {best_prob[0]}")
        best_prob2 = max(probs.items(), key=lambda x: x[1]['under'])
        print(f"The best under probability is {str(round(best_prob2[1]['under']*100.00,2))}% for column {best_prob2[0]}")
    
    else:
        target = float(input(f"Enter target value for {data_cols[int(mainChoice)-1]}: "))

        probs = {}
        z_score_over = (target - means[data_cols[int(mainChoice)-1]]) / std_devs[data_cols[int(mainChoice)-1]]
        prob_over = 1 - norm.cdf(z_score_over)

        z_score_under = (target - means[data_cols[int(mainChoice)-1]]) / std_devs[data_cols[int(mainChoice)-1]]
        prob_under = norm.cdf(z_score_under)


        print("\nProbability of hitting over " + str(target) + ": " + str(round(prob_over * 100.00,2)) + "%")
        print("Probability of hitting under " + str(target) + ": " + str(round(prob_under * 100.00,2)) + "%\n")

# check if the user wants to stop the program
    stop_program = input("Enter 'q' to quit, or press any other key to continue: ")
    if stop_program.lower() == "q":
        break