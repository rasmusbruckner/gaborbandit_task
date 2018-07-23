# -*- coding: utf-8 -*-


from numpy.random import shuffle
from simpleInstructions import simpleInstructions 
from runTask import runTask 


def taskLoop(set, nBlocks, whichVersion, globalClock, experimentStructure, outcomeStructure, stimuliStructure, data,
feedbackText, nTrials, tracker, blockList, expInfo, conditionName, targetWord):
    """ This function implements the blocks of the Gabor-bandit task
    
    If used with fMRI, block waits until initial trigger is received.
    
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
        tracker: eye-tracker object instance
        blockList: list of all blocks for set of blocks of current participant
        expInfo: structure with background information about experiment
        conditionName: name of current condition
        targetWord: displayed word that indicates if high or low patch should be identified
    
    Return:
        sum(accPerf): total performance
        totalReward: obtained reward 
    
    """
    
    whichLoop = conditionName
    accPerf = []
    
    # Start task
    for x in range (0, nBlocks):
        
        # Wait for fMRI signal and sync with globalClock
        if whichVersion == 2:
            
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
        
        blockIndex = blockList[x]
        print blockIndex
        
        # Start actual task block
        (y,win) = runTask(experimentStructure, outcomeStructure, stimuliStructure,
        data, feedbackText, nTrials, whichLoop, blockIndex, x, conditionName, globalClock, tracker)
        
        accPerf.append(y)
        
        if x < nBlocks-1:
            header = 'Block %1.0f von %1.0f' %(x+1,nBlocks)
            mainText = ("""In diesem Block hast Du %1.0f Punkte gesammelt!\n\n"""
            """Du fängst jetzt mit einem neuen Block """
            """an und musst den Zusammenhang zwischen der Seite des %sn Bildes und des Musters wieder neu lernen. Weiter mit Enter.""" %(accPerf[x], targetWord))
        else:
            header = 'Ende der Aufgabe'
            mainText =  "Insgesamt hast du %1.0f Punkte gesammelt!" %(sum(accPerf))
        
        simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])
        
    
    print('Points for subject %s in %s: %s ' %(expInfo['participant'], conditionName, sum(accPerf)))
    
    # Compute reward: difference between collected points and chance-level 
    # divided by 10 that 1 point above chance is worth 7.5 Cent
    y = sum(accPerf)
    totalReward = (y - ((nTrials*nBlocks)/2))/15
    
    print('Reward for subject %s in %s: %s Euros' %(expInfo['participant'], conditionName, totalReward))
    
    return(sum(accPerf), totalReward)