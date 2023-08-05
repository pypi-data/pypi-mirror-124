"""
    PsychopyManager

    Developed by Brandon Egger for the University of Iowa 
    SCNLab led by Dorit Kliemann.

    This module builds off of the PsychoPy library,
    developed by Jon Peirce and others.
    found at: https://www.psychopy.org/download.html
"""

from psychopy import  monitors, gui, visual, core, data, event, clock, sound
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
from psychopy.hardware.emulator import launchScan # Add and customize this www.psychopy.org/api/hardware/emulator.html
from psychopy.info import RunTimeInfo

from scipy.io.wavfile import write
import pandas as pd
import sounddevice as sd
import soundfile as sf
import queue
import os
import datetime
import copy
import time

class PsychopyTask():
    """
    Class designed to structure a typical Psychopy Task. Allows for quick
    development and deployment of unique tasks using common elements built
    into the PsychoPy library.

    Attributes
    ----------
    subjectID : str
        Subject identifier
    taskName : str
        Name of task
    runName : str
        Name of run
    keyInputReference : dict
        Key: keyboard key, Value: What key press is saved as in key logs
    interruptKeys : list
        List of keys which end task abruptly
    stimDir : str
        Directory stimuli are stored
    outputsDir : str
        Directory exportCSV() stores pandas CSV file.
    loadedStimuli : dict
        Key: stimulus name, value: respective stimulus object
    window : PsychoPy Window
        Reference to window object
    taskDF : Pandas DataFrame
        Reference to dataframe object
    dataPath : str
        Once an export has been done, this stores the location of the data.
    micStream : 
        Microphone object
    """

    videoExtensions = ["avi", "mov"]
    photoExtensions = ["png", "jpeg"]
    audioExtensions = ["wav"]

    def __init__(self, subject, taskName, runName, runKeyReference={}, interruptKeys=[], dataFrameColumns =[],
                 monitorRes="1920x1080", screenNum=0, fullscreen=False, 
                 toPreloadStim = True, stimulusDir = None, outputsDir = None):
        """
        Parameters
        ----------
        subject : str
            Subject ID string
        taskName : str
            Name of task
        runName : str
            Name of run
        runKeyReference : dict
            Key represents keyboard input, value represents the value it is replaced with
        interruptKeys : list
            List of keys which interrupt task (exiting application)
        dataFrameColumns : list
            List of columns needed in dataframe
        monitorRes : str, default="1920x1080"
            String representing "widthxheight" for monitor resolution
        sreenNum : int, default=0
            Which monitor to use, main monitor is 0.
        fullScreen : bool, default=False
            Whether window appears fullscreen
        toPreloadStim : bool, default=True
            Whether all stimulus are preloaded (stored to memory) when added
            Setting to True improves run time performance at the expensive of system memory.
        stimulusDir : str, default=None
            Directory stimuli are found in. When set to None, no file type stimuli can be loaded.
            All file type stimuli must be stored in this directory (IMG's, Videos, Sound)
        outputsDir : str, default=None
            Directory output CSV file is saved to. When set to None, exportCSV() will throw error.

        Notes
        -----
        Leave all window settings (monitorRes, screenNum, fullscreen) set to defaults
        when running on UIowa MRI stimulus PC.
        """

        self.loadedStimuli = {} #Where preloaded stimulus go
        self.taskName = taskName
        self.setSubject(subject)
        self.setRunName(runName)
        self.interruptKeys = interruptKeys
        self.setStimulusDir(stimulusDir)
        self.setOutputsDir(outputsDir)
        self.setKeyInputReference(runKeyReference)
        self.dataPath = None

        #For audio recording
        self.initializeAudioCapture()

        #Create window instance:
        self.window = visual.Window(size=self.__convertResolution(monitorRes), fullscr=fullscreen, screen=screenNum,
            allowGUI=False, allowStencil=False, units='deg', monitor='', 
            colorSpace='rgb', blendMode='avg', useFBO=True)
        self.window.recordFrameIntervals=True

        for key in interruptKeys:
            event.globalKeys.add(key, func=self.end)
        self.window.mouseVisible = False
        self.taskDF = {key:[] for key in dataFrameColumns}

    #---Functional---#
    def exportCSV(self, path=None):
        """
        Exports the data collected to a desired directory.
        Defaults to the outputDir set on object initialization.
        
        Parameters
        ----------
        path : str
            Path to output files directory.

        See Also
        --------
        addDataPoint() for adding data.
        """
        if path == None and self.dataPath == None:
            if self.outputsDir == None:
                raise ValueError("Can't export CSV without path.")

            path = os.path.join(self.outputsDir, f"sub-{self.subjectID}_task-{self.taskName}_run-{self.runName}.csv")

        if self.dataPath == None:
            self.dataPath = self.__getValidPath(path)

        outputDict = copy.deepcopy(self.taskDF)

        maxColumnSize = 0
        #Find largest column
        for column in outputDict:
            maxColumnSize = max(maxColumnSize, len(outputDict[column]))

        #Repair small columns
        for column in outputDict:
            if len(outputDict[column]) < maxColumnSize:
                addElements = [None for i in range(0,maxColumnSize - len(outputDict[column]))]
                outputDict[column] = outputDict[column] + addElements

        pd.DataFrame(outputDict).to_csv(self.dataPath, index=False)

    def end(self):
        """For halting task"""
        self.exportCSV()
        core.quit()
 
    #TODO: I don't think videos that haven't been preloaded will work
    def runStimulus(self, stimName, stimulus = None, wait=5, logKeys = False, ignoreKeys = []):
        """
        Displays selected stimulus on task's window, 
        if stimulus is not preloaded (aka stimName not found in loadedStimuli)
        then stimulus is loaded first.

        Parameters
        ----------
        stimName : str
            The name which the stimulus is/will be saved under in loadedStimuli
        stimulus : str or stimulus object, default=None
            The stimulus to be displayed. When given str a TextStim is assumed.
            Only used if stimulus has not been preloaded.
        wait : int or str or list, default=5
            If an int, stimulus is held on screen for wait seconds
            If a str, stimulus is held on screen until wait key is pressed
            If a list, stimulus is held on screen until a key in wait is pressed
        logKeys : bool, default=False
            When true, key presses that occur during stimulus display are
            returned as tuples (key, timestamp) under keyLog
        ignoreKeys : list, default=[]
            Keys in this list will not be logged.

        Returns
        -------
        startTime : str
            Formatted start time
        endTime : str
            Formatted end time
        duration : float
            length of duration stimulus was displayed in seconds
        keyLog : list
            List of key press tuples (key, timestamp) in order


        Notes
        -----
        Audio stimulus return None
        """

        startTime = datetime.datetime.now()
        endTime = None
        startClock = core.MonotonicClock()

        keyLog = []

        stimObj = None
        if not stimName in self.loadedStimuli:
            stimObj = self.loadStimulus(stimName, stimulus)
        else:
            stimObj = self.loadedStimuli[stimName]
        
        if type(stimObj) == visual.MovieStim3:
            stimObj.play()
            while stimObj.status != FINISHED:
                stimObj.draw()
                self.window.flip()

            endTime = datetime.datetime.now()
        elif type(stimObj) == sound.Sound:
            stimObj.play()
            return None #Audio object returns none
        else:
            if type(stimObj) == list:
                for stim in stimObj:
                    stim.draw()
            elif type(stimObj) == visual.text.TextStim:
                stimObj.draw()
            else:
                raise ValueError(f"Invalid stimulus type - {type(stimulus)}")

            self.window.flip()

            if type(wait) == int:
                event.clearEvents('keyboard')

                while startClock.getTime() < wait:
                    newInputs = event.getKeys(timeStamped = startClock)
                    for keyIn in newInputs:
                        if keyIn[0] not in ignoreKeys and logKeys:
                            keyLog.append((self.__formatKeyPress(keyIn[0]), keyIn[1]))
            elif type(wait) == str or type(wait) == list:
                ended = False
                if type(wait) == str:
                    wait = [wait]

                while not ended:
                    newInputs = event.getKeys(timeStamped = startClock)
                    for keyIn in newInputs:
                        if keyIn[0] in wait:
                            ended = True
                        elif keyIn[0] not in list(ignoreKeys) and logKeys:
                            keyLog.append((self.__formatKeyPress(keyIn[0]), keyIn[1]))
                    time.sleep(0.01)

            endTime = datetime.datetime.now()
        return self.dateTimeStr(startTime), self.dateTimeStr(endTime), (endTime-startTime).total_seconds(), keyLog

    def initializeAudioCapture(self):
        self.__micQueues = {}
        self.__activeMicQueue = None
        self.micStream = sd.InputStream(samplerate=41000, channels=1, callback=self.__callback)

    def startAudioCapture(self, audioLabel):
        """
        Begins audio recording if none is active, active mic queue begins
        
        Parameters
        ----------
        audioLabel, str
            Key for which the recording data is stored under.
        """

        if self.__activeMicQueue != None:
            raise ValueError("Attempted to start an audio recording while another audio recording is active.\nRun stopAudioCapture() before starting again.")

        if audioLabel not in self.__micQueues:
            self.__micQueues[audioLabel] = {"queue": queue.Queue(), "file": None}
        self.__activeMicQueue = audioLabel

        self.micStream.start()

    def stopAudioCapture(self):
        """Halts active audio capture"""

        if self.__activeMicQueue == None:
            raise ValueError("An audio recording must be active for it to be stopped.")

        self.micStream.stop()
        self.__activeMicQueue = None

    def saveAudioCapture(self, audioLabel):
        """
        Saves remaining audio queue data (stored in memory) to disk

        Parameters
        ----------
        audioLabel, str
            Key for which the recording data is stored under.
        """

        if not audioLabel in self.__micQueues:
            raise ValueError(f"Audio label: {audioLabel} does not exist in the queue library.")

        if self.__micQueues[audioLabel]["file"] == None:
            soundPath = os.path.join(self.outputsDir,f"sub-{self.subjectID}_audio-{audioLabel}.wav")
            self.__micQueues[audioLabel]["file"] = sf.SoundFile(self.__getValidPath(soundPath),mode='x', samplerate=41000,channels=1)
        audioQueue = self.__micQueues[audioLabel]["queue"]
        audioFile = self.__micQueues[audioLabel]["file"]

        while not audioQueue.empty():
            audioFile.write(audioQueue.get())

        print(f"Audio: {audioLabel} was successfully saved!")


    def loadStimulus(self, stimKey, stimulus, isFile = False, storeValue = True):
        """
        Loads in a stimulus object to memory, stored in loadedStimuli

        Parameters
        ----------
        stimKey : str
            Key stimulus object is stored under in loadedStimuli.
        stimulus : str, dict
            Stimulus object data, dict. If isFile, this should be a file name
            within stimDir.
        isFile : bool, default=False
            When true, stimulus object is MovieStim, Audio, or ImageStim.
        storeValue : bool, default=True
            When true, value is stored to memory in loadedStimuli. Set to false
            when you just need stimulus object locally.

        Returns
        -------
        finalStimulus : Stimulus Object
            Either TextStim, MovieStim3, or *coming soon* ImageStim, Audio
            regardless of whether it was stored to loadedStimuli

        See Also
        --------
        *Place holder for info about writing stimulus dict*
        """

        if type(stimulus) == list:
            self.loadedStimuli[stimKey] = [self.loadStimulus(stimKey, subStim, isFile, storeValue = False) for subStim in stimulus]
            return self.loadedStimuli[stimKey]
        
        if type(stimulus) != str and type(stimulus) != dict:
            raise ValueError(f"Expected value of stimulus to be str or dict, instead got {type(stimulus)}")



        finalStimulus = None
        if type(stimulus) == dict:
            finalStimulus = self.dictToStim(stimulus)
        elif isFile:
            extSplit = stimulus.strip().split('.')
            if len(extSplit) < 2:
                raise ValueError(f"No extension provided for file {stimulus}")

            fileName = extSplit[0]
            fileExt = extSplit[1]

            if fileExt in PsychopyTask.videoExtensions:
                finalStimulus = visual.MovieStim3(win=self.window, filename=os.path.join(self.stimDir, stimulus.strip()),name=fileName)
            elif fileExt in PsychopyTask.photoExtensions:
                pass #Do img stim
            elif fileExt in PsychopyTask.audioExtensions:
                finalStimulus = sound.Sound(os.path.join(self.stimDir, stimulus.strip()))
            else:
                raise ValueError(f"{fileExt} extension is not currently supported!")

        else:
            if type(stimulus) != str:
                raise ValueError(f"Expected type str for stimulus, received {type(stimulus)}")

            finalStimulus = visual.TextStim(win=self.window, name='textstim',
                text=stimulus, units='norm',
                font=u'Arial', height=0.1, wrapWidth=self.window.size[0], ori=0,
                color=u'white', colorSpace='rgb', opacity=1,
                languageStyle='LTR',
                depth=0.0);
        if storeValue:
            self.loadedStimuli[stimKey] = finalStimulus
        return finalStimulus

    def dictToStim(self, stimDict):
        """
        Function for converting dictionary to stimulus. Depending on which parameters are provided,
        dictToStim will automatically determine the correct Stimulus type.

        Parameters
        ----------
        stimDict : dict
            Stim dictionary has keys representing the parameters of a stimulus object.

        See Also
        --------
        For more information on stimulus parameters, visit PsychoPy's documentation at
        <https://www.psychopy.org/documentation.html>
        """

        stimTypes = ["filename", "text", "image"]
        if len(set(stimDict.keys()).intersection(stimTypes)) > 1:
            raise ValueError("Unable to convert dictionary to stimulus when multiple stimulus types are given. Only specify filename OR text OR image!")
        elif len(set(stimDict.keys()).intersection(stimTypes)) == 0:
            raise ValueError(f"Your dictionary is missing a stimulus identifier, you are required to have only ONE of the following: {stimTypes}")

        stimDict["win"] = self.window #Need to add window parameter

        if "filename" in stimDict:
            fileExtension = stimDict["filename"].split(".")[-1]
            if fileExtension not in PsychopyTask.videoExtensions:
                raise ValueError(f"{fileExtension} is not a supported video file type.")

            stimDict["filename"] = os.path.join(self.stimDir, stimDict["filename"])
            return visual.MovieStim3(**stimDict)
        elif "image" in stimDict:
            fileExtension = stimDict["image"].split(".")[-1]
            if fileExtension not in PsychopyTask.photoExtensions:
                raise ValueError(f"{fileExtension} is not a supported image file type.")

            stimDict["image"] = os.path.join(self.stimDir, stimDict["image"])
            return visual.ImageStim(**stimDict)
        elif "text" in stimDict:
            stimDict["wrapWidth"]=self.window.size[0]
            return visual.TextStim(**stimDict)
        else:
            raise ValueError("A text or file address must be provided for a stimulus to be made!")

    def addDataPoint(self, column, data):
        """
        Function for adding data to the pandas DataFrame.

        Parameters
        ----------
        column : str
            Column which data is appended to.
        data: any
            Takes some data type and adds it as a new row to the column.
        """

        if column in self.taskDF:
            self.taskDF[column] += [data]
        else:
            raise ValueError(f"The column '{column}' is not in the task data set. Select from the list VideoTask.dfColumns")
    
    def dateTimeStr(self, dt):
        """
        Takes a datetime.datetime object and returns a formatted string
        following "hours:minutes:seconds:microseconds"
        """
        return f"{dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}.{dt.microsecond}"

    def exportAudio(self, path):
        pass #Exports audio

    #---Setters---#
    def setSubject(self, subStr):
        """Setter function for subjectID attribute."""

        if subStr == None:
            raise ValueError("A task object requires a subject ID.")

        self.subjectID = subStr

    def setOutputsDir(self, path):
        self.outputsDir = path

    def setRunName(self, runName):
        """Setter function for runName attribute."""

        if runName == None:
            raise ValueError("A task object requires a run name.")

        self.runName = runName

    def setStimulusDir(self, path):
        """Setter function for stimDir attribute."""

        #TODO: Make 'cur/dir/dir' default to os.getcwd()+'/dir/dir'
        self.stimDir = path

    def setKeyInputReference(self, refDict):
        """Setter function for keyInputReference attribute."""

        self.keyInputReference = refDict

    def setScreenNum(self, screenNum):
        pass #Updates window

    def setResolution(self, resolution):
        pass #convert resolution, update window

    def setScreen(self, screenNum):
        pass #updates window

    def setFullscreen(self, fullscreen):
        pass #updates window

    #---Getters---#
    def getStim(self, stimName, stimList, preload=True, isFile = False):
        """
        Used when you have unique expected types of stimuli which you are loading in.
        Designed to add preload and isFile functionality to the loadStimulus function.

        Parameters
        ----------
        stimName : str
            Name of stimulus, when preload True this is the key the stimulus object is stored under
            inside of loadedStimuli dictionary.
        stimList : dict, str or list
            List of stimuli or single stimuli reference.
        preload : bool, default=True
            Whether stimuli should be stored in loadedStimuli
        isFile : bool, default=False
            If stimList is/contains file names rather than content, set to True.

        Returns
        -------
        The stimuli object

        See Also
        --------
        PsychopyTask.loadStimulus
        """

        if stimName in self.loadedStimuli:
            return self.loadedStimuli[stimName]

        return self.loadStimulus(stimName, stimList, isFile, preload)

    def getSubjectID(self):
        return self.subjectID

    def getDataFrame():
        pass #Returns dataframe (this would be the df exported by exportcsv)

    def getMicrophone():
        """
        Returns Microphone object

        See Also
        --------
        startAudioRecording - For initializing microphone object.
        """
        return self.microphoneObj

    #---Private---#
    def __callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.__micQueues[self.__activeMicQueue]["queue"].put(indata.copy())

    def __getValidPath(self, desiredPath):
        """
        Takes a desired file path, creates the needed folders, 
        checks if path is a duplicate, returns the updated file path

        Parameters
        ----------
        desiredPath : string
            The desired path file path you intend to use.

        Returns
        -------
        str
            String representation of a valid file path nearest to your desired path.
        """

        fileCount = 0
        desiredName = desiredPath.split('/')[-1] 
        newFileName = desiredName
        outputDir = desiredPath[:len(desiredPath)-len(newFileName)]

        if not os.path.isdir(outputDir):
            print(f"The path: {outputDir} doesn't exist, creating it now...")
            os.makedirs(outputDir)

        newFileName = str(desiredName)
        while os.path.exists(os.path.join(outputDir, newFileName)):
            if fileCount != 0:
                oldFilePrefix = f"({fileCount})"
                newFileName = newFileName[len(oldFilePrefix):]

            fileCount += 1
            filePrefix = f"({fileCount})"
            newFileName = filePrefix+newFileName

        if newFileName != desiredName:
            print(f"The file {desiredName} already exists, to prevent loss of data we will use {newFileName} instead")
        return os.path.join(outputDir, newFileName)

    def __isImgFile(self, filePath):
        validImgFileType = ["png", "jpeg", "gif"]
        pass #TODO: Make method for checking if file path is image file, useful for set instructions, etc where could be text or img

    def __convertResolution(self, resStr):
        """
        Function for converting resolution strings.

        Parameters
        ----------
        resStr : str
            A resolution string, formatted "widthxheight". I.E.: "1920x1080"

        Returns
        -------
        An integer tuple, (width, height)
        """

        if type(resStr) == str:
            resTuple = resStr.strip().split('x')
            resTuple = (int(resTuple[0]), int(resTuple[1]))

            return resTuple
        elif type(resStr) == tuple or type(resStr) == list:
            return (resStr[0], resStr[1])
        else:
            raise ValueError(f"Resolution string must be a string or int tuple, {type(resStr)} was received.")

    def __formatKeyPress(self, keyPress):
        """
        Takes a keyPress str, returns its associated value from keyInputReference if specified.

        See Also
        --------
        PsychopyTask.__init__ - runKeyReference parameter
        """

        if keyPress in self.keyInputReference:
            return self.keyInputReference[keyPress]
        return keyPress

if __name__ == "__main__":
    pass