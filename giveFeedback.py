from psychopy import core
import random

def giveFeedback(experimentStructure, stimuliStructure, feedbackText, msg, routineTimer, globalClock, miss):
    """" This function displays the reward feedback 
    
    Input:
        experimentStructure: all general experimental properties 
        stimuliStructure: all general stimulus properties
        feedbackText: feedback text object instance
        msg: variable text that should be displayed
        routineTimer: timer to control presentation times
        globalClock: clock to control timing during fMRI
        miss: indicate if response was missed
    
    Return:
        routineTimer: timer to control presentation times
        globalClock: clock to control timing during fMRI
        feedbackTimestamp: indicates feedback onset
        fixCrossTiming: actual presentation time of fixation cross
    """
    
    # create some shortnames
    NOT_STARTED     = experimentStructure['NOT_STARTED']
    STARTED         = experimentStructure['STARTED']
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
    if miss == 0:
        fixCrossTiming = fixCrossTiming + currentJitter
    elif miss == 1:
        fixCrossTiming = 0
        
    routineTimer.add(fixCrossTiming + stimulusTiming)
    feedbackText.setText(msg)
    
    # Keep track of which components have finished
    feedbackComponents = []
    feedbackComponents.append(feedbackText)
    feedbackComponents.append(fixationCross)
    for thisComponent in feedbackComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    #-------Start Routine "feedback"-------
    feedbackTimestamp = globalClock.getTime()
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        
        # Get current time
        t = feedbackClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        
        # Update/draw components on each frame
        
        # *feedbackText* updates
        if t >= fixCrossTiming and feedbackText.status == NOT_STARTED:
            # keep track of start time/frame for later
            feedbackText.tStart = t  # underestimates by a little under one frame
            feedbackText.frameNStart = frameN  # exact frame index
            feedbackText.setAutoDraw(True)
        if feedbackText.status == STARTED and t >= (fixCrossTiming + (stimulusTiming - win.monitorFramePeriod*0.75)): #most of one frame period left
            feedbackText.setAutoDraw(False)
        
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
    
    return(routineTimer, globalClock, feedbackTimestamp, fixCrossTiming)