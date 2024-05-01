import pandas as pd
import numpy as np
from scipy.stats import norm

while True:

    while True:
        try:
            file = input('Enter target file: ')
            df = pd.read_csv('scraping/output/'+file+'.csv')
            break
        except FileNotFoundError:
            print(f'\'{file}.csv\' not found, please try again\n\n')
    
    
    primaryData = [
        '3p',
        'ft',
        'trb',
        'ast',
        'stl',
        'blk',
        'tov',
        'pts'
    ]

    secondaryData = {
        'ast+trb': ['ast', 'trb'],
        'pts+ast': ['pts', 'ast'],
        'pts+trb': ['pts', 'trb'],
        'pts+trb+ast': ['pts', 'trb', 'ast']
    }

    newDF = df.reindex(columns=primaryData)

    stdDev = {}
    means = {}

    for i in newDF.columns:
        newDF[i] = pd.to_numeric(newDF[i], errors='coerce')
        stdDev[i] = np.nanstd(newDF[i])
        means[i] = np.nanmean(newDF[i])
    
    targetPoints = {}
    print('Select from the list below or type `ALL` for all stats\n')
    tempZ = 0
    for i in primaryData:
        tempZ = tempZ + 1
        print(f'{tempZ}. {i}')

    choice = input('> ')

    if choice.lower() == 'all':
        tempX = 0
        for i in newDF.columns:
            tempX = tempX + 1
            target = float(input(f'Enter target value for {i}, or type `NA`: '))
            targetPoints[i] = target
        
        for k,v in secondaryData.items():
            tempX = tempX + 1
            target = float(input(f'Enter target value for {k}, or type `NA`: '))
            targetPoints[k] = target

        probs = {}
        for i in newDF.columns:
            zScore = (targetPoints[i] - means[i]) / stdDev[i]
            probOver = 1 - norm.cdf(zScore)
            probUnder = norm.cdf(zScore)

            probs[i] = {'over': probOver, 'under': probUnder}
        
        for i, k in secondaryData.items():
            if i not in targetPoints:
                continue
            combinedCol = newDF[k].sum(axis=1)
            combinedMean = np.mean(combinedCol)
            combinedStdDev = np.std(combinedCol)

            zScores = []
            for h in k:
                zScoreLocal = (targetPoints[i] - means[h]) / stdDev[h]
                zScores.append(zScoreLocal)
            
            zScoreCombined = (targetPoints[i] - combinedMean) / combinedStdDev
            probOver = 1 - norm.cdf(zScoreCombined)
            probUnder = norm.cdf(zScoreCombined)

            probs[i] = {'over': probOver, 'under': probUnder}

        for i in newDF.columns:
            over = probs[i]['over']
            under = probs[i]['under']

            print(f'{i}: \n')
            print(f'Over {str(targetPoints[i])}: {str(round(over*100.00,2))}%')
            print(f'Under {str(targetPoints[i])}: {str(round(under*100.00,2))}%\n======')

        for i,j in secondaryData.items():
            over = probs[i]['over']
            under = probs[i]['under']

            print(f'{i}: \n')
            print(f'Over {str(targetPoints[i])}: {str(round(over*100.00,2))}%')
            print(f'Under {str(targetPoints[i])}: {str(round(under*100.00,2))}%\n======')

        bestOver = max(probs.items(), key=lambda x: x[1]['over'])
        bestUnder = max(probs.items(), key=lambda x: x[1]['under'])

        bestO = round(bestOver[1]['over']*100.00,2)
        bestU = round(bestUnder[1]['under']*100.00,2)

        print(f'Best over: {bestOver[0]} with {str(bestO)}')
        print(f'Best under: {bestUnder[0]} with {str(bestU)}')
    else:
        target = float(input(f"Enter target value for {primaryData[int(choice)-1]}: "))

        probs = {}
        zScore = (target - means[primaryData[int(choice)-1]]) / stdDev[primaryData[int(choice)-1]]
        probOver = 1 - norm.cdf(zScore)
        probUnder = norm.cdf(zScore)

        print(f'\nOver {str(target)}: {str(round(probOver * 100.00,2))}%')
        print(f'Under {str(target)}: {str(round(probUnder * 100.00,2))}%')

    print('Press `q` to quit, otherwise press any key to resume...\n')
    exitChoice = input('> ')
    if exitChoice.lower() == 'q': break