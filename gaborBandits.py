# -*- coding: utf-8 -*-

"""
Gabor-Bandit Task

Master script where all variables can be controlled.
The task is incentive compatible. Obtained reward 
is proportional to the difference between collected
points and chance performance. 
Includes digit-span task to measure working memory 
capacity.

Written by Rasmus Bruckner with contributions from Felix Molter.
Version 12/2019
"""

from __future__ import division
from psychopy import visual, core, data, event, logging, sound, gui
from psychopy.constants import *
from psychopy import parallel
import numpy as np
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os
import numpy as np
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
from math import atan2, degrees
import matplotlib
matplotlib.use('Qt4Agg')
import pylab
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
reload(sys)  
sys.setdefaultencoding('utf8')


# Set variables
# -------------

ID = '001' #u'8104' # participant's ID (use numbers)
set = 1  # predefined dataset
whichVersion = 1  # 1 = behavioral; 2 = fMRI
session = 2  # 1 = practice; 2 = main condition; 3 = digit-span, 4 = fMRI test run
nTrials = 25 #25  # for testing this has to be equal to the number of trials in the .xlsx file!
nBlocksSafe = 4  # 6 blocks
nBlocksUnc = 6  # 12 blocks
nBlocksTest = 1  # blocks for fMRI test run
nTrialsPatches = 100  # patch main and other practice: 100
nTrialsPatchesPract = 50 #50  # patch practice with feedback: 50
nTrialsTest = 394  # Trials for fMRI test run (max 394)
reward = 1  # number of points if rewarded
noReward = 0  # number of points if not rewarded
cBal = u'1'  # 1 = high contrast patch, 2 = low contrast patch
winFeedback = "+ 1 Punkt" 
neutralFeedback = "+ 0 Punkte"
scr_wdt, scr_hght = (1280, 1024)  # (800, 600)
useEyeTracker = False #True  # True
et_dummy = False #True  # use dummy eyetracker?
scanner_dummy = False #False#True#False  # use dummy scanner?
crit_win_dg = 5  # window size to skip trial when not fixated (currently not used)
monitor = "testMonitor" #"MRI screen" # use "testMonitor" when not using MRI screen
showDroppedFrames = False
mainSize = 0.06 # General text size
headerSize = 0.07 # General header size

# For current subject, check which blocks already exist in the data directory
saved_blocks = []
for i in range(0, nBlocksUnc):
    check_for_file = "data/main/*%s_%s.csv"%(ID, i)
    files = glob.glob(check_for_file)
    if len(files) > 0:
        saved_blocks.append(i)

# Based on existing blocks, propose which block should be done next
if not saved_blocks:
    proposed_block = 0
else:
    proposed_block = max(saved_blocks) + 1

# Show dialogue box with proposed block
myDlg = gui.Dlg(title="Gabor-bandit task")
myDlg.addText('Participant %s'%(ID))
myDlg.addField('Current block:', str(proposed_block))
ok_data = myDlg.show()  # show dialog and wait for OK or Cancel

if not myDlg.OK:
    
    # Quit if user presses 'cancel'
    print('User cancelled')
    core.quit()
    
else:
    
    # Extract block_number from list
    block_start = int(float(ok_data[0]))
    
    # Check if block number is in the range of pregenerated blocks
    if block_start < 0 or block_start >= 12:
        print('Block number not available')
        core.quit() # end task
    
    # Check if specified block number already exists
    check_for_file = "data/main/*%s_%s.csv"%(ID, block_start)
    files = glob.glob(check_for_file)
    if len(files) > 0:
        
        # If file exists, inform user and request confirmation
        myDlg = gui.Dlg(title="Gabor-bandit task")
        myDlg.addText('Block %s for participant %s already exists! \nPress OK to continue.'%(block_start, ID))
        ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
        
        if not myDlg.OK:
            
            # Quit if user presses 'cancel'
            print('User cancelled')
            core.quit()

# Convert crit_win from visual degrees to pixels
# Taken from: https://osdoc.cog.sci.nl/3.2/visualangle
h = 24.75
d = 119
r = 600
deg_per_px = degrees(atan2(.5*h, d)) / (.5*r)
crit_win = crit_win_dg / deg_per_px

# Use current set to determine random number generator for reproducible results
np.random.seed(set)

# Control timing
if whichVersion == 1 or (whichVersion == 2 and session == 1):
    if session == 1 or session == 2:
        fixCrossTiming = 0.9
        jitter = 0.2
        stimulusTiming = 1.0
    elif session == 3:
        fixCrossTiming = 0.9
        jitter = 0.2
        stimulusTiming = 1.0
elif whichVersion == 2:
    if session == 1 or session == 2:
        fixCrossTiming = 4.00
        jitter = 2.00
        stimulusTiming = 1.00
    elif session == 4:
        fixCrossTiming = 0.05
        jitter = 0.05
        stimulusTiming = 0.50

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
elif session == 4:
    folder = 'fMRI_test'

expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName
expInfo['session'] = session
expInfo['cBal'] = cBal

if whichVersion == 1:
    versionString = 'behav'
elif whichVersion == 2:
    if session == 1:
        versionString = 'fMRI_pract'
    elif session == 2:
        versionString = 'fMRI_main'
    elif session == 4:
        versionString = 'fMRI_vs'

if session == 1 or session == 2 or session == 4:
    filename = _thisDir + os.sep + 'data/%s/%s_%s_%s_%s_%s_%s' %(folder, expName, versionString, expInfo['date'], cBal, expInfo['participant'], block_start)
elif session == 3:
    filename = _thisDir + os.sep + 'data/%s_dspan/dspan_%s_%s' %(expName, expInfo['participant'],expInfo['date'])

# Initialize experiment handler
thisExp = data.ExperimentHandler(name = expName, version = '',
    extraInfo = expInfo, runtimeInfo = None,
    originPath = None,
    savePickle = True, saveWideText = True,autoLog = False,
    dataFileName = filename)  

# Initialize window object
win = visual.Window(size=(scr_wdt, scr_hght), monitor=monitor, screen=0, fullscr=True, units='deg', colorSpace='rgb') #color=[-.75,-.75,-.75]

# Initialize option to quit experiment using esc-key
endExpNow = False

# Frame rate
expInfo['frameRate'] = win.getActualFrameRate()
print('frame rate: %f' %(expInfo['frameRate']))
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0
win._refreshThreshold = frameDur + 0.004 # we want to allow 4ms tolerance

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
'useEyeTracker': useEyeTracker, 'et_dummy': et_dummy, 'scr_wdt': scr_wdt, 'scr_hght': scr_hght,
'crit_win': crit_win, 'block_start': block_start, 'scanner_dummy': scanner_dummy}

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
tracker = 0
if session == 1:
    
    # Indicate that the following sessions belong to the training blocks 
    conditionName = 'training'
    
    header = 'Herzlich Willkommen'
    mainText = 'Studie zum Thema Lernen und Entscheiden'
    
    simpleInstructions(experimentStructure, header, headerSize, [0, 0.6], mainText, mainSize, [0, 0.0])
    
    if expInfo['cBal'] == '1':
        positionPatch1 = [-3.5, 0] # -6
        positionPatch2 = [3.5, 0] # 6
    elif expInfo['cBal'] == '2':
        positionPatch1 = [3.5, 0] # 6
        positionPatch2 = [3.5, 0] # -6
    
    corrAns = 'return'
    exampleText = ("""Deine Aufgabe ist es zu entscheiden, welches der beiden Bilder %sr ist. """
    """Wenn z.B. das linke Bild %sr ist, drückst du die linke Pfeiltaste. """ %(targetWord2, targetWord2))
    patchesExample(experimentStructure, exampleText, positionPatch1, positionPatch2, corrAns)
    
    header = '1. Übung'
    mainText = ("""In dieser Übung sollst du wie im Beispiel angeben, welches Bild %sr """
    """ist. Nutze dafür die Pfeiltasten (rechts und links).\n\n"""
    """Während der Übung bekommst du Feedback, ob deine Antwort richtig oder falsch war. """
    """Bitte achte darauf, dass du immer in die Mitte des Bildschirms auf das Kreuz schaust! """
    """Mit Enter startest du die Übung.""" %(targetWord2))
    simpleInstructions(experimentStructure, header, headerSize, [0, 0.6], mainText, mainSize, [0, 0.0])
    
    whichLoop = 'patches'
    blockIndex = """blockFiles/set_%d/pract_PD/GB_runPatches1.xlsx""" %(set)
    showFeedback = 1
    accPerf = runPatches(experimentStructure, stimuliStructure, data, feedbackText, patchClock,
    whichLoop, conditionName, showFeedback, nTrialsPatchesPract, blockIndex, globalClock) #, eyeTracker
    
    header = 'Ende der Übung'
    mainText = ("""In diesem Block hast du %1.0f Mal richtig geantwortet!""" %(accPerf))
    simpleInstructions(experimentStructure, header, headerSize, [0, 0.6], mainText, mainSize, [0, 0.0])
    
    header = '2. Übung'
    mainText = ("""In dieser Übung sollst du wieder entscheiden, welches Bild %sr ist. """
    """Diesmal bekommst du allerdings kein Feedback zu deiner Antwort.""" %(targetWord2))
    simpleInstructions(experimentStructure, header, headerSize, [0, 0.6], mainText, mainSize, [0, 0.0])
    
    whichLoop = 'patches'
    blockIndex = """blockFiles/set_%1d/pract_PD/GB_runPatches2.xlsx""" %(set)    
    showFeedback = 0
    accPerf = runPatches(experimentStructure, stimuliStructure, data, feedbackText, patchClock,
    whichLoop, conditionName, showFeedback, nTrialsPatches, blockIndex, globalClock, 0)
    
    header = 'Ende der Übung'
    mainText = ("""In diesem Block hast du %1.0f Mal richtig geantwortet!""" %(accPerf))
    simpleInstructions(experimentStructure, header, headerSize, [0, 0.6], mainText, mainSize, [0, 0.0])
    
    corrAns = 'return'
    mainText = """Jetzt kommen zwei Muster hinzu. Im nächsten Schritt wird dir die Rolle dieser Muster erklärt."""
    fractalsExample(experimentStructure, mainText, corrAns)
    
    header = ' '
    mainText = ("""Ab jetzt sollst du versuchen, deinen Gewinn in der Aufgabe zu maximieren:\n\n"""
    """Es gibt zwei mögliche Kopplungen zwischen der Position des %sn Bildes (rechts und links) und den zwei Mustern (rot oder blau). """ 
    """Das Ziel ist es herauszufinden, gegeben der Position des %sn Bildes, welches Muster du wählen solltest, um wahrscheinlich eine Belohnung zu erhalten. """
    """Diese Kopplung lernst du durch Feedback nach der Antwort (%s).\n\nDeine so verdienten """
    """Punkte bekommst du am Ende, in Geld umgerechnet, ausgezahlt.""" %(targetWord, targetWord, winFeedback))
    simpleInstructions(experimentStructure, header, mainSize, [0, 0.6], mainText, mainSize, [0, 0.0])
    
    corrAns = 'left'
    exampleText = ("""Gib jetzt an, welches der beiden Bilder %sr ist. Da in diesem Fall das linke """
    """Bild %sr ist, drückst du die linke Pfeiltaste.""" %(targetWord2, targetWord2))
    patchesExample(experimentStructure, exampleText, positionPatch1, positionPatch2, corrAns)
    
    header = ' '
    mainText = ("""Du hast dich in diesem Beispiel entschieden, dass das Bild links %sr war. """
    """Im folgenden Schritt versuchst du herauszufinden, welches Muster bei "%ss Bild links" """
    """häufiger eine Belohnung gibt.\n\nBeachte, dass beide Muster mit einer """
    """bestimmten Häufigkeit zu einer Belohnung (%s) führen, aber eines öfter zu """
    """einer Belohnung führt und somit die bessere Antwort ist.""" %(targetWord2, targetWord, winFeedback))
    simpleInstructions(experimentStructure, header, headerSize, [0, 0.6], mainText, mainSize, [0, 0.0])
    
    corrAns = 'up'
    mainText = """In diesem Fall ist das rote Muster die bessere Antwort. Drücke daher die obere Pfeiltaste."""
    fractalsExample(experimentStructure, mainText, corrAns)
    
    header = ("""Wenn du das richtige Muster auswählst, erhältst du in den meisten Fällen eine Belohnung. """
    """Beachte, dass du manchmal trotz der besseren Antwort keine Belohnung erhälst.\n"""
    """Beachte außerdem, dass du manchmal auch bei der schlechteren Antwort eine Belohnung erhälst.""")
    mainText = winFeedback
    simpleInstructions(experimentStructure, header, mainSize, [0, 0.6], mainText, 0.1, [0, 0.0])
    
    header = ' '
    mainText = ("""Wenn sich das %s Bild auf der anderen Seite befindet, wählst Du auch das andere Muster.\n\n"""
    """Das heißt: Wenn du bei "%ss Bild links" am besten das rote Muster wählst, so nimmst du bei "%ss """
    """Bild rechts" am besten das blaue Muster.\n\nWir schauen uns hiervon jetzt ein Beispiel an.""" %(targetWord, targetWord, targetWord))
    simpleInstructions(experimentStructure, header, headerSize, [0, 0.6], mainText, mainSize, [0, 0.0])
    
    if expInfo['cBal'] == '1':
        positionPatch1 = [3, 0]# 3
        positionPatch2 = [-3, 0] # -3
    elif expInfo['cBal'] == '2':
        positionPatch1 = [-3, 0] # -3
        positionPatch2 = [3, 0] #3
        
    corrAns = 'right'
    exampleText = ("""Jetzt ist das rechte Bild %sr. Drücke daher die rechte Pfeiltaste.""" %(targetWord2))
    patchesExample(experimentStructure, exampleText, positionPatch1, positionPatch2, corrAns)
    
    corrAns = 'down'
    mainText = ("""Weil das %s Bild auf der anderen Seite war, ist jetzt das blaue Muster besser. """
    """Drücke daher die untere Pfeiltaste.""" %(targetWord))
    fractalsExample(experimentStructure, mainText, corrAns)

    header = ("""Daraufhin siehst du wieder ob du eine Belohnung erhalten hast.""")
    mainText = winFeedback
    simpleInstructions(experimentStructure, header, headerSize, [0, 0.6], mainText, 0.1, [0, 0.0])
    
    header = ' '
    mainText = ("""Innerhalb eines Blocks bleiben die Belohnungshäufigkeiten stabil. Das heißt, wenn """
    """du einmal herausgefunden hast, wann du am besten welches Muster wählst, bleibt dies bis zum nächsten Block konstant. """
    """Deine Belohnung erhälst du auch, wenn du das falsche Bild im ersten Schritt gewählt hast."""
    """Versuche bitte trotzdem so gut wie Möglich das richtige Bild anzugeben.""")
    simpleInstructions(experimentStructure, header, headerSize, [0, 0.6], mainText, mainSize, [0, 0.0])
    
    header = '3. Übung'
    mainText = ("""In dieser Übung sollst du jetzt selber herausfinden mit """
    """welchem Muster das %s Bild zusammenhängt, so dass du möglichst viele Punkte verdienst. """
    """Bitte achte wieder darauf, auf das Kreuz in der Mitte zu schauen!""" %(targetWord))
    simpleInstructions(experimentStructure, header, headerSize, [0, 0.6], mainText, mainSize, [0, 0.0])
    
    whichLoop = 'practice2'
    blockIndex = """blockFiles/set_%d/pract_safe/rightBlue/GB_RB_1.xlsx""" %(set)
    (accPerf, win) = runTask(experimentStructure, outcomeStructure, stimuliStructure,
    data, feedbackText, nTrials, whichLoop, blockIndex, 1, conditionName, globalClock, tracker)
    
    header = ' '
    mainText = ("""In diesem Block hast du %1.0f Punkte gesammelt!\n\n"""
    """Du fängst jetzt mit einem neuen Block """
    """an und musst den Zusammenhang zwischen der Seite des %sn Bildes und des Musters wieder neu lernen.""" %(accPerf, targetWord))
    simpleInstructions(experimentStructure, header, headerSize, [0, 0.6], mainText, mainSize, [0, 0.0])
    
    whichLoop = 'practice3'
    blockIndex = """blockFiles/set_%d/pract_safe/leftBlue/GB_LB_1.xlsx""" %(set)
    (accPerf, win) = runTask(experimentStructure, outcomeStructure, stimuliStructure,
    data, feedbackText, nTrials, whichLoop, blockIndex, 2, conditionName, globalClock, tracker)
    header = ' '
    
    header = 'Ende der Übung'
    mainText = ("""In diesem Block hast du %1.0f Punkte gesammelt!\n\n""" %(accPerf))
    simpleInstructions(experimentStructure, header, headerSize, [0, 0.6], mainText, mainSize, [0, 0.0])
    
    header = '4. Übung'
    mainText = ("""Diese Übung ist die letzte Übung bevor der Versuch startet. Du hast genau die gleiche """
    """Aufgabe wie in der letzten Übung, allerdings sind die Bilder in der ersten Stufe schwieriger von einander zu unterscheiden. """
    """Es ist wieder wichtig, dass du die ganze Zeit auf das Kreuz schaust!""")
    simpleInstructions(experimentStructure, header, headerSize, [0, 0.6], mainText, mainSize, [0, 0.0])
    
    whichLoop = 'practice4'
    blockIndex = """blockFiles/set_%d/pract_unc/leftBlue/GB_LB_1.xlsx""" %(set)
    (accPerf, win) = runTask(experimentStructure, outcomeStructure, stimuliStructure,
    data, feedbackText, nTrials, whichLoop, blockIndex, 2, conditionName, globalClock, tracker)
    
    header = ' '
    mainText = ("""In diesem Block hast du %1.0f Punkte gesammelt!\n\n"""
    """Du fängst jetzt mit einem neuen Block """
    """an und musst den Zusammenhang zwischen der Seite des %sn Bildes und des Musters wieder neu lernen.""" %(accPerf, targetWord))
    simpleInstructions(experimentStructure, header, headerSize, [0, 0.6], mainText, mainSize, [0, 0.0])
    
    whichLoop = 'practice5'
    blockIndex = """blockFiles/set_%d/pract_unc/rightBlue/GB_RB_1.xlsx""" %(set)
    (accPerf, win) = runTask(experimentStructure, outcomeStructure, stimuliStructure,
    data, feedbackText, nTrials, whichLoop, blockIndex, 3, conditionName, globalClock, tracker)
    
    header = 'Ende der Übung'
    mainText = ("""In diesem Block hast du %1.0f Punkte gesammelt!\n\n""" %(accPerf))
    simpleInstructions(experimentStructure, header, headerSize, [0, 0.6], mainText, mainSize, [0, 0.0])
    
    header = ' '
    mainText = """Du hast den Übungsteil jetzt abgeschlossen. Wende dich bitte an den Versuchsleiter."""
    simpleInstructions(experimentStructure, header, headerSize, [0, 0.6], mainText, mainSize, [0, 0.0])
    
elif session == 2:
    
    # Main task
    #----------
    
    if whichVersion == 1:
        # First part: "economic decision making"
        leftBlue  = glob.glob('blockFiles/set_%1.0f/main_safe/leftBlue/*.xlsx' %(set))
        rightBlue = glob.glob('blockFiles/set_%1.0f/main_safe/rightBlue/*.xlsx' %(set))
        blockList = (leftBlue + rightBlue)
        shuffle(blockList)
        print(blockList)    
        
        header = 'Entscheidungsaufgabe Teil 1'
        mainText = ("""Ab jetzt erhälst du Punkte für deine Entscheidungen. Die Punkte werden am Ende des Experiments in Geld umgerechnet. """
        """Du fängst mit %1.0f Blöcken an, in denen du den Kontrast der Bilder einfach unterscheiden kannst. """ 
        """Bitte schaue wieder auf das Kreuz in der Mitte des Bildschirms!""" %(nBlocksSafe))
        simpleInstructions(experimentStructure, header, headerSize, [0, 0.6], mainText, mainSize, [0, 0.0])
        
        conditionName = 'main_safe'
        nBlocks = nBlocksSafe
        (score1, rew1) = taskLoop(set, nBlocks, whichVersion, globalClock, experimentStructure, outcomeStructure, stimuliStructure, data,
        feedbackText, nTrials, blockList, expInfo, conditionName, targetWord)
        
        # Second part: "perceptual decision making"
        header = 'Kontrastentscheidungen'
        mainText = ("""In dieser Aufgabe siehst du ausschließlich die Bilder aus der Entscheidungsaufgabe. Wie in der Übung am Anfang, sollst du angeben, """
        """welches Bild %sr ist.""" %(targetWord2))
        simpleInstructions(experimentStructure, header, headerSize, [0, 0.6], mainText, mainSize, [0, 0.0])
        
        whichLoop = 'patches'
        blockIndex = """blockFiles/set_%d/main_PD/GB_runPatches1.xlsx""" %(set)
        showFeedback = 0
        accPerf = runPatches(experimentStructure, stimuliStructure, data, feedbackText, patchClock,
        whichLoop, conditionName, showFeedback, nTrialsPatches, blockIndex, globalClock) #eyeTracker
        
        header = 'Ende Kontrastentscheidungen'
        mainText = ("""In diesem Block hast du %1.0f Mal richtig geantwortet!""" %(accPerf))
        simpleInstructions(experimentStructure, header, headerSize, [0, 0.6], mainText, mainSize, [0, 0.0])
    
    # Third part: "economic decision making under perceptual uncertainty"
    if whichVersion == 1:
        header = 'Entscheidungsaufgabe Teil 2'
        mainText = ("""Jetzt kommt der zweite Teil der Entscheidungsaufgabe. Du sollst wieder probieren, möglichst viele Punkte zu verdienen. """
        """Dabei kannst du die Kontraste manchmal nur schwer von einander unterscheiden. Insgesamt durchläufst du %1.0f Blöcke. """ 
        """Bitte schaue wieder auf das Kreuz in der Mitte des Bildschirms!""" %(nBlocksUnc))
    else: 
        header = 'Entscheidungsaufgabe'
        mainText = ("""Ab jetzt erhälst du Punkte für deine Entscheidungen. Die Punkte werden am Ende des Experiments in Geld umgerechnet. """
        """Du wirst die Kontraste manchmal nur schwer von einander unterscheiden können. Insgesamt durchläufst du noch %1.0f Blöcke.""" %(nBlocksUnc-block_start))
    simpleInstructions(experimentStructure, header, headerSize, [0, 0.6], mainText, mainSize, [0, 0.0])
    
    leftBlue = glob.glob('blockFiles/set_%1.0f/main_unc/leftBlue/*.xlsx' %(set))
    rightBlue = glob.glob('blockFiles/set_%1.0f/main_unc/rightBlue/*.xlsx' %(set))
    blockList = (leftBlue + rightBlue)
    shuffle(blockList)
    print(blockList)
    
    conditionName = 'main_unc'
    nBlocks = nBlocksUnc
    (score2, rew2) = taskLoop(set,nBlocks, whichVersion, globalClock, experimentStructure, outcomeStructure, stimuliStructure, data,
    feedbackText, nTrials, blockList, expInfo, conditionName, targetWord)
    
    # End of task: total reward
    if whichVersion == 1:
        totalScore = score1 + score2 
        totalReward = rew1 + rew2
        #print('----------')
        print('Total points for subject %s: %s' %(expInfo['participant'], totalScore))
        print('Total reward for subject %s: %s Euros' %(expInfo['participant'], totalReward))
    
elif session == 3:
    
    # Digit-span
    #-----------
    
    # Forward part instructions
    header = 'Merkaufgabe Teil 1'
    mainText = ("""In dieser Aufgabe werden dir hintereinander Zahlen gezeigt. Diese Zahlen sollst du dir merken und anschließend """
    """in der Reihenfolge, wie sie präsentiert wurden, wiedergeben. Wenn du z.B. 1, 2 und 3 siehst, gibst du 123 ein. """
    """Du fängst mit einer kurzen Übung an.""")
    simpleInstructions(experimentStructure, header, headerSize, [0, 0.6], mainText, mainSize, [0, 0.0])
    
    # Training
    myGoal = 3
    backward = False
    dspanCond = 'training'
    digitSpanTask(experimentStructure, stimuliStructure, globalClock, filename, myGoal, backward, dspanCond)
    
    # Main task (forward)
    header = 'Anfang der Aufgabe'
    mainText = """Du fängst jetzt mit der Merkaufgabe an. Wenn du noch Fragen hast, wende dich bitte an den Versuchsleiter."""
    simpleInstructions(experimentStructure, header, headerSize, [0, 0.6], mainText, mainSize, [0, 0.0])
    
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
    mainText = ("""In dieser Aufgabe sollst du die präsentierten Zahlen in umgekehrter Reihenfolge wiedergeben. """
    """Wenn du z.B. die Zahlen 1, 2 und 3 siehst, gibst du 321 ein. Du startest wieder mit einer kurzen Übung.""")
    simpleInstructions(experimentStructure, header, headerSize, [0, 0.6], mainText, mainSize, [0, 0.0])

    # Training
    myGoal = 3
    backward = True
    dspanCond = 'training'
    digitSpanTask(experimentStructure, stimuliStructure, globalClock, filename, myGoal, backward, dspanCond)
    
    # Main task (backward)
    header = 'Anfang der Aufgabe'
    mainText = """Du fängst jetzt mit der Merkaufgabe an. Wenn du noch Fragen hast, wende dich bitte an den Versuchsleiter."""
    simpleInstructions(experimentStructure, header, headerSize, [0, 0.6], mainText, mainSize, [0, 0.0])
    
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
    mainText = "Vielen Dank für deine Teilnahme!"
    simpleInstructions(experimentStructure, header, headerSize, [0, 0.6], mainText, mainSize, [0, 0.0])

elif session == 4:
    
    # fMRI test run
    #--------------
    
    conditionName = 'fMRI_test'
    blockList = glob.glob('blockFiles/fMRI_test.xlsx')
    (score2, rew2) = taskLoop(set, nBlocksTest, whichVersion, globalClock, experimentStructure, outcomeStructure, stimuliStructure, data,
    feedbackText, nTrialsTest, blockList, expInfo, conditionName, targetWord)
    
# Close window
win.close()

# Plot dropped frames (this can be useful for fMRI and EEG applications)
intervalsMS = pylab.array(win.frameIntervals)*1000
m = pylab.mean(intervalsMS)
sd = pylab.std(intervalsMS)
distString = "Mean=%.1fms, s.d.=%.2f, 99%%CI(frame)=%.2f-%.2f" %(m,sd,m-2.58*sd,m+2.58*sd)
nTotal = len(intervalsMS)
nDropped = sum(intervalsMS>(1.5*m))

if showDroppedFrames:
    if nDropped >= 1:
        
        # String that is printed
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
