# -*- coding: utf-8 -*-

from psychopy import visual, event, parallel
import os
from numpy.random import shuffle
from simpleInstructions import simpleInstructions 
from runTask import runTask 
import pylink
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy


def taskLoop(set, nBlocks, whichVersion, globalClock, experimentStructure, outcomeStructure, stimuliStructure, data,
feedbackText, nTrials, blockList, expInfo, conditionName, targetWord):
    """ This function implements the blocks of the Gabor-bandit task
    
    If used with fMRI, task block starts only when initial trigger is received.
    
    Input:
        set: Participant specific outcome set (here not in use anymore)
        nBlocks: number of blocks
        whichVersion: indicates if practice or main task version
        globalClock: clock to control timing during fMRI
        experimentStructure: all general experimental properties 
        outcomeStructure: all general stimulus properties
        stimuliStructure: all general stimulus properties
        data: PsychoPy data functions
        feedbackText: feedback text object instance
        nTrials: number of trials
        blockList: list of all blocks for set of blocks of current participant
        expInfo: structure with background information about experiment
        conditionName: name of current condition
        targetWord: displayed word that indicates if high or low patch should be identified
    
    Return:
        sum(accPerf): total performance
        totalReward: obtained reward 
    
    """
    
    #  Extract variables
    whichLoop = conditionName
    accPerf = []
    expInfo = experimentStructure['expInfo']
    session = expInfo['session']
    block_start = experimentStructure['block_start']
    useEyeTracker = experimentStructure['useEyeTracker']
    et_dummy = experimentStructure['et_dummy']
    win = experimentStructure['win']
    scr_wdt = experimentStructure['scr_wdt']
    scr_hght = experimentStructure['scr_hght']
    scanner_dummy = experimentStructure['scanner_dummy']
    if whichVersion == 1:
        block_end = nBlocks
    elif whichVersion == 2:
        block_end = block_start + 1

    # Start task
    for x in range (block_start, block_end):
        
        # Create eyetracker object and calibrate
        # --------------------------------------
        if useEyeTracker:
            
            # Eyetracking file name
            et_filename = '%s_%s' %(expInfo['participant'], x) +'.EDF'
            print(et_filename)
            
            # Create eyetracker object
            if not et_dummy:
                eyeTracker = pylink.EyeLink()
            else:
                eyeTracker = pylink.EyeLink(None)
            
            # Create eytracking data file
            eyeTracker.openDataFile(et_filename)
            
            # Add file preamble to data file
            eyeTracker.sendCommand('add_file_preamble_text = Gabor')
            
            # Stop for a moment to ensure the file is open and ready to receive data
            pylink.msecDelay(50)
            
            # Initialize the graphics for calibration/validation
            genv = EyeLinkCoreGraphicsPsychoPy(eyeTracker, win)
            pylink.openGraphicsEx(genv)

            # Eyetracker setup
            # ----------------

            # Determine ET mode
            eyeTracker.setOfflineMode()

            # Sampling rate
            eyeTracker.sendCommand('sample_rate 500')

            # 0-> standard, 1-> sensitive [Manual: section ??]
            eyeTracker.sendCommand('select_parser_configuration 0')

            # Make sure the tracker knows the physical resolution of the subject display
            eyeTracker.sendCommand("screen_pixel_coords = 0 0 %d %d" % (scr_wdt-1, scr_hght-1))
            #scr_wdt, scr_hght

            # Stamp display resolution in EDF data file for Eyelink Data Viewer integration
            eyeTracker.sendMessage("DISPLAY_COORDS = 0 0 %d %d" % (scr_wdt-1, scr_hght-1))

            # Set the tracker to record Event Data in "GAZE" (or "HREF") coordinates
            eyeTracker.sendCommand("recording_parse_type = GAZE")

            # Here we show how to use the "setXXXX" command to control the tracker, see the "EyeLink" section of the pylink manual.
            # specify the calibration type, H3, HV3, HV5, HV13 (HV = horiztonal/vertical)
            eyeTracker.sendCommand("calibration_type = HV9")

            # Allow buttons on the gamepad to accept calibration/dirft check target
            eyeTracker.sendCommand("button_function 1 'accept_target_fixation'")
            eyeTracker.sendCommand("calibration_area_proportion  0.88 0.83") # proportion of the screen to calibrate
            eyeTracker.sendCommand("validation_area_proportion  0.88 0.83") # proportion of the screen to validata

            # Check tracker version and set parameters accordingly
            eyelink_ver = eyeTracker.getTrackerVersion()

            if eyelink_ver >=3:
                # Establish link and file contents (code for EyeLink 1000 and 1000 plus)
                # This is the version we're using. Other cases not tested!
                eyeTracker.sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT")
                eyeTracker.sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON,INPUT")
                eyeTracker.sendCommand("file_sample_data = LEFT,RIGHT,GAZE,GAZERES,AREA,HREF,PUPIL,STATUS,INPUT,HTARGET")
                eyeTracker.sendCommand("link_sample_data = LEFT,RIGHT,GAZE,GAZERES,AREA,HREF,PUPIL,STATUS,INPUT,HTARGET")
            else:
                    
                # Establish link and file contents (code for EyeLink II)
                eyeTracker.sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT")
                eyeTracker.sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON,INPUT")
                eyeTracker.sendCommand("file_sample_data = LEFT,RIGHT,GAZE,GAZERES,AREA,HREF,PUPIL,STATUS,INPUT")
                eyeTracker.sendCommand("link_sample_data = LEFT,RIGHT,GAZE,GAZERES,AREA,HREF,PUPIL,STATUS,INPUT")
             
            # Calibrate the camera
            calInstruct = visual.TextStim(win, text='Press any key to go to EyeLink camera setup mode.', color='white')
            calInstruct.draw()
            win.flip()
            event.waitKeys()
            eyeTracker.doTrackerSetup()
        else:
            eyeTracker = 0
        
        # Wait for fMRI signal and sync with globalClock
        if whichVersion == 2 and scanner_dummy == False:
            
            port = parallel.ParallelPort(address=0x0378)
            
            dummy = visual.TextStim(win, text='Warte auf MRT Signal...', units='pix')
            
            while 1:
                dummy.draw()
                win.flip()
                dat = port.readPin(10)
                if dat == 1:
                    globalClock.reset()
                    break
                
                # check for quit:
                if event.getKeys(keyList=["escape"]):
                        core.quit()
            print('triggered')
        else:
            globalClock.reset()  # sync with trigger time
        
        if not session == 4:
            blockIndex = blockList[x]
        else:
            blockIndex = blockList[0]
        #print blockIndex
        
        # Start actual task block
        (y, win) = runTask(experimentStructure, outcomeStructure, stimuliStructure,
        data, feedbackText, nTrials, whichLoop, blockIndex, x, conditionName, globalClock, eyeTracker)
        
        # Deactivate eyetracker
        if useEyeTracker:

            # Close EDF data File
            eyeTracker.closeDataFile()

            # Currently commented out because automatic transfer takes quite long
            # EyeLink - copy EDF file to Display PC and put it in the 'edfData' folder
            #edfTransfer = visual.TextStim(win, text='Gaze data is transfering from EyeLink Host PC, please wait...', color='white')
            #edfTransfer.draw()
            #eyeTracker.receiveDataFile(et_filename, os.path.join(os.getcwd(), 'data', 'eyetracking_data', et_filename))

            # EyeLink - Close connection to tracker
            eyeTracker.close()
        
        # runTask output
        accPerf.append(y)
        
        if not session == 4:
            if x < block_end: 
                header = 'Block %1.0f von %1.0f' %(x+1,nBlocks)
                if whichVersion == 1:
                    mainText = ("""In diesem Block hast du %1.0f Punkte gesammelt!\n\n"""
                    """Du fängst jetzt mit einem neuen Block """
                    """an und musst den Zusammenhang zwischen der Seite des %sn Bildes und des Musters wieder neu lernen. Weiter mit Enter.""" %(accPerf[0], targetWord))
                else:
                    mainText = ("""In diesem Block hast du %1.0f Punkte gesammelt!\n\n"""
                    """Du fängst gleich mit einem neuen Block """
                    """an und musst den Zusammenhang zwischen der Seite des %sn Bildes und des Musters wieder neu lernen.""" %(accPerf[0], targetWord))
            else:
                header = 'Ende der Aufgabe'
                mainText =  "Insgesamt hast du %1.0f Punkte gesammelt!" %(sum(accPerf))
        
            simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])
    
    print('----------')
    
    # Compute reward: difference between collected points and chance-level 
    # divided by 15 that 1 point above chance is worth XX Cent
    if whichVersion == 1:
        y = sum(accPerf)
        totalReward = (y - ((nTrials*nBlocks)/2))/15
        print('Reward for subject %s in %s: %s Euros' %(expInfo['participant'], conditionName, totalReward))
    else: 
        totalReward = float('nan')
    
    return(sum(accPerf), totalReward)
