import pandas as pd
import numpy as np
from scipy.stats import norm
import urllib.request

def doLookupMean(playerid,player_stat):
    try:
        url = 'https://zerscrpt.cfd/omega/nbaData/' + playerid + '.txt'
        urllib.request.urlretrieve(url, playerid+'.csv')
        df = pd.read_csv(playerid+'.csv')
    except FileNotFoundError:
        exit(0)
    
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

    meanReturn = round(means[player_stat],2)
    stdDevReturn = round(stdDev[player_stat],2)
    
    return meanReturn, stdDevReturn

def doLookup(playerid,player_stat,player_target):
    try:
        url = 'https://zerscrpt.cfd/omega/nbaData/' + playerid + '.txt'
        urllib.request.urlretrieve(url, playerid+'.csv')
        df = pd.read_csv(playerid+'.csv')
    except FileNotFoundError:
        exit(0)
    
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

    zScore = (float(player_target) - float(means[primaryData[primaryData.index(str(player_stat))]])) / float(stdDev[primaryData[primaryData.index(str(player_stat))]])

    probOver = 1 - norm.cdf(zScore)
    probUnder = norm.cdf(zScore)

    probOver = round(probOver*100.00,2)
    probUnder = round(probUnder*100.00,2)

    return probOver,probUnder
