from psychopy import visual, core
import inspect

# Collection of functions to initialize different task component objects

def initializeFixationCross(win):
    """ This function initializes the fixation cross object
        
        Input:
            win: window object instance
        
        Return: 
            fixationCross object
    """
    fixationCross = visual.TextStim(win=win, ori=0, name='fixationCross',
        text='+',    font='Arial',
        pos=[0, 0], height=0.1, wrapWidth=None,
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0, units = "norm")
    return(fixationCross)
    
def initializeQuestProcedure(win):
    """ This function initializes the QuestProcedure (clock) object
        
        Quest procedure was not applied in the task.
    
    Input:
        win: window object instance
        
    Return: 
        questClock: clock object for quest procedure timing
    """
    
    questClock = core.Clock()
    return(questClock)
    
def initializePatches(win, expInfo):
    """ This function initializes the Gabor-patches
    
    Input:
        win: window object instance
        expInfo: Structure with background information about experiment
        
    Return: 
        patchClock: clock object instance for patch timing
        patch1: object instance for first Gabor-patch
        patch2: object instance for second Gabor-patch
    """
    
    patchClock = core.Clock()
    ISI = core.StaticPeriod(win=win, screenHz=expInfo['frameRate'], name='ISI')
    patch1 = visual.GratingStim(win=win, name='patch1',units='cm', 
        tex='sin', mask='raisedCos',
        ori=0, pos=[0,0], size=10, sf=0.4, phase=0.0,
        color=[1,1,1], colorSpace='rgb', opacity=1.0,
        texRes=512, interpolate=True, depth=-1.0)
    patch2 = visual.GratingStim(win=win, name='patch2',units='cm', 
        tex='sin', mask='raisedCos',
        ori=0, pos=[0,0], size=10, sf=0.4, phase=0.0,
        color=[1,1,1], colorSpace='rgb', opacity=1.0,
        texRes=512, interpolate=True, depth=-2.0)
    return(patchClock, patch1, patch2) 

def initializeFractals(win, expInfo):
    """ This function initializes the fractals
    
    Input:
        win: window object instance
        expInfo: Structure with background information about experiment
        
    Return: 
        patchClock object: clock object instance for fractal timing
        fractal1: object instance for first fractal
        fractal2: object instance for second fractal
    """
    
    fractalClock = core.Clock()
    fixation1 = visual.TextStim(win=win, ori=0, name='fixation1',
        text='+',    font='Arial',
        pos=[0, 0], height=0.1, wrapWidth=None,
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0)
    fractal1 = visual.ImageStim(win=win, name='fractal11',units='cm', 
        image='blueFractal.jpg', mask=None,
        ori=0, pos=[0,0], size=[9.6, 6],
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-1.0)
    fractal2 = visual.ImageStim(win=win, name='fractal22',units='cm', 
        image='redFractal.jpg', mask=None,
        ori=0, pos=[0,0], size=[9.6, 6],
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-2.0)
    return(fractalClock, fractal1,fractal2) 
    
def initializeFeedback(win, expInfo):
    """ This function initializes the reward feedback
    
    Input:
        win: window object
        expInfo: Structure with background information about experiment
        
    Return: 
        feedbackClock: clock object for feedback timing
        feedbackText: feedback text object instance
    """
    
    feedbackClock = core.Clock()
    feedbackText = visual.TextStim(win=win, ori=0, name='text',
        text='default text',    font=u'Arial',
        pos=[0, 0], height=0.1, wrapWidth=None,
        color=u'white', colorSpace='rgb', opacity=1,
        depth=0.0, units="norm")
    return(feedbackClock, feedbackText) 

def initializeSimpleInstructions(win, header, headerHeight, headerTextPosition, mainText, mainHeight, mainTextPosition):
    """ This function initializes the variable instructions
    
    Input:
        win: window object
        header: header for instructions
        headerHeight: height of header on the screen
        headerTextPosition: position of header on the screen
        mainText: instructions text
        mainHeight: height of instructions text on the screen
        mainTextPosition: position of the instructions text on the screen
        
    Return: 
        instructionsClock object: clock object for instructions timing
        header: header object instance
        mainText: main text object instance
    """
    instructionsClock = core.Clock()
    header = visual.TextStim(win=win, ori=0, name='header',
        text=header,    font='Arial',
        pos=headerTextPosition, height=headerHeight, wrapWidth=1.5,
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0, units = "norm")
    mainText = visual.TextStim(win=win, ori=0, name='mainText',
        text=mainText, font='Arial',
        pos=mainTextPosition, height=mainHeight, wrapWidth=1.5,
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0, units = "norm")
    return (instructionsClock, header, mainText)
    
def initializePatchesExample(win, exampleText, positionPatch1, positionPatch2):
    """ This function initializes an example to introduce the Gabor-patches
    
    Input:
        win: window object
        exampleText: text that is displayed during patch example
        positionPatch1: position of the first patch
        positionPatch2: position of the second patch
        
    Return: 
        patchExampleClock object: clock object for patch example timing
        examplePatch1: patch1 object instance
        examplePatch2: patch2 object instance
        exampleText: exampleText object instance
    """
    patchExampleClock = core.Clock()
    examplePatch1 = visual.GratingStim(win=win, name='examplePatch1',units='cm',
        tex=u'sin', mask=u'raisedCos',
        ori=0, pos=positionPatch1, size=10, sf=0.4, phase=0.0,
        color=[1,1,1], colorSpace='rgb', opacity=0.7,
        texRes=512, interpolate=True, depth=-1.0)
    examplePatch2 = visual.GratingStim(win=win, name='examplePatch2',units='cm',
        tex=u'sin', mask=u'raisedCos',
        ori=0, pos=positionPatch2, size=10, sf=0.4, phase=0.0,
        color=[1,1,1], colorSpace='rgb', opacity=0.5,
        texRes=512, interpolate=True, depth=-1.0)
    exampleText = visual.TextStim(win=win, ori=0, name='mainText',
        text=exampleText,font=u'Arial', pos=[0, 0.6], height=0.08,
        wrapWidth=1.5, color=u'white', colorSpace='rgb', opacity=1,
        depth=-4.0, units = "norm")
    return(patchExampleClock, examplePatch1, examplePatch2, exampleText)
        
def initializeFractalsExample(win, fractalText):
    """ This function initializes an example to introduce the fractals 
    
    Input:
        win: window object
        fractalText: text that is displayed during fractals example
        
    Return: 
        fractalExampleClock: clock object for fractal example timing
        exampleFractal1: exampleFractal1 object instance
        exampleFractal2: exampleFractal2 object instance
        exampleText: exampleText object instance
    """
    
    fractalExampleClock = core.Clock()
    fixation1 = visual.TextStim(win=win, ori=0, name='fixation1',
        text='+',    font='Arial',
        pos=[0, 0], height=0.1, wrapWidth=None,
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0)
    exampleFractal1 = visual.ImageStim(win=win, name='fractal11',units='cm', 
        image='blueFractal.jpg', mask=None,
        ori=0, pos=[0,0], size=[9.6, 6],
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-1.0)
    exampleFractal2 = visual.ImageStim(win=win, name='fractal22',units='cm', 
        image='redFractal.jpg', mask=None,
        ori=0, pos=[0,0], size=[9.6, 6],
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-2.0)
    exampleText = visual.TextStim(win=win, ori=0, name='text',
        text=fractalText, font=u'Arial',
        pos=[0, 0.8], height=0.08, wrapWidth=1.5,
        color=u'white', colorSpace='rgb', opacity=1,
        depth=-4.0, units = "norm")
    return(fractalExampleClock, exampleFractal1, exampleFractal2, exampleText) 
   
def initializeFeedbackExample(win, feedbackText, exampleText):
    """ This function initializes an example to introduce feedback
    
    Input:
        win: window object
        feedbackText: feedback that is displayed
        exampleText: text that is displayed during feedback example
        
    Return: 
        feedbackClock object: clock object instance for feedback example timing
        feedbackText: feedbck text object instance
        exampleText: exampleText object instance
    
    """
    feedbackClock = core.Clock()
    feedbackText = visual.TextStim(win=win, ori=0, name='text',
        text=feedbackText, font=u'Arial',
        pos=[0, 0], height=0.1, wrapWidth=1,
        color=u'white', colorSpace='rgb', opacity=1,
        depth=-4.0)
    exampleText = visual.TextStim(win=win, ori=0, name='text',
        text=exampleText, font=u'Arial',
        pos=[0, 0.6], height=0.08, wrapWidth=1.5,
        color=u'white', colorSpace='rgb', opacity=1,
        depth=-4.0)
    return(feedbackClock, feedbackText, exampleText)