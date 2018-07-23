import numpy as np
from psychopy import core
import random


def createPatches(experimentStructure, stimuliStructure, patchClock, targetPatch,
trials, whichLoop, thisDifference, contrast, routineTimer, globalClock, tracker):
    """ This function creates the Gabor-patches
    
    Input:
        experimentStructure: all general experimental properties 
        stimuliStructure: all general stimulus properties
        patchClock: clock object instance for patch timing
        targetPatch: position of the patch that should be identified (from xls block files)
        trials: trial handler Psychopy object instance
        whichLoop: indicates required task phase
        thisDifference: Not used anymore 
        contrast: presented contrast difference (from xls block files)
        routineTimer: timer to control presentation times
        globalClock: clock to control timing during fMRI
        tracker: eye-tracker object instance
        
    Return:
        decision1: decision1 object instance
        trials: trial handler Psychopy object instance
        routineTimer: timer to control presentation times
        globalClock: clock to control timing during fMRI
        decision1.timestamp: indicates decision2 onset
        fixCrossTiming: actual presentation time of fixation cross during patches phase
        saccadeMiss: Indicates if participant did not properly fixate stimulus (if eye-tracker is used)
    """

    # Create some shortnames
    expInfo         = experimentStructure['expInfo']
    cBal            = expInfo['cBal']
    globalClock     = experimentStructure['globalClock']
    NOT_STARTED     = experimentStructure['NOT_STARTED']
    STARTED         = experimentStructure['STARTED']
    FINISHED        = experimentStructure['FINISHED']
    STOPPED         = experimentStructure['STOPPED']
    event           = experimentStructure['event']
    whichVersion    = experimentStructure['whichVersion']
    patch1          = stimuliStructure['patch1']
    patch2          = stimuliStructure['patch2']
    endExpNow       = experimentStructure['endExpNow']
    event           = experimentStructure['event']
    win             = experimentStructure['win']
    useEyeTracker   = experimentStructure['useEyeTracker']
    fixationCross   = stimuliStructure['fixationCross']
    fixCrossTiming  = stimuliStructure['fixCrossTiming']
    jitter          = stimuliStructure['jitter']
    stimulusTiming  = stimuliStructure['stimulusTiming']
    

    #------Prepare to start Routine "trial"-------
    t = 0
    patchClock.reset()  # clock 
    frameN = -1
    
    # Draw jitter for current trial
    currentJitter = random.uniform(0,jitter)
    fixCrossTiming = fixCrossTiming + currentJitter
    
    # Routine timer for presentation timing
    routineTimer.add(fixCrossTiming + stimulusTiming)
    
    # Set mean opacity of patches
    meanOpacity = 0.5
    
    contrast = float(contrast)
    if cBal == '1':
        if targetPatch == 'left':
            patch1.setPos([-6,0])
            patch2.setPos([6,0])
        elif targetPatch == 'right':
            patch1.setPos([6,0])
            patch2.setPos([-6,0])
    elif cBal == '2':
        if targetPatch == 'left':
            patch1.setPos([6,0])
            patch2.setPos([-6,0])
        elif targetPatch == 'right':
            patch1.setPos([-6,0])
            patch2.setPos([6,0])
            
    # Get correct keys 
    if whichVersion == 1:
        targetPatchKey   = targetPatch
    elif whichVersion == 2:
        if targetPatch == 'left':
            targetPatchKey = '3'
        elif targetPatch == 'right':
            targetPatchKey = '1'
            
    # Compute delta contrast and state
    if targetPatch == 'left':
        deltaContrast = contrast*-1
        state         = 0
    elif targetPatch == 'right':
        deltaContrast = contrast
        state         = 1
    
    # Set opacity of patches
    opacityPatch1 = (meanOpacity + contrast/2)
    opacityPatch2 = (meanOpacity - contrast/2)
    patch1.setOpacity(opacityPatch1)
    patch2.setOpacity(opacityPatch2)
    
    decision1 = event.BuilderKeyResponse()  # create an object of type KeyResponse
    decision1.status = NOT_STARTED
    
    # Keep track of which components have finished
    trialComponents = []
    trialComponents.append(patch1)
    trialComponents.append(patch2)
    trialComponents.append(decision1)
    trialComponents.append(fixationCross)
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
            
#-------Start Routine "trial"-------

    decision1.timestamp = globalClock.getTime()
    
    ## pygaze stuff
    if useEyeTracker:
        tracker.start_recording()

    # drift correction (needed?)
    # keyboard = libinput.Keyboard(keylist=['space'], timeout=None)

    saccadeMiss = 0
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        
        if useEyeTracker:
            onesample = tracker.sample()
            
        if useEyeTracker:
            if (onesample[0] > 1330 or onesample[0] < 1230)  and (onesample[1] > 770 or onesample[1] < 670):
                saccadeMiss = 1
        
        # Get current time
        t = patchClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        
        # Update/draw components on each frame
        # *patch1* updates
        if t >= fixCrossTiming and patch1.status == NOT_STARTED:
            # keep track of start time/frame for later
            patch1.tStart = t  # underestimates by a little under one frame
            patch1.frameNStart = frameN  # exact frame index
            patch1.setAutoDraw(True)
        if patch1.status == STARTED and t >= (fixCrossTiming + (stimulusTiming - win.monitorFramePeriod*0.75)): #most of one frame period left
            patch1.setAutoDraw(False)
        
        # *patch2* updates
        if t >= fixCrossTiming and patch2.status == NOT_STARTED:
            # keep track of start time/frame for later
            patch2.tStart = t  # underestimates by a little under one frame
            patch2.frameNStart = frameN  # exact frame index
            patch2.setAutoDraw(True)
        if patch2.status == STARTED and t >= (fixCrossTiming + (stimulusTiming - win.monitorFramePeriod*0.75)): #most of one frame period left
            patch2.setAutoDraw(False)
            
        # *fixationCross* updates
        if t >= 0.0 and fixationCross.status == NOT_STARTED:
            # keep track of start time/frame for later
            fixationCross.tStart = t  # underestimates by a little under one frame
            fixationCross.frameNStart = frameN  # exact frame index
            fixationCross.setAutoDraw(True)
        if fixationCross.status == STARTED and t >= (0.0 + (fixCrossTiming + stimulusTiming - win.monitorFramePeriod*0.75)): #most of one frame period left
            fixationCross.setAutoDraw(False)
        
        # *decision1* updates
        if t >= fixCrossTiming and decision1.status == NOT_STARTED:
            # keep track of start time/frame for later
            decision1.tStart = t  # underestimates by a little under one frame
            decision1.frameNStart = frameN  # exact frame index
            decision1.status = STARTED
            
            # Keyboard checking is just starting
            decision1.clock.reset()  # now t=0
            event.clearEvents(eventType='keyboard')
        if decision1.status == STARTED and t >= (fixCrossTiming + (stimulusTiming - win.monitorFramePeriod*0.75)): #most of one frame period left
            decision1.status = STOPPED
        if decision1.status == STARTED:
            if whichVersion == 1:
                theseKeys = event.getKeys(keyList=['left', 'right'])
            elif whichVersion == 2:
                theseKeys = event.getKeys(keyList=['3', '1'])
                
            # Check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                decision1.keys = theseKeys[-1]  # just the last key pressed
                decision1.rt = decision1.clock.getTime()
                
                # Was this 'correct'?
                if (decision1.keys == str(targetPatchKey)) or (decision1.keys == targetPatchKey):
                    decision1.corr = 1
                else:
                    decision1.corr = 0
                
                # In current version (07/16) no reward for perceptual decision
                decision1.reward = 0
                
        for thisComponent in trialComponents:
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
            win.flip()
            
    # Stop eye tracking
    if useEyeTracker:
        tracker.stop_recording()
        #log.write([trialnr, trialtype,endpos, t1-t0, correct])

    #-------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Check responses
    if decision1.keys in ['', [], None]:  # No response was made
       decision1.keys = None
       decision1.corr = 0 # sonst zeigt der bei miss keinen kumulierten wert float('nan')  # failed to respond (incorrectly)
       decision1.reward = 0  # failed to respond (incorrectly)
    
    # Store data for trials (TrialHandler)
    if (whichLoop == 'patches' or whichLoop == 'practice1' or whichLoop == 'practice2' or 
    whichLoop == 'practice3' or whichLoop == 'practice4' or whichLoop == 'practice5' or whichLoop == 'main_safe' or whichLoop == 'main_unc'):
        trials.addData('contrast', str(contrast))
        trials.addData('deltaContrast', deltaContrast)
        trials.addData('state', state)
        trials.addData('opacityPatch1', opacityPatch1)
        trials.addData('opacityPatch2', opacityPatch2)
        trials.addData('meanOpacity', meanOpacity)
        trials.addData('decision1.keys',decision1.keys)
        if decision1.keys == 'left':
            decision1.decision = 0
            trials.addData('decision1.decision',0)
        elif decision1.keys == 'right':
            trials.addData('decision1.decision',1)
        elif decision1.keys == None:
            trials.addData('decision1.decision',float('nan'))
        trials.addData('decision1.corr', decision1.corr)
        trials.addData('decision1.reward', decision1.reward)
        accPerf = trials.data['decision1.reward'].sum()
        trials.addData('decision1.accPerf', accPerf)   
    
    # Currently not in use
    #elif whichLoop == 'quest':
        # store data for stairs (currently not used)
        #trials.addResponse(decision1.corr)
    
    return(decision1, trials, routineTimer, globalClock, decision1.timestamp, fixCrossTiming, saccadeMiss)
