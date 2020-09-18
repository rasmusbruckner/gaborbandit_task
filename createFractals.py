from numpy.random import random
import random
from psychopy import core
from giveFeedback import giveFeedback
import pylink

def createFractals(experimentStructure, outcomeStructure, stimuliStructure, redFractal, targetPatch, corrAns,
trials, outcomes, feedbackText, misses, missCounter, myCount, routineTimer, globalClock, nTrials, accPerf, eyeTracker=0):
    """ This function creates the fractals
    
    Input: 
        experimentStructure: all general experimental properties 
        outcomeStructure: all general outcome properties 
        stimuliStructure: all general stimulus properties
        redFractal: position of red fractal (from xls block files)
        targetPatch: position of the patch that should be identified (from xls block files)
        corrAns: indicates which button should be pressed (up vs. down)
        trials: trial handler Psychopy object instance
        outcome: outcome if anwer is correct (from xls block files)
        feedbackText: feedback text object instance
        misses: temporarily saves information about trials that have been missed to repeat these trials
        missCounter: counter for number of misses
        myCount: counter for total number of completed trials (if missed trials exist, can be larger than nTrials)
        routineTimer: timer to control presentation times
        globalClock: clock to control timing during fMRI
        nTrials: number of trials
        accPerf: Accumulated performance
        eyeTracker: eye-tracker object instance
    
    Return:
        decision2: decision2 object instance
        trials: trial handler Psychopy object instance
        misses: temporarily saves information about trials that have been missed to repeat these trials
        accPerf: Accumulated performance
        missCounter: counter for number of misses
        routineTimer: timer to control presentation times
        globalClock: clock to control timing during fMRI
        decision2.timestamp: indicates decision2 onset
        fixCrossTiming: actual presentation time of fixation cross during fractal phase
        feedbackTimestamp: indicates feedback onset
        fixCrossTiming_feedback: actual presentation time of fixation cross during feedback
        missIndex: indicates if current trial was missed
    """
    
    # Create some shortnames
    expInfo = experimentStructure['expInfo']
    session = expInfo['session']
    NOT_STARTED = experimentStructure['NOT_STARTED']
    STARTED = experimentStructure['STARTED']
    FINISHED = experimentStructure['FINISHED']
    STOPPED = experimentStructure['STOPPED']
    endExpNow = experimentStructure['endExpNow']
    event = experimentStructure['event']
    win = experimentStructure['win']
    whichVersion = experimentStructure['whichVersion']
    useEyeTracker = experimentStructure['useEyeTracker']
    winFeedback = outcomeStructure['winFeedback']
    neutralFeedback = outcomeStructure['neutralFeedback']
    reward = outcomeStructure['reward']
    noReward = outcomeStructure['noReward']
    fractalClock = stimuliStructure['fractalClock']
    fractal1 = stimuliStructure['fractal1']
    fractal2 = stimuliStructure['fractal2']
    fixationCross = stimuliStructure['fixationCross']
    fixCrossTiming = stimuliStructure['fixCrossTiming']
    jitter = stimuliStructure['jitter']
    stimulusTiming = stimuliStructure['stimulusTiming']
    feedbackClock = stimuliStructure['feedbackClock']

    # Create variable for buttons of button box used in fMRI experiment
    upButton = '3'
    downButton = '1'
    
    #------Prepare to start Routine "decision2"-------
    t = 0
    fractalClock.reset() 
    frameN = -1
    currentJitter = random.uniform(0,jitter)
    fixCrossTiming = fixCrossTiming + currentJitter
    routineTimer.add(fixCrossTiming + stimulusTiming)
    
    # Compute position of fractals
    pos = 3
    if redFractal == 'up':
        fractal1.setPos([0,-pos])
        fractal2.setPos([0,pos])
    elif redFractal == 'down':
        fractal1.setPos([0,pos])
        fractal2.setPos([0,-pos])
    
    # Get correct keys 
    if whichVersion == 1 or (whichVersion == 2 and session == 1):
        if redFractal == 'up':
            redFractalKey = 'up'
            blueFractalKey = 'down'
        elif redFractal == 'down':
            redFractalKey = 'down'
            blueFractalKey = 'up'
    elif whichVersion == 2:
        if redFractal == 'up':
            redFractalKey = upButton
            blueFractalKey = downButton
        elif redFractal == 'down':
            redFractalKey = downButton
            blueFractalKey = upButton
            
    if whichVersion == 1 or (whichVersion == 2 and session == 1):
        corrAnsKey = corrAns
    elif whichVersion == 2:
        if corrAns == 'up':
            corrAnsKey = upButton
        elif corrAns == 'down':
            corrAnsKey = downButton
    
    # Create an object of type KeyResponse
    decision2 = event.BuilderKeyResponse()  
    decision2.status = NOT_STARTED
    
    # Keep track of which components have finished
    decision2Components = []
    decision2Components.append(fixationCross)
    decision2Components.append(fractal1)
    decision2Components.append(fractal2)
    decision2Components.append(decision2)
    for thisComponent in decision2Components:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "decision2"-------
    decision2.ts_start = globalClock.getTime()
    triggered = False # indicate if fractal onset trigger has been recorded
    
    missIndex = 0
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
    
        # Get current time
        t = fractalClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        
        # *fixationCross* updates
        if t >= 0.0 and fixationCross.status == NOT_STARTED:
            # keep track of start time/frame for later
            fixationCross.tStart = t  # underestimates by a little under one frame
            fixationCross.frameNStart = frameN  # exact frame index
            fixationCross.setAutoDraw(True)
            if useEyeTracker:
                # Send ET message
                eyeTracker.sendMessage('FRACTALS PHASE ON')
        if fixationCross.status == STARTED and t >= (0.0 + (fixCrossTiming + stimulusTiming - win.monitorFramePeriod*0.75)): #most of one frame period left
            fixationCross.setAutoDraw(False)
        
        # *fractal1* updates
        if t >= fixCrossTiming and fractal1.status == NOT_STARTED:
            # keep track of start time/frame for later
            fractal1.tStart = t  # underestimates by a little under one frame
            fractal1.frameNStart = frameN  # exact frame index
            fractal1.setAutoDraw(True)
            if useEyeTracker:
                # Send ET message
                eyeTracker.sendMessage('FRACTALS ON')
        if fractal1.status == STARTED and t >= (fixCrossTiming + (stimulusTiming - win.monitorFramePeriod*0.75)): #most of one frame period left
            fractal1.setAutoDraw(False)
        
        # *fractal2* updates
        if t >= fixCrossTiming and fractal2.status == NOT_STARTED:
            # keep track of start time/frame for later
            fractal2.tStart = t  # underestimates by a little under one frame
            fractal2.frameNStart = frameN  # exact frame index
            fractal2.setAutoDraw(True)
        if fractal2.status == STARTED and t >= (fixCrossTiming + (stimulusTiming - win.monitorFramePeriod*0.75)): #most of one frame period left
            fractal2.setAutoDraw(False)
        
        # *decision2* updates
        if t >= fixCrossTiming and decision2.status == NOT_STARTED:
            # keep track of start time/frame for later
            decision2.tStart = t  # underestimates by a little under one frame
            decision2.frameNStart = frameN  # exact frame index
            decision2.status = STARTED
            # keyboard checking is just starting
            decision2.clock.reset()
            event.clearEvents(eventType='keyboard')
        if decision2.status == STARTED and t >= (fixCrossTiming + (stimulusTiming - win.monitorFramePeriod*0.75)): #most of one frame period left
            decision2.status = STOPPED
        if decision2.status == STARTED:
            if whichVersion == 1 or (whichVersion == 2 and session == 1):
                theseKeys = event.getKeys(keyList=['up', 'down'])
            elif whichVersion == 2:
                theseKeys = event.getKeys(keyList=[upButton, downButton])
            
            # Check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                decision2.keys = theseKeys[-1]  # just the last key pressed
                decision2.rt = decision2.clock.getTime()
                
                # Which response?
                if (decision2.keys == str(redFractalKey)) or (decision2.keys == redFractalKey):
                    decision2.color = 1
                else:
                    decision2.color = 2
                
                # Was the answer correct? 
                if (decision2.keys == str(corrAnsKey)) or (decision2.keys == corrAnsKey):
                    decision2.corr = 1
                else:
                    decision2.corr = 0
                    
                # Todo: schauen, ob wir das brauchen
                if useEyeTracker:
                    eyeTracker.sendMessage("FRACTALS RESPONSE %s"%(decision2.keys))
                    
            for thisComponent in decision2Components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
                else:
                    continueRoutine = False
            
        # Check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # Refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            
            # Send  patch onset trigger
            if t >= fixCrossTiming and triggered == False:
                decision2.ts_fractal = globalClock.getTime() # send trigger
                triggered = True # indicate that patch trigger has been recorded
            
            # Refresh the screen
            win.flip()
        
     # Stop eye tracking
    if useEyeTracker:
        
        # Send a message to mark the end of trial
        eyeTracker.sendMessage('FRACTALS PHASE OFF')
    
    #-------Ending Routine "decision2"-------
    for thisComponent in decision2Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # Check responses
    # ---------------
    if decision2.keys in ['', [], None]:
       decision2.keys=None
       decision2.color = float('nan')
       if str(corrAns).lower() == 'none': 
        decision2.corr = float('nan')
        decision2.rt = float('nan')
       else: 
        decision2.corr = float('nan')
        decision2.rt = float('nan')
    
    if (decision2.keys is None):
        decision2.reward = noReward
        msg = "Zu langsam!"
        
        if myCount <  nTrials:
            misses.append(myCount)
            missCounter = missCounter + 1
            missIndex = 1
            
    elif (decision2.corr == 1):
            
        if float(outcomes) == 1:
            decision2.reward = reward
            msg = winFeedback
        else:
            decision2.reward = noReward
            msg = neutralFeedback
    elif (decision2.corr == 0):
        
        if float(outcomes) == 1: 
            decision2.reward = noReward
            msg = neutralFeedback
        else:
            decision2.reward = reward
            msg = winFeedback
            
    # Store data for trials (TrialHandler)
    trials.addData('decision2.rt', decision2.rt)
    trials.addData('decision2.keys',decision2.keys)
    trials.addData('decision2.corr', decision2.corr)
    trials.addData('decision2.color', decision2.color)
    trials.addData('decision2.reward', decision2.reward)
    accPerf = accPerf + decision2.reward #trials.data['decision2.reward'].sum()
    trials.addData('decision2.accPerf', accPerf)
    
    # Give feedback
    (routineTimer, globalClock, feedbackTimestamp, fixCrossTiming_feedback) = giveFeedback(experimentStructure, stimuliStructure, feedbackText, msg, routineTimer, globalClock, missIndex, eyeTracker)
    
    return(decision2, trials, misses, missCounter, accPerf, routineTimer, globalClock, decision2.ts_start, fixCrossTiming, feedbackTimestamp, fixCrossTiming_feedback, missIndex)