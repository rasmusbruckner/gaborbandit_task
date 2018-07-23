# -*- coding: utf-8 -*-
# Digit-Span Task
#
# Simple digit-span task that can 
# be used in combination with 
# Gabor-Bandit task.
#
# Written by RB. Version 06/2017
from psychopy import visual, core, data, event, logging, sound, gui
from giveFeedback import giveFeedback
from runDigitSpan import runDigitSpan
import random
import os
from initializeComponents import initializeFractals, initializeFeedback
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
import numpy as np

def digitSpanTask(experimentStructure, stimuliStructure, globalClock, filename, myGoal, backward, dspanCond):
    """ This function implements a digit-span task
    
        Input:
            experimentStructure: all general experimental properties 
            stimuliStructure: all general stimulus properties
            globalClock: clock to control timing during fMRI
            filename: not used anymore
            myGoal: indicates how many digits have to be remembered in current trial
            backward: indicates if forward or backward condition is used
            dspanCond: condition string for data logging
        
        Return:
            routineTimer:  timer to control presentation times
            globalClock: clock to control timing during fMRI
            fixCrossTiming: actual presentation time of fixation cross during digit span phase
            corrRep: indicats if correct responses have been given
    
    """
    
    # Create some shortnames
    expInfo         = experimentStructure['expInfo']
    thisExp         = experimentStructure['thisExp']
    win             = experimentStructure['win']
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
    
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)

    myD     = 0
    corrRep = []
    while True: 
        blockIndex = 'blockFiles/digit-span/digit-span.xlsx'
        routineTimer    = core.CountdownTimer()
        (feedbackClock, feedbackText)  = initializeFeedback(win, expInfo)
        text = feedbackText
        
        # Set up handler to look after randomisation of conditions etc
        N_Back = data.TrialHandler(nReps = 1, method = 'random', 
            extraInfo = None, originPath = -1,
            trialList = data.importConditions(blockIndex),
            seed = None, autoLog = False) 
            
        thisTrial = N_Back.trialList[0]  # so we can initialise stimuli with some values
        if thisTrial != None:
                for paramName in thisTrial.keys():
                    exec(paramName + '= thisTrial.' + paramName)

        myCount         = 0
        presentedDigits = []
        while True: 
         
            thisTrial = N_Back.next()
            
            # Abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
            if thisTrial != None:
                for paramName in thisTrial.keys():
                    exec(paramName + '= thisTrial.' + paramName)
         
            presentedDigits.append(thisTrial.stim)
            
            (N_Back, decision1, thisExp, thisTrial, miss) = runDigitSpan(experimentStructure, stimuliStructure, globalClock, filename, routineTimer, text, stim, N_Back,thisExp, thisTrial)

            myCount = myCount + 1
            if (myCount) == myGoal:
                break
            
        endExpNow = False  # flag for 'escape' or other condition => quit the exp

        # Initialize components for Routine "trial"
        trialClock = core.Clock()
        if backward == False:
            Question = visual.TextStim(win=win, name='Question',
                text='Welche Zahlen wurden angezeigt (vorwärts)?',
                font='Arial',
                pos=[0, 0.6], height=0.1, wrapWidth=1.5, ori=0, 
                color='white', colorSpace='rgb', opacity=1,
                depth=0.0, units = 'norm');
        elif backward == True:
            Question = visual.TextStim(win=win, name='Question',
                text='Welche Zahlen wurden angezeigt (rückwärts)?',
                font='Arial',
                pos=[0, 0.6], height=0.1, wrapWidth=1.5, ori=0, 
                color='white', colorSpace='rgb', opacity=1,
                depth=0.0, units = 'norm');
            
        AnswerDisplay = visual.TextStim(win=win, name='AnswerDisplay',
            text='default text',
            font='Arial',
            pos=[0, 0], height=0.1, wrapWidth=None, ori=0, 
            color=[-1.000,-1.000,-1.000], colorSpace='rgb', opacity=1,
            depth=-3.0, units = 'norm');

        # Create some handy timers
        globalClock = core.Clock()  # to track the time since experiment started
        routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

        # Set up handler to look after randomisation of conditions etc
        trials = data.TrialHandler(nReps=1, method='random', 
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='trials')
        thisExp.addLoop(trials)  # add the loop to the experiment
        thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
        
        # Abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial.keys():
                exec(paramName + '= thisTrial.' + paramName)

        for thisTrial in trials:
            currentLoop = trials
            
            # Abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
            if thisTrial != None:
                for paramName in thisTrial.keys():
                    exec(paramName + '= thisTrial.' + paramName)
            
            # ------Prepare to start Routine "trial"-------
            t = 0
            trialClock.reset()  # clock
            frameN = -1
            continueRoutine = True
            # Update component parameters for each repeat
            AnswerFinished = event.BuilderKeyResponse()
            RecordAnswer = event.BuilderKeyResponse()
            AnswerDisplay.setText(RecordAnswer.keys)
            
            # Keep track of which components have finished
            trialComponents = [Question, AnswerFinished, RecordAnswer, AnswerDisplay]
            for thisComponent in trialComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            
            # -------Start Routine "trial"-------
            while continueRoutine:
                # get current time
                t = trialClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # Update/draw components on each frame
                
                # *Question* updates
                if t >= 0.0 and Question.status == NOT_STARTED:
                    # Keep track of start time/frame for later
                    Question.tStart = t
                    Question.frameNStart = frameN  # exact frame index
                    Question.setAutoDraw(True)
                
                # *AnswerFinished* updates
                if t >= 0.0 and AnswerFinished.status == NOT_STARTED:
                    # Keep track of start time/frame for later
                    AnswerFinished.tStart = t
                    AnswerFinished.frameNStart = frameN  # exact frame index
                    AnswerFinished.status = STARTED
                    # Keyboard checking is just starting
                    win.callOnFlip(AnswerFinished.clock.reset)  # t=0 on next screen flip
                    event.clearEvents(eventType='keyboard')
                if AnswerFinished.status == STARTED:
                    theseKeys = event.getKeys(keyList=['return'])
                    
                    # check for quit:
                    if "escape" in theseKeys:
                        endExpNow = True
                    if len(theseKeys) > 0:  # at least one key was pressed
                        AnswerFinished.keys = theseKeys[-1]  # just the last key pressed
                        AnswerFinished.rt = AnswerFinished.clock.getTime()
                        # a response ends the routine
                        continueRoutine = False
                
                # *RecordAnswer* updates
                if t >= 0.0 and RecordAnswer.status == NOT_STARTED:
                    # Keep track of start time/frame for later
                    RecordAnswer.tStart = t
                    RecordAnswer.frameNStart = frameN  # exact frame index
                    RecordAnswer.status = STARTED
                    # Keyboard checking is just starting
                    win.callOnFlip(RecordAnswer.clock.reset)  # t=0 on next screen flip
                    event.clearEvents(eventType='keyboard')
                if RecordAnswer.status == STARTED:
                    theseKeys = event.getKeys(keyList=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
                    
                    # check for quit:
                    if "escape" in theseKeys:
                        endExpNow = True
                    if len(theseKeys) > 0:  # at least one key was pressed
                        RecordAnswer.keys.extend(theseKeys)  # storing all keys
                        RecordAnswer.rt.append(RecordAnswer.clock.getTime())
                
                # *AnswerDisplay* updates
                if t >= 0.0 and AnswerDisplay.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    AnswerDisplay.tStart = t
                    AnswerDisplay.frameNStart = frameN  # exact frame index
                    AnswerDisplay.setAutoDraw(True)
                displaystring=" ".join(RecordAnswer.keys) #convert list of pressed keys to string
                displaystring=displaystring.replace(' ','') #remove intermediate spaces
                
                # Do some text cleanup...replacing key names with puntuation and effectively disabling keys like 'back','shift', etc.
                displaystring=displaystring.replace('space',' ') 
                displaystring=displaystring.replace('comma',',')
                displaystring=displaystring.replace('lshift','')
                displaystring=displaystring.replace('rshift','')
                displaystring=displaystring.replace('period','.')
                displaystring=displaystring.replace('back','')
                
                # Set text of AnswerDisplay to modified string
                AnswerDisplay.setText(displaystring)
                
                # Check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in trialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # Check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # Check for delete
                if endExpNow or event.getKeys(keyList=["backspace"]):
                    if len(RecordAnswer.keys) > 0:
                        RecordAnswer.keys.pop(-1)
                    
                # Refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "trial"-------
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            
            # Check response
            if len(presentedDigits) == len(RecordAnswer.keys):
                new_list = []
                for i in range (0,len(presentedDigits)):
                    if backward == False:
                        if str(presentedDigits[i]) == RecordAnswer.keys[i]:
                            new_list.append(1)
                    elif backward == True:
                        
                        if str(presentedDigits[-i-1]) == RecordAnswer.keys[i]:
                            new_list.append(1)
                        
                if sum(new_list) == len(presentedDigits):
                    corrRep.append(1)
                    
            # Check responses
            if AnswerFinished.keys in ['', [], None]:  # No response was made
                AnswerFinished.keys=None
            trials.addData('AnswerFinished.keys',AnswerFinished.keys)
            if AnswerFinished.keys != None:  # we had a response
                trials.addData('AnswerFinished.rt', AnswerFinished.rt)
            
            # Check responses
            if RecordAnswer.keys in ['', [], None]:  # No response was made
                RecordAnswer.keys=None
            trials.addData('RecordAnswer.keys',RecordAnswer.keys)
            if RecordAnswer.keys != None:  # we had a response
                trials.addData('RecordAnswer.rt', RecordAnswer.rt)
            trials.addData('RecordAnswer.keys',displaystring)
            trials.addData('corrRep', corrRep)
            trials.addData('dspanCond', dspanCond)
            trials.addData('dspan', myGoal-1)
            trials.addData('stim', presentedDigits)

            # The Routine "trial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # Start next trial
            thisExp.nextEntry()
        
        # Update digit span estimate
        myD = myD + 1
        if (myD) == 2:
            break
    
    return(routineTimer, globalClock, fixCrossTiming, corrRep)