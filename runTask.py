from numpy.random import random, shuffle
import numpy as np
from numpy import average
from createPatches import createPatches
from createFractals import createFractals
from psychopy import core
from simpleInstructions import simpleInstructions
from giveFeedback import giveFeedback
import re

def runTask(experimentStructure, outcomeStructure, stimuliStructure, data,
feedbackText, nTrials, whichLoop, blockIndex, blockNumber, conditionName, globalClock, tracker):
    """ This function runs a single block of the Gabor-bandit task
    
    Here we loop over trials and check if the current participant missed trials.
    If trials were missed, we repeat these trials at the end of the block.
    
    Input:
        experimentStructure: all general experimental properties 
        outcomeStructure: all general outcome properties 
        stimuliStructure: all general stimulus properties
        data: PsychoPy data functions
        feedbackText: feedback text object instance
        nTrials: number of trials
        whichLoop: indicates required task phase
        blockIndex: path to pre-generated block
        blockNumber: indicates current block number
        conditionName: name of current condition
        globalClock: clock to control timing during fMRI
        tracker: eye-tracker object instance
        
    Return: 
        accPerf: accumulated performance of current block
        win: window object instance
    """
    
    # Create some shortnames
    expInfo         = experimentStructure['expInfo']
    thisExp         = experimentStructure['thisExp']
    patchClock      = stimuliStructure['patchClock']
    win             = experimentStructure['win']
    useEyeTracker   = experimentStructure['useEyeTracker']
    win.setRecordFrameIntervals(True)
    
    # Set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler(nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=None,
        trialList=data.importConditions(blockIndex),
        seed=None, name = conditionName) 
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    
    # Abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)
    
    myCount         = 0 # counter for total number of completed trials (if missed trials exist, can be larger than nTrials)
    missCounter     = 0 # counter for number of misses
    misses          = list() # temporarily saves information about trials that have been missed to repeat these trials
    routineTimer    = core.CountdownTimer()
    currentMiss     = float('nan') # actual trial that has to be repeated next
    
    while True: 
        
        missIndex = 0
        try:
            thisTrial = trials.next()
        except StopIteration:  # we got a StopIteration error
            currentMiss = misses[0]
            thisTrial = trials.trialList[currentMiss] 
        
        currentLoop = trials
        
        # Abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial.keys():
                exec(paramName + '= thisTrial.' + paramName)
        
        # First state (Gabor-patches)
        thisDifference = float('nan')
        (decision1, trials, routineTimer, globalClock, decision1.timestamp, fixCrossTiming, saccadeMiss) = createPatches(experimentStructure,
        stimuliStructure, patchClock, targetPatch, trials, whichLoop, thisDifference, PU, routineTimer, globalClock, tracker)
        
        if (decision1.keys==None):
            if saccadeMiss == 1:
                msg = 'Augenbewegung!'
            elif saccadeMiss == 0:
                msg = 'Zu langsam!' 
            
            # Feedback, if required
            (routineTimer, globalClock, feedbackTimestamp, fixCrossTiming_feedback) = giveFeedback(experimentStructure,
            stimuliStructure, feedbackText, msg, routineTimer, globalClock, 1)
            trials.addData('decision1.rt', float('nan'))
            trials.addData('decision2.rt', float('nan'))
            trials.addData('decision2.keys', float('nan'))
            trials.addData('decision2.corr', float('nan'))
            trials.addData('decision2.color', float('nan'))
            trials.addData('decision2.reward', 0)
            accPerf = trials.data['decision2.reward'].sum()
            trials.addData('decision2.accPerf', accPerf)
            
            # Triggers for fMRI
            trials.addData('decision1.trigger_1', decision1.timestamp)                          # decision1 fixation cross onset
            trials.addData('decision1.trigger_2', (decision1.timestamp + fixCrossTiming))       # decision1 patches onset
            trials.addData('decision2.trigger_1', float('nan'))                                 # decision2 fixation cross onset
            trials.addData('decision2.trigger_2', float('nan'))                                 # decision2 fractals onset
            trials.addData('feedback.trigger_1', feedbackTimestamp)                             # feedback fixation cross onset
            trials.addData('feedback.trigger_2', (feedbackTimestamp + fixCrossTiming_feedback)) # feedback reward onset
            
            # Check if trial was missed
            if (myCount < nTrials):
                misses.append(myCount)
                missCounter = missCounter + 1
                missIndex = 1

        elif (decision1.keys!=None):
            
            # Record reaction time for perceptual decision
            trials.addData('decision1.rt', decision1.rt)
            
            # Second stage (fractals)
            (decision2, trials, misses, missCounter, routineTimer, globalClock, decision2.timestamp, fixCrossTiming, feedbackTimestamp,
            fixCrossTiming_feedback, missIndex) = createFractals(experimentStructure, outcomeStructure, stimuliStructure, redFractal, 
            targetPatch, corrAns, trials, outcomes, feedbackText, misses, missCounter, myCount, routineTimer, globalClock, nTrials)
            
            # Triggers for fMRI
            trials.addData('decision1.trigger_1', decision1.timestamp)                          # decision1 fixation cross onset
            trials.addData('decision1.trigger_2', (decision1.timestamp + fixCrossTiming))       # decision1 patches onset
            trials.addData('decision2.trigger_1', decision2.timestamp)                          # decision2 fixation cross onset
            trials.addData('decision2.trigger_2', (decision2.timestamp + fixCrossTiming))       # decision2 fractals onset
            trials.addData('feedback.trigger_1', feedbackTimestamp)                             # feedback fixation cross onset
            trials.addData('feedback.trigger_2', feedbackTimestamp + fixCrossTiming_feedback)   # feedback reward onset
            
            # Delete miss that has been repeated
            if (decision2.keys!=None) and myCount >= nTrials and len(misses) > 0:
                misses.pop(0)
        
        # Record data
        trials.addData('whichLoop', whichLoop)
        trials.addData('block', blockIndex)
        trials.addData('blockNumber', blockNumber)
        trials.addData('eyeTracker', useEyeTracker)
        trials.addData('missIndex', missIndex)
        trials.addData('misses', missCounter)
        trials.addData('currentMiss', currentMiss)
        thisExp.nextEntry()
        
        # Update counter
        myCount = myCount + 1
        
        # Check if more we have to repeat any misses
        if (myCount) >= nTrials and len(misses)==0:
            break
    
    # Block performance 
    if 'decision2' in locals():
        accPerf = trials.data['decision1.reward'].sum() + trials.data['decision2.reward'].sum()
    else:
        accPerf = trials.data['decision1.reward'].sum()
        
    win.setRecordFrameIntervals(False)    
    
    return(accPerf, win)