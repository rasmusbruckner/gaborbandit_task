# -*- coding: utf-8 -*-

"""
Gabor-Bandit Task

Master script where all variables can be controlled
The task is incentive compatible. Obtained reward 
is proportional to the difference between collected
points and chance performance. 
Includes digit-span task to measure working memory 
capacity.

Written by RB. Version 07/2017
"""

from __future__ import division
from psychopy import visual, core, data, event, logging, sound, gui
from psychopy.constants import *
from psychopy import parallel
import numpy as np
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os
import glob
import random
from initializeComponents import initializeFixationCross, initializeQuestProcedure, initializePatches
from initializeComponents import initializeFractals, initializeFeedback
from simpleInstructions import simpleInstructions 
from patchesExample import patchesExample 
from runPatches import runPatches
from runQuest import runQuest 
from fractalsExample import fractalsExample 
from taskLoop import taskLoop
from runTask import runTask 
from digitSpanTask import digitSpanTask
from psychopy.hardware.emulator import launchScan
import sys  
import matplotlib
matplotlib.use('Qt4Agg')
import pylab
reload(sys)  
sys.setdefaultencoding('utf8')

# Set variables
# -------------

ID                  = u'999'       # participant's ID (use numbers)
set                 = 1            # predefined dataset
whichVersion        = 1            # 1 = behavioral; 2 = fMRI
session             = 1            # 1 = practice; 2 = main condition; 3 = digit-span
nTrials             = 25           # For testing this has to be equal to the number of trials in the .xlsx file!
nBlocksSafe         = 6            # 6 blocks
nBlocksUnc          = 12           # 12 blocks
nTrialsPatches      = 100          # patch main and other practice: 100
nTrialsPatchesPract = 50           # patch practice with feedback: 50
reward              = 1            # number of points if rewarded
noReward            = 0            # number of points if not rewarded
cBal                = u'1'         # 1 = high contrast patch, 2 = low contrast patch
winFeedback         = "+ 1 Punkt" 
neutralFeedback     = "+ 0 Punkte"
useEyeTracker       = False

# Control timing
if whichVersion == 1:
    if session == 1 or session == 2:
        fixCrossTiming  = 0.9
        jitter          = 0.2
        stimulusTiming  = 1.00
    elif session == 3:
        fixCrossTiming  = 0.9
        jitter          = 0.20
        stimulusTiming  = 1.00
elif whichVersion == 2:
    fixCrossTiming  = 4
    jitter          = 2
    stimulusTiming  = 1.00

# Set directory
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Names, info and folders
# ------------------------
expName = 'GB'
expInfo = {u'participant': ID}
if session == 1:
    folder = 'training'
elif session == 2:
    folder = 'main'
elif session == 3:
    folder = 'main'

expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName
expInfo['session'] = session
expInfo['cBal'] = cBal

if whichVersion == 1:
    versionString = 'behav'
elif whichVersion == 2:
    versionString = 'fMRI'

if session == 1 or session == 2:
    filename = _thisDir + os.sep + 'data/%s/%s_%s_cBal%s_%s_%s' %(folder, expName, versionString, cBal, expInfo['participant'],expInfo['date'])
elif session == 3:
    filename = _thisDir + os.sep + 'data/%s_dspan/dspan_%s_%s' %(expName,expInfo['participant'],expInfo['date'])

# Initialize experiment handler
thisExp = data.ExperimentHandler(name = expName, version = '',
    extraInfo = expInfo, runtimeInfo = None,
    originPath = None,
    savePickle = True, saveWideText = True,autoLog = False,
    dataFileName = filename)  

# Initialize window object
win = visual.Window(size=(1280, 1024), monitor='testMonitor', fullscr=True, units='deg', colorSpace='rgb')

# Initialize option to quit experiment using esc-key
endExpNow = False

# Create eyetracker object and calibrate
# --------------------------------------
if useEyeTracker:
    tracker = eyetracker.EyeTracker(win, eyedatafile='eyetracking_log')
    tracker.calibrate()
    tracker.start_recording()
else:
    tracker = 0

# Frame rate
expInfo['frameRate'] = win.getActualFrameRate()
print('frame rate: %f' %(expInfo['frameRate']))
if expInfo['frameRate'] != None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0
win._refreshThreshold = frameDur+0.004 # we want to allow 4ms tolerance

# Set the log module to report warnings to the std output window (default is errors only)
logging.console.setLevel(logging.WARNING)

# Initialize components
(fixationCross) = initializeFixationCross(win)
(questClock) = initializeQuestProcedure(win)
(patchClock, patch1, patch2) = initializePatches(win, expInfo)
(fractalClock, fractal1, fractal2) = initializeFractals(win, expInfo)
(feedbackClock, feedbackText) = initializeFeedback(win, expInfo)

# Imaging clock: will be reset in response to first fMRI impulse
globalClock = core.Clock()

# Create some useful structures 
# -----------------------------
experimentStructure = {'expInfo': expInfo, 'thisExp': thisExp,
'globalClock': globalClock, 'NOT_STARTED': NOT_STARTED, 'STARTED': STARTED, 'FINISHED': FINISHED,
'STOPPED': STOPPED,'endExpNow': endExpNow, 'event': event, 'win': win, 'whichVersion': whichVersion,
'useEyeTracker': useEyeTracker}

outcomeStructure = {'reward': reward, 'noReward': noReward, 'winFeedback': winFeedback,
'neutralFeedback': neutralFeedback}

stimuliStructure = {'patch1': patch1, 'patch2': patch2, 'fractal1': fractal1, 'fractal2': fractal2,
'fixationCross': fixationCross, 'fixCrossTiming': fixCrossTiming, 'jitter': jitter,
'stimulusTiming': stimulusTiming, 'questClock': questClock, 'patchClock': patchClock,
'fractalClock': fractalClock, 'feedbackClock': feedbackClock}

# Instructions
# -------------
if expInfo['cBal'] == '1':
    targetWord = 'kontrastreiche'
elif expInfo['cBal'] == '2':
    targetWord = 'kontrastarme'

if expInfo['cBal'] == '1':
    targetWord2 = 'kontrastreiche'
elif expInfo['cBal'] == '2':
    targetWord2 = 'kontrastärme'

if session == 1:
    
    # Indicate that the following sessions belong to the training blocks 
    conditionName = 'training'
    
    header = 'Herzlich Willkommen'
    mainText = 'Studie zum Thema Lernen und Entscheiden'
    
    simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])
    
    if expInfo['cBal'] == '1':
        positionPatch1 = [-6, 0]
        positionPatch2 = [6, 0]
    elif expInfo['cBal'] == '2':
        positionPatch1 = [6, 0]
        positionPatch2 = [-6, 0]
    
    corrAns = 'return'
    exampleText = ("""Deine Aufgabe ist es zu entscheiden, welches der beiden Bilder %sr ist. """
    """Wenn z.B. das linke Bild %sr ist, drückst Du die linke Pfeiltaste. """ %(targetWord2, targetWord2))
    patchesExample(experimentStructure, exampleText, positionPatch1, positionPatch2, corrAns)
    
    header = '1. Übung'
    mainText = ("""In dieser Übung sollst Du wie im Beispiel angeben, welches Bild %sr """
    """ist. Nutze dafür die Pfeiltasten (rechts und links).\n\n"""
    """Während der Übung bekommst Du Feedback, ob Deine Antwort richtig oder falsch war. Mit Enter startest Du die Übung.""" %(targetWord2))
    simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])
    
    whichLoop = 'patches'
    blockIndex = """blockFiles/set_%d/pract_PD/GB_runPatches1.xlsx""" %(set)
    showFeedback = 1
    accPerf = runPatches(experimentStructure, stimuliStructure, data, feedbackText, patchClock,
    whichLoop, conditionName, showFeedback, nTrialsPatchesPract, blockIndex, globalClock, tracker)
    
    header = 'Ende der Übung'
    mainText = ("""In diesem Block hast Du %1.0f Mal richtig geantwortet!""" %(accPerf))
    simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])
    
    header = '2. Übung'
    mainText = ("""In dieser Übung sollst Du wieder entscheiden, welches Bild %sr ist. """
    """Diesmal bekommst Du allerdings kein Feedback zu Deiner Antwort.""" %(targetWord2))
    simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])
    
    whichLoop = 'patches'
    blockIndex = """blockFiles/set_%1d/pract_PD/GB_runPatches2.xlsx""" %(set)    
    showFeedback = 0
    accPerf = runPatches(experimentStructure, stimuliStructure, data, feedbackText, patchClock,
    whichLoop, conditionName, showFeedback, nTrialsPatches, blockIndex, globalClock, tracker)
    
    header = 'Ende der Übung'
    mainText = ("""In diesem Block hast Du %1.0f Mal richtig geantwortet!""" %(accPerf))
    simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])
    
    corrAns = 'return'
    mainText = """Jetzt kommen zwei Muster hinzu. Im nächsten Schritt wird Dir die Rolle dieser Muster erklärt."""
    fractalsExample(experimentStructure, mainText, corrAns)
    
    header = ' '
    mainText = ("""Ab jetzt sollst Du versuchen, Deinen Gewinn in der Aufgabe zu maximieren:\n\n"""
    """Es gibt zwei mögliche Kopplungen zwischen der Position des %sn Bildes (rechts und links) und den zwei Mustern (rot oder blau). """ 
    """Das Ziel ist es herauszufinden, gegeben der Position des %sn Bildes, welches Muster Du wählen solltest, um wahrscheinlich eine Belohnung zu erhalten. """
    """Diese Kopplung lernst Du durch Feedback nach der Antwort (%s).\n\nDeine so verdienten """
    """Punkte bekommst Du am Ende, in Geld umgerechnet, ausgezahlt.""" %(targetWord, targetWord, winFeedback))
    simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])
    
    corrAns = 'left'
    exampleText = ("""Gib jetzt an, welches der beiden Bilder %sr ist. Da in diesem Fall das linke """
    """Bild %sr ist, drückst Du die linke Pfeiltaste.""" %(targetWord2, targetWord2))
    patchesExample(experimentStructure, exampleText, positionPatch1, positionPatch2, corrAns)
    
    header = ' '
    mainText = ("""Du hast Dich in diesem Beispiel entschieden, dass das Bild links %sr war. """
    """Im folgenden Schritt versuchst Du herauszufinden, welches Muster bei "%ss Bild links" """
    """häufiger eine Belohnung gibt.\n\nBeachte, dass beide Muster mit einer """
    """bestimmten Häufigkeit zu einer Belohnung (%s) führen, aber eines öfter zu """
    """einer Belohnung führt und somit die bessere Antwort ist.""" %(targetWord2, targetWord, winFeedback))
    simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])
    
    corrAns = 'up'
    mainText = """In diesem Fall ist das rote Muster die bessere Antwort. Drücke daher die obere Pfeiltaste."""
    fractalsExample(experimentStructure, mainText, corrAns)
    
    header = ("""Wenn Du das richtige Muster auswählst, erhältst Du in den meisten Fällen eine Belohnung. """
    """Beachte, dass Du manchmal trotz der besseren Antwort keine Belohnung erhälst.\n"""
    """Beachte außerdem, dass Du manchmal auch bei der schlechteren Antwort eine Belohnung erhälst.""")
    mainText = winFeedback
    simpleInstructions(experimentStructure, header, 0.08, [0, 0.6], mainText, 0.1, [0, 0.0])
    
    header = ' '
    mainText = ("""Wenn sich das %s Bild auf der anderen Seite befindet, wählst Du auch das andere Muster.\n\n"""
    """Das heißt: Wenn Du bei "%ss Bild links" am besten das rote Muster wählst, so nimmst Du bei "%ss """
    """Bild rechts" am besten das blaue Muster.\n\nWir schauen uns hiervon jetzt ein Beispiel an.""" %(targetWord, targetWord, targetWord))
    simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])
    
    if expInfo['cBal'] == '1':
        positionPatch1 = [6, 0]
        positionPatch2 = [-6, 0]
    elif expInfo['cBal'] == '2':
        positionPatch1 = [-6, 0]
        positionPatch2 = [6, 0]
        
    corrAns = 'right'
    exampleText = ("""Jetzt ist das rechte Bild %sr. Drücke daher die rechte Pfeiltaste.""" %(targetWord2))
    patchesExample(experimentStructure, exampleText, positionPatch1, positionPatch2, corrAns)
    
    corrAns = 'down'
    mainText = ("""Weil das %s Bild auf der anderen Seite war, ist jetzt das blaue Muster besser. """
    """Drücke daher die untere Pfeiltaste.""" %(targetWord))
    fractalsExample(experimentStructure, mainText, corrAns)

    header = ("""Daraufhin siehst Du wieder ob du eine Belohnung erhalten hast.""")
    mainText = winFeedback
    simpleInstructions(experimentStructure, header, 0.08, [0, 0.6], mainText, 0.1, [0, 0.0])
    
    header = ' '
    mainText = ("""Innerhalb eines Blocks bleiben die Belohnungshäufigkeiten stabil. Das heißt, wenn """
    """Du einmal herausgefunden hast, wann Du am besten welches Muster wählst, bleibt dies bis zum nächsten Block konstant.""")
    simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])    
    
    header = '3. Übung'
    mainText = ("""In dieser Übung sollst Du jetzt selber herausfinden mit """
    """welchem Muster das %s Bild zusammenhängt, so dass Du möglichst viele Punkte verdienst.""" %(targetWord))
    simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])
    
    whichLoop = 'practice2'
    blockIndex = """blockFiles/set_%d/pract_safe/rightBlue/GB_RB_1.xlsx""" %(set)
    (accPerf, win) = runTask(experimentStructure, outcomeStructure, stimuliStructure,
    data, feedbackText, nTrials, whichLoop, blockIndex, 1, conditionName, globalClock, tracker)
    
    header = ' '
    mainText = ("""In diesem Block hast Du %1.0f Punkte gesammelt!\n\n"""
    """Du fängst jetzt mit einem neuen Block """
    """an und musst den Zusammenhang zwischen der Seite des %sn Bildes und des Musters wieder neu lernen.""" %(accPerf, targetWord))
    simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])
    
    whichLoop = 'practice3'
    blockIndex = """blockFiles/set_%d/pract_safe/leftBlue/GB_LB_1.xlsx""" %(set)
    (accPerf, win) = runTask(experimentStructure, outcomeStructure, stimuliStructure,
    data, feedbackText, nTrials, whichLoop, blockIndex, 2, conditionName, globalClock, tracker)
    header = ' '
    
    header = 'Ende der Übung'
    mainText = ("""In diesem Block hast Du %1.0f Punkte gesammelt!\n\n""" %(accPerf))
    simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])
    
    header = '4. Übung'
    mainText = ("""Diese Übung ist die letzte Übung bevor der Versuch startet. Du hast genau die gleiche """
    """Aufgabe wie in der letzten Übung, allerdings sind die Bilder in der ersten Stufe schwieriger von einander zu unterscheiden.""")
    simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])
    
    whichLoop = 'practice4'
    blockIndex = """blockFiles/set_%d/pract_unc/leftBlue/GB_LB_1.xlsx""" %(set)
    (accPerf, win) = runTask(experimentStructure, outcomeStructure, stimuliStructure,
    data, feedbackText, nTrials, whichLoop, blockIndex, 2, conditionName, globalClock, tracker)
    
    header = ' '
    mainText = ("""In diesem Block hast Du %1.0f Punkte gesammelt!\n\n"""
    """Du fängst jetzt mit einem neuen Block """
    """an und musst den Zusammenhang zwischen der Seite des %sn Bildes und des Musters wieder neu lernen.""" %(accPerf, targetWord))
    simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])
    
    whichLoop = 'practice5'
    blockIndex = """blockFiles/set_%d/pract_unc/rightBlue/GB_RB_1.xlsx""" %(set)
    (accPerf, win) = runTask(experimentStructure, outcomeStructure, stimuliStructure,
    data, feedbackText, nTrials, whichLoop, blockIndex, 3, conditionName, globalClock, tracker)
    
    header = 'Ende der Übung'
    mainText = ("""In diesem Block hast Du %1.0f Punkte gesammelt!\n\n""" %(accPerf))
    simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])
    
    header = ' '
    mainText = """Du hast den Übungsteil jetzt abgeschlossen. Wende Dich bitte an den Versuchsleiter."""
    simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])
    
elif session == 2:
    
    # Main task
    #----------
    
    # First part: "economic decision making"
    leftBlue  = glob.glob('blockFiles/set_%1.0f/main_safe/leftBlue/*.xlsx' %(set))
    rightBlue = glob.glob('blockFiles/set_%1.0f/main_safe/rightBlue/*.xlsx' %(set))
    blockList = (leftBlue + rightBlue)
    shuffle(blockList)
    print(blockList)    
    
    header = 'Entscheidungsaufgabe Teil 1'
    mainText = ("""Ab jetzt erhälst Du Punkte für Deine Entscheidungen. Die Punkte werden am Ende des Experiments in Geld umgerechnet. """
    """Du fängst mit %1.0f Blöcken an, in denen Du den Kontrast der Bilder einfach unterscheiden kannst. """ %(nBlocksSafe))
    simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])
    
    conditionName = 'main_safe'
    nBlocks = nBlocksSafe
    (score1, rew1) = taskLoop(set, nBlocks, whichVersion, globalClock, experimentStructure, outcomeStructure, stimuliStructure, data,
    feedbackText, nTrials, tracker, blockList, expInfo, conditionName, targetWord)
    
    # Second part: "perceptual decision making"
    header = 'Kontrastentscheidungen'
    mainText = ("""In dieser Aufgabe siehst Du ausschließlich die Bilder aus der Entscheidungsaufgabe. Wie in der Übung am Anfang, sollst Du angeben, """
    """welches Bild %sr ist.""" %(targetWord2))
    simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])
    
    whichLoop = 'patches'
    blockIndex = """blockFiles/set_%d/main_PD/GB_runPatches1.xlsx""" %(set)
    showFeedback = 0
    accPerf = runPatches(experimentStructure, stimuliStructure, data, feedbackText, patchClock,
    whichLoop, conditionName, showFeedback, nTrialsPatches, blockIndex, globalClock, tracker)
    
    header = 'Ende Kontrastentscheidungen'
    mainText = ("""In diesem Block hast Du %1.0f Mal richtig geantwortet!""" %(accPerf))
    simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])
    
    # Third part: "economic decision making under perceptual uncertainty"
    header = 'Entscheidungsaufgabe Teil 2'
    mainText = ("""Jetzt kommt der zweite Teil der Entscheidungsaufgabe. Du sollst wieder probieren, möglichst viele Punkte zu verdienen. """
    """Dabei kannst Du die Kontraste manchmal nur schwer von einander unterscheiden. Insgesamt durchläufst Du %1.0f Blöcke.""" %(nBlocksUnc))
    simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])
    
    leftBlue  = glob.glob('blockFiles/set_%1.0f/main_unc/leftBlue/*.xlsx' %(set))
    rightBlue = glob.glob('blockFiles/set_%1.0f/main_unc/rightBlue/*.xlsx' %(set))
    blockList = (leftBlue + rightBlue)
    shuffle(blockList)
    print(blockList)
    
    conditionName = 'main_unc'
    nBlocks = nBlocksUnc
    (score2, rew2) = taskLoop(set,nBlocks, whichVersion, globalClock, experimentStructure, outcomeStructure, stimuliStructure, data,
    feedbackText, nTrials, tracker, blockList, expInfo, conditionName, targetWord)
    
    # end of task: total reward
    totalScore = score1 + score2 
    totalReward = rew1 + rew2
    print('Total points for subject %s: %s' %(expInfo['participant'], totalScore))
    print('Total reward for subject %s: %s Euros' %(expInfo['participant'], totalReward))

elif session == 3:
    
    # Digit-span
    #-----------
    
    # Forward part instructions
    header = 'Merkaufgabe Teil 1'
    mainText = ("""In dieser Aufgabe werden Dir hintereinander Zahlen gezeigt. Diese Zahlen sollst Du Dir merken und anschließend """
    """in der Reihenfolge, wie sie präsentiert wurden, wiedergeben. Wenn Du z.B. 1, 2 und 3 siehst, gibst Du 123 ein. """
    """Du fängst mit einer kurzen Übung an.""")
    simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])
    
    # Training
    myGoal = 3
    backward = False
    dspanCond = 'training'
    digitSpanTask(experimentStructure, stimuliStructure, globalClock, filename, myGoal, backward, dspanCond)
    
    # Main task (forward)
    header = 'Anfang der Aufgabe'
    mainText = """Du fängst jetzt mit der Merkaufgabe an. Wenn Du noch Fragen hast, wende Dich bitte an den Versuchsleiter."""
    simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])
    
    # Run until digit-span is determined
    myGoal = 3
    backward = False
    dspanCond = 'forward'
    while True:
        routineTimer, globalClock, fixCrossTiming, corrRep = digitSpanTask(experimentStructure, stimuliStructure, globalClock, filename, myGoal, backward, dspanCond)
        print(corrRep)
        if sum(corrRep) >= 1:
            myGoal = myGoal + 1
            if myGoal == 10:
                break
        else:
            break
    
    # Backard part instructions
    header = 'Merkaufgabe Teil 2'
    mainText = ("""In dieser Aufgabe sollst Du die präsentierten Zahlen in umgekehrter Reihenfolge wiedergeben. """
    """Wenn Du z.B. die Zahlen 1, 2 und 3 siehst, gibst Du 321 ein. Du startest wieder mit einer kurzen Übung.""")
    simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])

    # Training
    myGoal = 3
    backward = True
    dspanCond = 'training'
    digitSpanTask(experimentStructure, stimuliStructure, globalClock, filename, myGoal, backward, dspanCond)
    
    # Main task (backward)
    header = 'Anfang der Aufgabe'
    mainText = """Du fängst jetzt mit der Merkaufgabe an. Wenn Du noch Fragen hast, wende Dich bitte an den Versuchsleiter."""
    simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])
    
    # Run until digit-span is determined
    myGoal = 3
    backward = True
    dspanCond = 'backward'
    while True:
        routineTimer, globalClock, fixCrossTiming, corrRep = digitSpanTask(experimentStructure, stimuliStructure, globalClock, filename, myGoal, backward, dspanCond)
        print(corrRep)
        if sum(corrRep) >= 1:
            myGoal = myGoal + 1
            if myGoal == 10:
                break
        else:
            break
    
    header = 'Ende der Aufgabe'
    mainText = "Vielen Dank für Deine Teilnahme!"
    simpleInstructions(experimentStructure, header, 0.1, [0, 0.6], mainText, 0.08, [0, 0.0])

# Close window
win.close()

# Deactivate eyetracker
if useEyeTracker:
    tracker.close()

# Plot dropped frames (this can be useful for fMRI and EEG applications)
intervalsMS = pylab.array(win.frameIntervals)*1000
m=pylab.mean(intervalsMS)
sd=pylab.std(intervalsMS)
distString= "Mean=%.1fms, s.d.=%.2f, 99%%CI(frame)=%.2f-%.2f" %(m,sd,m-2.58*sd,m+2.58*sd)
nTotal=len(intervalsMS)
nDropped=sum(intervalsMS>(1.5*m))

if nDropped >= 1:
    droppedString = "Dropped/Frames = %i/%i = %.3f%%" %(nDropped,nTotal, 100*nDropped/float(nTotal))

    # Plot the frameintervals
    pylab.figure(figsize=[12,8])
    pylab.subplot(1,2,1)
    pylab.plot(intervalsMS, '-')
    pylab.ylabel('t (ms)')
    pylab.xlabel('frame N')
    pylab.title(droppedString)

    # Plot histogram of the frameintervals
    pylab.subplot(1,2,2)
    pylab.hist(intervalsMS, 50, normed=0, histtype='stepfilled')
    pylab.xlabel('t (ms)')
    pylab.ylabel('n frames')
    pylab.title(distString)
    pylab.show()

else:
    print('No dropped frames')

# end task
core.quit()
