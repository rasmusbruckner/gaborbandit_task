from numpy.random import random, shuffle
import numpy as np
from numpy import average
from createPatches import createPatches
from createFractals import createFractals
from psychopy import core
from simpleInstructions import simpleInstructions
from giveFeedback import giveFeedback
import re
import pylink

def runTask(experimentStructure, outcomeStructure, stimuliStructure, data,
feedbackText, nTrials, whichLoop, blockIndex, blockNumber, conditionName, globalClock, eyeTracker):
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
    expInfo = experimentStructure['expInfo']
    session = expInfo['session']
    thisExp = experimentStructure['thisExp']
    patchClock = stimuliStructure['patchClock']
    win = experimentStructure['win']
    useEyeTracker = experimentStructure['useEyeTracker']
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
    
    myCount = 0  # counter for total number of completed trials (if missed trials exist, can be larger than nTrials)
    missCounter = 0  # counter for number of misses
    misses = list()  # temporarily saves information about trials that have been missed to repeat these trials
    routineTimer = core.CountdownTimer()
    currentMiss = float('nan')  # actual trial that has to be repeated next
    currentPerf = 0
    accPerf = 0
    
    # Cycle over trials
    # -----------------
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
                
        if useEyeTracker:
        
            # Flush cached button presses (eyelink) 
            #eyeTracker.flushKeybuttons(0)
            #eyeTracker.setOfflineMode()
            #pylink.msecDelay(50)
            
            # Log trial onset message
            eyeTracker.sendCommand("record_status_message 'Trial %d %s'"%(myCount, "main_unc"))
            eyeTracker.sendMessage("TRIALID %d %s"%(myCount, "main_unc"))
            
            # Start recording
            eyeTracker.startRecording(1, 1, 1, 1)
        
        # First state (Gabor-patches) initialize contrast difference
        thisDifference = float('nan')
        
        # Deterimine opacity
        if session == 4:
            meanOpacity = np.float(opacity)
        else:
            meanOpacity = 0.5
        
        (decision1, trials, routineTimer, globalClock, decision1.timestamp, fixCrossTiming_patch, saccadeMiss) = createPatches(experimentStructure,
        stimuliStructure, patchClock, targetPatch, trials, whichLoop, thisDifference, PU, routineTimer, globalClock, eyeTracker, meanOpacity)
        
        if (decision1.keys==None) or session == 4:
            
            # Message if participant was too slow
            msg = 'Zu langsam!'
            
            # Feedback, if required
            if not session == 4:
                (routineTimer, globalClock, fb_ts_start, fb_ts_fb) = giveFeedback(experimentStructure,
                stimuliStructure, feedbackText, msg, routineTimer, globalClock, 1, eyeTracker)
            trials.addData('decision1.rt', float('nan'))
            trials.addData('decision2.rt', float('nan'))
            trials.addData('decision2.keys', float('nan'))
            trials.addData('decision2.corr', float('nan'))
            trials.addData('decision2.color', float('nan'))
            trials.addData('decision2.reward', 0)
            # accPerf = trials.data['decision2.reward'].sum()
            trials.addData('decision2.accPerf', accPerf)
            
            # Add the triggers
            trials.addData('decision1.ts_start', decision1.ts_start)  # decision1 fixation cross onset
            trials.addData('decision1.ts_patch', decision1.ts_patch)  # decision1 patches onset
            trials.addData('decision1.ts_resp', float('nan'))  # decision1 response
            trials.addData('decision2.ts_start', float('nan'))  # decision2 fixation cross onset
            trials.addData('decision2.ts_fractal', float('nan'))  # decision2 fractals onset
            trials.addData('decision2.ts_resp', float('nan'))  # decision2 response
            if not session == 4:
                trials.addData('feedback.ts_start', fb_ts_start) # feedback fixation cross onset
                trials.addData('feedback.ts_feedback', fb_ts_fb)  # feedback reward onset
            else: 
                trials.addData('feedback.ts_start', float('nan'))  # feedback fixation cross onset
                trials.addData('feedback.ts_feedback', float('nan'))  # feedback reward onset
            
            # Record trial duration
            duration = globalClock.getTime()-decision1.ts_start
            
            # Check if trial was missed and record this
            if (myCount < nTrials) and not session == 4:
                misses.append(myCount)
                missCounter = missCounter + 1
                missIndex = 1
                print(len(misses))
        else:
            # If we have a non-fixation trial, treat it the same as miss trial, but still show fractals to reduce distraction
            #if (myCount < nTrials):
            #    misses.append(myCount)
            #    missCounter = missCounter + 1
            #    missIndex = 1
            
            # Record reaction time for perceptual decision
            trials.addData('decision1.rt', decision1.rt)
            
            # Second stage (fractals)
            (decision2, trials, misses, missCounter, accPerf, routineTimer, globalClock, decision2.timestamp, fixCrossTiming_fractal, fb_ts_start,
            fb_ts_fb, missIndex) = createFractals(experimentStructure, outcomeStructure, stimuliStructure, redFractal, 
            targetPatch, corrAns, trials, outcomes, feedbackText, misses, missCounter, myCount, routineTimer, globalClock, nTrials, accPerf, eyeTracker)
            
            # Record current performance
            #currentPerf = accPerf
            
            # Compute additional triggers for fMRI
            d1_ts_resp = decision1.ts_patch + decision1.rt
            d2_ts_fractal = decision2.ts_start + fixCrossTiming_fractal
            d2_ts_resp = decision2.ts_fractal + decision2.rt 
            
            # Add the triggers
            trials.addData('decision1.ts_start', decision1.ts_start) #  decision1 fixation cross onset
            trials.addData('decision1.ts_patch', decision1.ts_patch) #  decision1 patches onset
            trials.addData('decision1.ts_resp', d1_ts_resp) # decision1 response
            trials.addData('decision2.ts_start', decision2.ts_start) #  decision2 fixation cross onset
            trials.addData('decision2.ts_fractal', decision2.ts_fractal) #  decision2 fractals onset
            trials.addData('decision2.ts_resp', d2_ts_resp) # decision2 response
            trials.addData('feedback.ts_start', fb_ts_start) #  feedback fixation cross onset
            trials.addData('feedback.ts_feedback', fb_ts_fb)  #  feedback reward onset
            
            # Record trial duration
            duration = globalClock.getTime()-decision1.ts_start
            
            # Delete miss that has been repeated
            if (decision2.keys!=None) and myCount >= nTrials and len(misses) > 0 and saccadeMiss == 0:
                misses.pop(0)
        
            # Stop eye tracking
            if useEyeTracker:
                 
                # Send a message to mark the end of trial
                eyeTracker.sendMessage('TRIAL OK')
                
                # EyeLink - stop recording eye data
                eyeTracker.stopRecording()
        
        # Record data
        trials.addData('whichLoop', whichLoop)
        trials.addData('block', blockIndex)
        trials.addData('blockNumber', blockNumber)
        trials.addData('eyeTracker', useEyeTracker)
        trials.addData('missIndex', missIndex)
        trials.addData('misses', missCounter)
        trials.addData('currentMiss', currentMiss)
        trials.addData('onset', decision1.ts_start) 
        trials.addData('duration', duration) 
        thisExp.nextEntry()
        
        # Print out useful information about trials and block 
        print('----------')
        print('Block index %s' %blockIndex) 
        print('Block # %s' %blockNumber)
        print('Trial # %s' %myCount)
        print('Miss # %s' %missCounter)
        # print('Performance: %s' %currentPerf)
        print('Performance: %s' %accPerf)

        # Update counter
        myCount = myCount + 1
        
        # Check if we have to repeat any misses
        if (myCount) >= nTrials and len(misses)==0:
            break
            
        if myCount >=30 and not session == 4: 
            break
    
    # Block performance 
#    if not session == 4:
#        if 'decision2' in locals():
#            accPerf = trials.data['decision1.reward'].sum() + trials.data['decision2.reward'].sum()
#        else:
#            accPerf = trials.data['decision1.reward'].sum()
#    else: 
#        accPerf = np.nan
    if session == 4:
        accPerf = np.nan
        
    win.setRecordFrameIntervals(False)    
    
    return(accPerf, win)