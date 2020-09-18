from initializeComponents import initializeFractalsExample
from psychopy import core

def fractalsExample(experimentStructure, exampleText, corrAns):
    """ This function presents fractals during the instructions
    
    Input:
        experimentStructure: all general experimental properties 
        exampleText: exampleText object instance
        corrAns: indicates which fractal should be identified
    
    Return: ~
    """
     
    # Create some shortnames
    NOT_STARTED     = experimentStructure['NOT_STARTED']
    STARTED         = experimentStructure['STARTED']
    FINISHED        = experimentStructure['FINISHED']
    STOPPED         = experimentStructure['STOPPED']
    endExpNow       = experimentStructure['endExpNow']
    event           = experimentStructure['event']
    win             = experimentStructure['win']

    # Initialize components for Routine "initializeFractalsExample"
    (fractalClock, fractal1, fractal2, exampleText)  = initializeFractalsExample(win, exampleText)
    
    #------Prepare to start Routine "fractalsExample"-------
    t = 0
    fractalClock.reset()  # clock 
    frameN = -1
    
    # Update component parameters for each repeat
    redFractal = 'up'
    darkBandit = 'left'
    corrAnsLeft = 'up'
    if redFractal == 'up':
        fractal1.setPos([0,-3])
        fractal2.setPos([0,3])
    elif redFractal == 'down':
        fractal1.setPos([0,3])
        fractal2.setPos([0,-3])
        
    if darkBandit == 'left':
        corrAnsF = corrAnsLeft
    elif darkBandit == 'right':
        corrAnsF = corrAnsRight

    fractalsExample = event.BuilderKeyResponse()  # create an object of type KeyResponse
    fractalsExample.status = NOT_STARTED
    
    # Keep track of which components have finished
    feComponents = []
    feComponents.append(fractal1)
    feComponents.append(fractal2)
    feComponents.append(fractalsExample)
    feComponents.append(exampleText)
    for thisComponent in feComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "fractalsExample"-------
    continueRoutine = True
    while continueRoutine: # and routineTimer.getTime() > 0:
        
        # Get current time
        t = fractalClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        
        # Update/draw components on each frame

        # *fractal1* updates
        if t >= 0.0 and fractal1.status == NOT_STARTED:
            # keep track of start time/frame for later
            fractal1.tStart = t  # underestimates by a little under one frame
            fractal1.frameNStart = frameN  # exact frame index
            fractal1.setAutoDraw(True)
        
        # *fractal2* updates
        if t >= 0.0 and fractal2.status == NOT_STARTED:
            # keep track of start time/frame for later
            fractal2.tStart = t  # underestimates by a little under one frame
            fractal2.frameNStart = frameN  # exact frame index
            fractal2.setAutoDraw(True)
        
        # *fractalsExample* updates
        if t >= 0.0 and fractalsExample.status == NOT_STARTED:
            # keep track of start time/frame for later
            fractalsExample.tStart = t  # underestimates by a little under one frame
            fractalsExample.frameNStart = frameN  # exact frame index
            fractalsExample.status = STARTED
            # keyboard checking is just starting
            fractalsExample.clock.reset()  # now t=0
            event.clearEvents(eventType='keyboard')
        if fractalsExample.status == STARTED:
            theseKeys = event.getKeys(keyList=[corrAns])
            
            # Check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                fractalsExample.keys = theseKeys[-1]  # just the last key pressed
                fractalsExample.rt = fractalsExample.clock.getTime()
                if (fractalsExample.keys == str(corrAnsF)) or (fractalsExample.keys == corrAnsF):
                    fractalsExample.corr = 1
                else:
                    fractalsExample.corr = 0
                # a response ends the routine
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
        for thisComponent in feComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # Check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # Refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "fractalsExample"-------
    for thisComponent in feComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Check responses
    if fractalsExample.keys in ['', [], None]:  # No response was made
       fractalsExample.keys=None
       # Was no response the correct answer?!
       if str(corrAnsF).lower() == 'none': fractalsExample.corr = 1  # correct non-response
       else: fractalsExample.corr = 0  # failed to respond (incorrectly)