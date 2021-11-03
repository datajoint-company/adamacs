"""Tables related to behavioral data.

During some recordings behavioral data is recorded.
This module organizes the different types of behavioral
raw data and relates them to the Recording.
"""

import datajoint as dj
import element_data_loader.utils #github.com/datajoint/element-data-loader

import scipy.io as sio
import numpy as np
import pathlib
from adamacs import session

schema = dj.schema()

@schema
class RecordingBpod(dj.Manual):
	definition = """ # CB: Does this recording_dir differ from session.Recording recording_dir?
	-> session.Recording
	---
	recording_dir : varchar(1024) # Path to the data directory for a particular session
	"""

@schema
class TrialType(dj.Lookup):
	definition = """
	trialtype_id: smallint
	---
	tialtype_name: varchar(32)
	"""

# CB modeled after example bpod datastructure
# each recording has a list of trials

@schema
class Trial(dj.Imported):
	definition = """
	-> session.Recording
	trial : smallint # trial number (1-based indexing)
	---
	start_time : datetime 
	stop_time :  datetime
	"""	

	@schema
	class Event(dj.Part):
		definition = """ 
		-> Session
		-> Trial
		event_time: decimal(8, 4)   # (s) from session start
		---
		event_states=null : varchar(32)  # see SessionData.TrialN.States  
		"""

	def make(self, key): # reading bpod data to populate
		# could model dir navigation after element_array_ephys
		# which uses config file and relative paths
		bpod_root_dir = pathlib.Path(get_beh_root_dir(key))
		bpod_sess_dir = pathlib.Path(get_beh_sess_dir(key))
		bpod_dir = find_full_path(bpod_root_dir,bpod_sess_dir)

		for file in os.listdir(bpod_dir): if filename.endswith(".mat"):
			# exp65533_AN_210627_1_MWM_20210808_155428.mat
			# experiment##_Initials_ProtocolDate_SubjID?
			bpod_file = sio.loadmat(file)['SessionData']
			for trial in np.arange(0,bpod_file['nTrials'][0][0][0][0])
				key['trial']=trial #currently zero-indexed
				key['start_time'] = bpod_file['TrialStartTimestamp'][0][0][0][trial]
				key['stop_time'] = bpod_file['TrialEndTimestamp'][0][0][0][trial]
				self.insert1(**key)


@schema
class TrialEvent(dj.Imported):
	definition = """
	-> Trial 
	-> Event
	"""
	
	
@schema
class BehaviorTrial(dj.Imported):
	definition = """
	-> Trial 
	---
	-> TrialType
	-> Outcome
	"""
	
	class TrialVariable(dj.Part):
		definition = """
		-> master
		-> Variable
		"""

''' NOTES:
bpod SessionData structure
	TrialTypes - 1,2,3,1,2,3
	TrialTypeNames - Visibile,Visible,Fading
	Info
		StateMachineVersion
		SessionDate
		SessionStartTime_UTC
		SessionStartTime_MATLAB
	nTrials (# trials in session, here 54)
	RawEvents (timestamps for each trial's state transitions/recorded events)
		Trial{1,n}.States #Which of these are important?
			WaitForPosTriggerSoftCode
			CueDelay
			WaitForResponse
			Port2RewardDelay
			Port2Reward
			CloseValves
			Drinking
			Port1RewardDelay
			Port3RewardDelay
			Port4RewardDelay
			Port5RewardDelay
			Port6RewardDelay
			Port7RewardDelay
			Port8RewardDelay
			Port1Reward
			Port3Reward
			Port4Reward
			Port5Reward
			Port6Reward
			Port7Reward
			Port8Reward
			Punish
			Punishexit
			EarlyWithdrawal
		Trial{1,n}.Events
			Port4In
			Port4Out
			SoftCode10
			Tup
			Port2In
			Port2Out
	RawData (copy of raw data from state machine)
	TrialStartTimestamp (time when trial started on Bpod's clock)
		Note: Timestamps in RawEvents are relative to each trial's start
	TrialEndTimestamp
	SettingsFile (the settings file you selected in the launch manager)
	Notes
	MarkerCodes
	CurrentSubjectName
	TrialSettings
		GUI
		GUIMeta
		GUIPanels
		polling
		debug
		debugvis
		Data
		arm_number
		arm_baited_orig
		arm_baited
		SF
		rotation
		position
		StimAlpha
	StimPos
		TriggerLocPix
		TriggerLocOptitrackHitbox
		TriggerLocOptitrackCenter
		TriggerLocOptitrackCircleHitRadius
		tform
'''