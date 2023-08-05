"""
Authors: Brandon Egger

This script turns common Psychopy task types into easy to implement objects.

SCN Lab Information:
    University of Iowa, 
    Iowa City, IA
    SCN Lab, Dpt. of Psychological and Brain Sciences

    Web: https://wiki.uiowa.edu/display/scnlab/SCN+Lab+Home
"""

import datetime
from psychopy import data

from SimplePsycho.PsychopyManager import PsychopyTask

#TODO, add a run function for each type of screen, run welcome, run instructions, etc. that way the start() function is
# simply, runWelcome(), runInstructions(), runVideo(videoName), etc.
#Each of these functions will check whether it can be done, and likewise will determine whether a dataset can be made
#Also create a setupColumns() function which goes through the runStimulus dictionary, checks which elements are present,
#and creates the necessary columns for it

class VideoTask(PsychopyTask):
    """
    VideoTask structure
    """

    dfColumns = ["date", "subject_id", "trial", "trial_start", "trial_end", "trial_duration", "trial_duration_compared",
                  "video", "video_start", "video_end", "video_duration", "video_duration_compared", 
                  "response_value", "response_start", "response_end", "response_duration", "response_duration_compared",
                  "fixation_start", "fixation_end", "fixation_duration", "fixation_duration_compared",
                  "run_start", "run_end", "run_duration", "run_duration_compared", "trigger_time"]

    def __init__(self, subject, taskName,runName, runStimulus={}, runTiming={}, runKeyReference={}, interruptKeys=[],
                 monitorRes="1920x1080", screenNum=0, fullScreen=False, recordMicrophone=False, 
                 toPreloadStim = True, stimulusDir = None, outputsDir = None):
        """
        See Also
        --------
        PsychopyManagers.PsychopyTask.__init__()
        """

        super().__init__(subject, taskName,runName, runKeyReference, interruptKeys, VideoTask.dfColumns, 
                         monitorRes, screenNum, fullScreen, toPreloadStim, stimulusDir, outputsDir)

        self.instructionStim, self.welcomeStim, self.triggerStim, self.videoStim, self.responseStim, self.fixationStim, self.audioAlert = (None,None,None,None,None,None,None)
        if "instruction" in runStimulus:
            self.setInstructionStim(runStimulus["instruction"], toPreloadStim)
        if "welcome" in runStimulus:
            self.setWelcomeStim(runStimulus["welcome"], toPreloadStim)
        if "trigger" in runStimulus:
            self.setTriggerStim(runStimulus["trigger"], toPreloadStim)
        if "video" in runStimulus:
            self.setVideoStim(runStimulus["video"], toPreloadStim)
        if "response" in runStimulus:
            self.setResponseStim(runStimulus["response"], toPreloadStim)
        if "fixation" in runStimulus:
            self.setFixationStim(runStimulus["fixation"], toPreloadStim)
        if "audio" in runStimulus:
            self.setAudioAlert(runStimulus["audio"], toPreloadStim)

        self.instructionWait, self.welcomeWait, self.triggerWait, self.videoWait, self.responseWait, self.fixationWait = (None,None,None,None,None,None)
        if "instruction" in runTiming:
            self.setInstructionWait(runTiming["instruction"])
        if "welcome" in runTiming:
            self.setWelcomeWait(runTiming["welcome"])
        if "trigger" in runTiming:
            self.setTriggerWait(runTiming["trigger"])
        if "video" in runTiming:
            self.setVideoWait(runTiming["video"])
        if "response" in runTiming:
            self.setResponseWait(runTiming["response"])
        if "fixation" in runTiming:
            self.setFixationWait(runTiming["fixation"])

        self.exportCSV()
        self.recordMic = recordMicrophone

    #Functional:
    def start(self):
        date, runStart, runEnd, runDuration, triggerStart = (data.getDateStr(), None,None,None, None)
        runExpectedDuration = 0

        self.runInstructions()
        self.runWelcome()

        triggerEnd = self.runTriggerWait()
        runStart = datetime.datetime.now()

        trialNum = 1

        for video in self.videoStim:
            print(f"Now playing: {video}")
            if self.recordMic:
                self.startAudioCapture(f"response_to_video_{video}")

            #Do trial. save data
            self.addDataPoint("date", date)
            self.addDataPoint("subject_id", self.getSubjectID())
            self.addDataPoint("trigger_time", triggerEnd)
            self.addDataPoint("run_start", self.dateTimeStr(runStart))
            self.addDataPoint("trial", trialNum)
            self.addDataPoint("video", video)
            trialStart = datetime.datetime.now()
            self.addDataPoint("trial_start", self.dateTimeStr(trialStart))
            trialExpectedDuration=0
            fixationExpected= self.runFixation()
            trialExpectedDuration+=fixationExpected
            runExpectedDuration+=fixationExpected

            if self.audioAlert != None:
                self.runStimulus("audio_alert", self.audioAlert, None)

            videoExpected = self.runVideo(video)
            trialExpectedDuration+=videoExpected
            runExpectedDuration+=videoExpected

            responseExpected = self.runResponse()
            trialExpectedDuration+=responseExpected
            runExpectedDuration+=responseExpected

            trialEnd = datetime.datetime.now()

            if self.recordMic:
                self.stopAudioCapture()
                self.saveAudioCapture(f"response_to_video_{video}")

            self.addDataPoint("trial_end", self.dateTimeStr(trialEnd))
            self.addDataPoint("trial_duration", (trialEnd-trialStart).total_seconds())
            self.addDataPoint("trial_duration_compared", (trialEnd-trialStart).total_seconds()-trialExpectedDuration)

            self.exportCSV()

            trialNum += 1

        runEnd = datetime.datetime.now()
        runDuration = (runEnd-runStart).total_seconds()
        runCompared = runDuration-runExpectedDuration
        for i in range(0,len(self.videoStim)):
            self.addDataPoint("run_end", self.dateTimeStr(runEnd))
            self.addDataPoint("run_duration", runDuration)
            self.addDataPoint("run_duration_compared", runCompared)

        self.exportCSV()

    def runInstructions(self):
        if self.instructionStim != None:
            start, end, duration, keys = self.runStimulus("instruction", self.instructionStim, self.instructionWait)
            if type(self.instructionWait) == int or type(self.instructionWait) == float:
                return self.instructionWait
            else:
                return duration
        return 0

    def runWelcome(self):
        if self.welcomeStim != None:
            start, end, duration, keys = self.runStimulus("welcome", self.welcomeStim, self.welcomeWait)
            if type(self.welcomeWait) == int or type(self.welcomeWait) == float:
                return self.instructionWait
            else:
                return duration
        return 0

    def runTriggerWait(self):
        triggerTime = self.dateTimeStr(datetime.datetime.now())

        if self.triggerStim != None:
            startTime, triggerTime, duration, keys = self.runStimulus("trigger", self.triggerStim, self.triggerWait)

        return triggerTime

    def runFixation(self, recordData = True):
        if self.fixationStim != None:
            startTime, endTime, duration, keys = self.runStimulus("fixation", self.fixationStim, self.fixationWait)

            if recordData:
                self.addDataPoint("fixation_start", startTime)
                self.addDataPoint("fixation_end", endTime)
                self.addDataPoint("fixation_duration", duration)
                if type(self.fixationWait) == int or type(self.fixationWait) == float:
                    self.addDataPoint("fixation_duration_compared", duration-self.fixationWait)
                else:
                    self.addDataPoint("fixation_duration_compared", 0)

            if type(self.fixationWait) == int or type(self.fixationWait) == float:
                return self.fixationWait
            else:
                return duration
        return 0



    def runVideo(self, vidName = None, recordData = True):
        #If none, self.videoStim can't be a list
        if type(self.videoStim) == list and vidName == None:
            raise ValueError("Parameter vidName must be provided when multiple video stim are present")
        if vidName == None:
            vidName = self.vidStim

        startTime,endTime,duration, keys = self.runStimulus(vidName, vidName, self.videoWait, logKeys=False)
        if recordData:
            self.addDataPoint("video_start", startTime)
            self.addDataPoint("video_end", endTime)
            self.addDataPoint("video_duration", duration)
            self.addDataPoint("video_duration_compared", duration - self.getStim(vidName, vidName, False, True).duration)

        return self.getStim(vidName, vidName, False, True).duration

    def runResponse(self, recordData = True):
        if self.responseStim != None:
            startTime, endTime, duration, keys = self.runStimulus("response", self.responseStim, self.responseWait, True)
            
            if recordData:
                self.addDataPoint("response_start", startTime)
                self.addDataPoint("response_end", endTime)
                self.addDataPoint("response_duration", duration)
                if type(self.responseWait) == int or type(self.responseWait) == float:
                    self.addDataPoint("response_duration_compared", duration-self.responseWait)
                else:
                    self.addDataPoint("response_duration_compared",0)
                self.addDataPoint("response_value", keys)

            if type(self.responseWait) == int or type(self.responseWait) == float:
                return self.responseWait
            else:
                return duration

        return 0

    def setInstructionWait(self, waitValue):
        self.instructionWait = waitValue
    
    def setWelcomeWait(self, waitValue):
        self.welcomeWait = waitValue

    def setTriggerWait(self, waitValue):
        self.triggerWait = waitValue

    def setVideoWait(self, waitValue):
        self.videoWait = waitValue

    def setResponseWait(self, waitValue):
        self.responseWait = waitValue

    def setFixationWait(self, waitValue):
        self.fixationWait = waitValue

    def setAudioAlert(self, stim, preload = False):
        self.getStim("audio_alert", stim, preload, True)
        self.audioAlert = stim

    def setInstructionStim(self, stimList, preload = False):
        self.getStim("instruction",stimList, preload, False)
        self.instructionStim = stimList

    def setWelcomeStim(self, stimList, preload = False):
        self.getStim("welcome", stimList, preload, False)
        self.welcomeStim = stimList

    def setTriggerStim(self, stimList, preload = False):
        self.getStim("trigger", stimList, preload, False)
        self.triggerStim = stimList

    def setVideoStim(self, stimList, preload = False):
        if type(stimList) == list:
            for vidStim in stimList:
                self.getStim(vidStim, vidStim, preload, True)
        else:
            self.getStim(stimList, stimList, preload, True)
        self.videoStim = stimList

    def setResponseStim(self, stimList, preload = False):
        self.getStim("response", stimList, preload, False)
        self.responseStim = stimList

    def setFixationStim(self, stimList, preload = False):
        self.getStim("fixation", stimList, preload, False)
        self.fixationStim = stimList