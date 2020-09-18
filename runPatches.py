from numpy.random import random
import numpy as np
from numpy import average
from createPatches import createPatches
from psychopy import core
from giveFeedback import giveFeedback

def runPatches(experimentStructure, stimuliStructure, data, feedbackText, patchClock, whichLoop,
conditionName, showFeedback, nTrialsPatches, blockIndex, globalClock, eyeTracker=0):
    """ This function manages the first stage of the Gabor-bandit task (Gabor-patches)
    
    Input:
        experimentStructure: all general experimental properties 
        stimuliStructure: all general stimulus properties
        data: PsychoPy data functions
        feedbackText: feedback text object instance
        patchClock: clock object instance for patch timing
        whichLoop: indicates required task phase 
        conditionName: name of current condition
        showFeedback: indicate if feedback should be displayed
        nTrialsPatches: number of trials
        blockIndex: indicates current block number
        globalClock: clock to control timing during fMRI
        eyeTracker: eye-tracker object instance
        
    Return:
        accPerf: accumulated performance of current block
    """

    # Create some shortnames
    expInfo = experimentStructure['expInfo']
    thisExp = experimentStructure['thisExp']
    
    # Store indexed trials for summary
    trialIndexes = 0 
    
    # Set up handler to look after randomisation of conditions etc.
    trials = data.TrialHandler(nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=None,
        trialList=data.importConditions(blockIndex),
        seed=None, name=conditionName)
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    
    # Abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)
    
    # Loop over trials
    routineTimer = core.CountdownTimer()
    myCount = 0 
    for thisTrial in trials:
        currentLoop = trials
        if thisTrial != None:
            for paramName in thisTrial.keys():
                exec(paramName + '= thisTrial.' + paramName)
        
        if whichLoop == 'patches':
            thisDifference = float('nan')
            
        # First stage of the task
        (decision1, trials, routineTimer, globalClock, decision1.timestamp, fixCrossTiming, saccadeMiss) = createPatches(experimentStructure, stimuliStructure, patchClock, targetPatch,
        trials, whichLoop, thisDifference, PU,routineTimer, globalClock, eyeTracker)
        
        # Check if response was made
        if (decision1.keys==None):
            msg = 'Zu langsam!' 
            giveFeedback(experimentStructure, stimuliStructure, feedbackText, msg, routineTimer, globalClock,1)
        
        # Check if response was correct
        elif (decision1.keys!=None):
            
            if showFeedback == 1:
                if decision1.corr == 1:
                    msg = 'richtig' 
                elif decision1.corr == 0:
                    msg = 'falsch'
                giveFeedback(experimentStructure, stimuliStructure, feedbackText, msg, routineTimer, globalClock,0)
            
            # Record reaction time
            trials.addData('decision1.rt', decision1.rt)
        
        # Record additional data
        trials.addData('whichLoop', whichLoop)
        trials.addData('block', blockIndex)
        accPerf = trials.data['decision1.corr'].sum()

        # Indicate that trial is over
        thisExp.nextEntry()
        myCount = myCount + 1
        if myCount == nTrialsPatches :
            trials.finished = True
        
    return(accPerf)