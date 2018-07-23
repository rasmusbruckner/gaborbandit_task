from psychopy import visual, core, data, event, logging, sound, gui
import random

def runDigitSpan(experimentStructure, stimuliStructure, globalClock, filename, routineTimer, text, stim, N_Back, thisExp, thisTrial):
    """" This function runs the digit-span task
    
        Input:
            experimentStructure: all general experimental properties 
            stimuliStructure: all general stimulus properties
            globalClock: clock to control timing during fMRI
            filename: not used anymore
            routineTimer: timer to control presentation times
            text: digit span text object instance
            stim: current stimulus from pre-defined data
            N_Back: trial handler (rename)
            thisExp: experiment handler
            thisTrial: currentTrial
    
        Return:
            N_Back: trial handler (rename)
            decision1: response object instance
            thisExp: experiment handler
            thisTrial: currentTrial
            miss: temporarily saves information about trials that have been missed to repeat these trials
    """

    # Create some shortnames
    expInfo         = experimentStructure['expInfo']
    thisExp         = experimentStructure['thisExp']
    win             = experimentStructure['win']
    NOT_STARTED     = experimentStructure['NOT_STARTED']
    STARTED         = experimentStructure['STARTED']
    STOPPED         = experimentStructure['STOPPED']
    FINISHED        = experimentStructure['FINISHED']
    endExpNow       = experimentStructure['endExpNow']
    event           = experimentStructure['event']
    win             = experimentStructure['win']
    fixationCross   = stimuliStructure['fixationCross']
    fixCrossTiming  = stimuliStructure['fixCrossTiming']
    jitter          = stimuliStructure['jitter']
    stimulusTiming  = stimuliStructure['stimulusTiming']
    feedbackClock   = stimuliStructure['feedbackClock']
    
    #------Prepare to start Routine "feedback"-------
    t = 0
    feedbackClock.reset()  # clock 
    frameN = -1
    currentJitter = random.uniform(0,jitter)
    routineTimer.add(fixCrossTiming + stimulusTiming)
    decision1 = event.BuilderKeyResponse()  # create an object of type KeyResponse
    decision1.status = NOT_STARTED
    text.setText(stim)
    
    # Keep track of which components have finished
    feedbackComponents = []
    feedbackComponents.append(text)
    feedbackComponents.append(fixationCross)
    for thisComponent in feedbackComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "feedback"-------
    feedbackTimestamp = globalClock.getTime()
    continueRoutine = True
    miss = 0
    while continueRoutine and routineTimer.getTime() > 0:
    
        # Get current time
        t = feedbackClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # Update/draw components on each frame
        
        # *text* updates
        if t >= fixCrossTiming and text.status == NOT_STARTED:
            # Keep track of start time/frame for later
            text.tStart = t  # underestimates by a little under one frame
            text.frameNStart = frameN  # exact frame index
            text.setAutoDraw(True)
        if text.status == STARTED and t >= (fixCrossTiming + (stimulusTiming - win.monitorFramePeriod*0.75)): #most of one frame period left
            text.setAutoDraw(False)
        
        # *fixationCross* updates
        if t >= 0.0 and fixationCross.status == NOT_STARTED:
            # keep track of start time/frame for later
            fixationCross.tStart = t  # underestimates by a little under one frame
            fixationCross.frameNStart = frameN  # exact frame index
            fixationCross.setAutoDraw(True)
        if fixationCross.status == STARTED and t >= (0.0 + (fixCrossTiming - win.monitorFramePeriod*0.75)): #most of one frame period left
            fixationCross.setAutoDraw(False)
        
        # Check if all components have finished
        for thisComponent in feedbackComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
            else:
                continueRoutine = False
                
         # *decision1* updates
        if t >= fixCrossTiming and decision1.status == NOT_STARTED:
            
            # Keep track of start time/frame for later
            decision1.tStart = t  # underestimates by a little under one frame
            decision1.frameNStart = frameN  # exact frame index
            decision1.status = STARTED
            
            # Keyboard checking is just starting
            decision1.clock.reset()  # now t=0
            event.clearEvents(eventType='keyboard')
        if decision1.status == STARTED and t >= (fixCrossTiming + (stimulusTiming - win.monitorFramePeriod*0.75)): #most of one frame period left
            decision1.status = STOPPED
        
        # Check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # Refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
        
    #-------Ending Routine "feedback"-------
    for thisComponent in feedbackComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    return(N_Back, decision1, thisExp, thisTrial, miss)
