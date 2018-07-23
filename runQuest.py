import numpy as np 
from numpy.random import shuffle
from psychopy import visual, data, event, core
from createPatches import createPatches
from giveFeedback import giveFeedback
import copy, time

def runQuest(experimentStructure, stimuliStructure, data, feedbackText, pThreshold, questTrials):
    """ This function implements a Quest procedure to individualize the maximum contrast difference
        
        Currently not in use.
        
        Input:
            exerimentStructure: all general experimental properties 
            stimuliStructure: all general stimulus properties
            data: PsychoPy data functions
            feedbackText: feedback text object instance
            pThreshold: threshold for quest procedure
            questTrials: number of trials for qQest procedure
        
        Return: 
            trials.quantile: quantile of Quest posterior pdf
            accPerf: accumulated performance of current block
    """
    
    # Create some shortnames
    thisExp = experimentStructure['thisExp']
    patch1 = stimuliStructure['patch1']
    patch2 = stimuliStructure['patch2']
    questClock = stimuliStructure['questClock']

    # Create some info to store with the data
    info={}
    info['startPoints']=[0.03,0.04]
    info['nTrials'] = questTrials
    lowerBound = 0.01
    upperBound = 0.05
    
    whichLoop = 'quest'
    
    stairs = []
    for thisStart in info['startPoints']:
    
        # We need a COPY of the info for each staircase 
        # (or the changes here will be made to all the other staircases)
        thisInfo = copy.copy(info)
        # Now add any specific info for this staircase
        thisInfo['thisStart'] = thisStart #we might want to keep track of this
        trials = data.QuestHandler(startVal = thisStart, startValSd=0.1, extraInfo=thisInfo, pThreshold=pThreshold,
        nTrials=questTrials, minVal=lowerBound, maxVal=upperBound, name = 'quest', gamma = 0.5) 
        thisExp.addLoop(trials) 
        stairs.append(trials)
    
    accPerf = 0.0
    for trialN in range(info['nTrials']):
        for trials in stairs:
            thisDifference = trials.next()
            print 'start=%.2f, current=%.4f' %(trials.extraInfo['thisStart'], thisDifference)
            lowerBound = float('NaN')
            upperBound = float('NaN')
            
            positions = np.random.choice([0,1])
            if positions == 1:
                targetPatch = 'left'
            else:
                targetPatch = 'right'
                
            (decision1, trials) = createPatches(experimentStructure, stimuliStructure, questClock, lowerBound, upperBound, targetPatch,
            trials, whichLoop, thisDifference)
            
            if (decision1.keys==None):
            
                msg = 'Zu langsam!' 
                giveFeedback(experimentStructure, stimuliStructure, feedbackText, msg)
            
            if decision1.corr:
                accPerf = accPerf + 1
            
            thisExp.nextEntry()
    
    questQuantiles = []
    for trials in stairs:
        questQuantiles.append(trials.quantile())
        print(questQuantiles)
    
    print(np.mean(questQuantiles))
    return(trials.quantile(), accPerf)
