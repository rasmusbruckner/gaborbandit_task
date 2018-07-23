from psychopy import event, core
from initializeComponents import initializeSimpleInstructions

def simpleInstructions(experimentStructure, header, headerSize, headerPosition, mainText, mainSize, mainPosition):
    """ This function displays instructions to the participant
    
    Input:
        experimentStructure: all general experimental properties 
        header: header for instructions
        headerSize: height of header on the screen
        headerPosition: position of header on the screen
        mainText: instructions text
        mainSize: height of instructions text on the screen
        mainPosition: position of the instructions text on the screen
    
    Return: ~
    
    """
    # Create some shortnames
    thisExp     = experimentStructure['thisExp']
    NOT_STARTED = experimentStructure['NOT_STARTED']
    STARTED     = experimentStructure['STARTED']
    FINISHED    = experimentStructure['FINISHED']
    win         = experimentStructure['win']
    endExpNow   = experimentStructure['endExpNow']
    
    # Initialize instructions object
    (instructionsClock, header, mainText) = initializeSimpleInstructions(win, header, headerSize, headerPosition, mainText, mainSize, mainPosition)
    
#------Prepare to start Routine "simpleInstructions"-------
    t = 0
    instructionsClock.reset()  # clock 
    frameN = -1
    # Update component parameters for each repeat
    simpleInstructions = event.BuilderKeyResponse()  # create an object of type KeyResponse
    simpleInstructions.status = NOT_STARTED
    
    # Keep track of which components have finished
    siComponents = []
    siComponents.append(header)
    siComponents.append(mainText)
    siComponents.append(simpleInstructions)
    for thisComponent in siComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "simpleInstructions"-------
    continueRoutine = True
    while continueRoutine:
        
        # Get current time
        t = instructionsClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # Update/draw components on each frame
        
        # *header* updates
        if t >= 0.5 and header.status == NOT_STARTED:
            # keep track of start time/frame for later
            header.tStart = t  # underestimates by a little under one frame
            header.frameNStart = frameN  # exact frame index
            header.setAutoDraw(True)
            
        # *mainText* updates
        if t >= 0.5 and mainText.status == NOT_STARTED:
            # keep track of start time/frame for later
            mainText.tStart = t  # underestimates by a little under one frame
            mainText.frameNStart = frameN  # exact frame index
            mainText.setAutoDraw(True)
        
        # *simpleInstructions* updates
        if t >= 0.5 and simpleInstructions.status == NOT_STARTED:
            # keep track of start time/frame for later
            simpleInstructions.tStart = t  # underestimates by a little under one frame
            simpleInstructions.frameNStart = frameN  # exact frame index
            simpleInstructions.status = STARTED
            # keyboard checking is just starting
            simpleInstructions.clock.reset()  # now t=0
            event.clearEvents(eventType='keyboard')
        if simpleInstructions.status == STARTED:
            theseKeys = event.getKeys(keyList=['return'])
            
            # Check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                simpleInstructions.keys = theseKeys[-1]  # just the last key pressed
                simpleInstructions.rt = simpleInstructions.clock.getTime()
                # a response ends the routine
                continueRoutine = False
        
        # Check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in siComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # Check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # Refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    #-------Ending Routine "simpleInstructions"-------
    for thisComponent in siComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Check responses
    if simpleInstructions.keys in ['', [], None]:  # No response was made
       simpleInstructions.keys=None