from initializeComponents import initializePatchesExample
from psychopy import core

def patchesExample(experimentStructure, exampleText, positionPatch1, positionPatch2, corrAns):
    """ This function presents Gabor-patches during the instructions
    
    Input:
        experimentStructure: All general experimental properties 
        exampleText: exampleText object instance
        positionPatch1: screen position of first patch
        positionPatch2: screen position of second patch
        corrAns: indicates which patch should be identified
    
    Return: ~
    """

    # Create some shortnames
    thisExp      = experimentStructure['thisExp']
    NOT_STARTED  = experimentStructure['NOT_STARTED']
    STARTED      = experimentStructure['STARTED']
    FINISHED     = experimentStructure['FINISHED']
    endExpNow    = experimentStructure['endExpNow']
    event        = experimentStructure['event']
    win          = experimentStructure['win']
    
    # Initialize components for Routine "initializePatchesExample"
    (patchExampleClock, examplePatch1, examplePatch2, exampleText) = initializePatchesExample(win, exampleText, positionPatch1, positionPatch2)
    
    #------Prepare to start Routine "patchesExample"-------
    t = 0
    patchExampleClock.reset()  # clock 
    frameN = -1
    
    # Update component parameters for each repeat
    patchExample = event.BuilderKeyResponse()  # create an object of type KeyResponse
    patchExample.status = NOT_STARTED
   
    # Keep track of which components have finished
    peComponents= []
    peComponents.append(examplePatch1)
    peComponents.append(examplePatch2)
    peComponents.append(patchExample)
    peComponents.append(exampleText)
    for thisComponent in peComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    #-------Start Routine "trial"-------
    continueRoutine = True
    while continueRoutine:
        # Get current time
        t = patchExampleClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        
        # *patch1* updates
        if t >= 0.0 and examplePatch1.status == NOT_STARTED:
            # keep track of start time/frame for later
            examplePatch1.tStart = t  # underestimates by a little under one frame
            examplePatch1.frameNStart = frameN  # exact frame index
            examplePatch1.setAutoDraw(True)
        
        # *patch2* updates
        if t >= 0.0 and examplePatch2.status == NOT_STARTED:
            # keep track of start time/frame for later
            examplePatch2.tStart = t  # underestimates by a little under one frame
            examplePatch2.frameNStart = frameN  # exact frame index
            examplePatch2.setAutoDraw(True)
        
        # *patchExample* updates
        if t >= 0.0 and patchExample.status == NOT_STARTED:
            # keep track of start time/frame for later
            patchExample.tStart = t  # underestimates by a little under one frame
            patchExample.frameNStart = frameN  # exact frame index
            patchExample.status = STARTED
            
            # Keyboard checking is just starting
            patchExample.clock.reset()  # now t=0
            event.clearEvents(eventType='keyboard')
        if patchExample.status == STARTED:
            theseKeys = event.getKeys(keyList=[corrAns])
            
            # Check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                patchExample.keys = theseKeys[-1]  # just the last key pressed
                patchExample.rt = patchExample.clock.getTime()
                
                # A response ends the routine
                continueRoutine = False
        
        # *exampleText* updates
        if t >= 0.0 and exampleText.status == NOT_STARTED:
            # keep track of start time/frame for later
            exampleText.tStart = t  # underestimates by a little under one frame
            exampleText.frameNStart = frameN  # exact frame index
            exampleText.setAutoDraw(True)

        # Check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in peComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # Check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # Refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    #-------Ending Routine "trial"-------
    for thisComponent in peComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # Check responses
    if patchExample.keys in ['', [], None]:  # No response was made
       patchExample.keys=None
