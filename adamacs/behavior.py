"""Tables related to behavioral data.

During some recordings behavioral data is recorded.
This module organizes the different types of behavioral
raw data and relates them to the Recording.
"""

import datajoint as dj
import element_data_loader.utils #github.com/datajoint/element-data-loader

import scipy.io as spio
import numpy as np
import pathlib
from adamacs import db_prefix, session


schema = dj.schema(db_prefix + 'behavior')


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
	trial_type: varchar(16)
	---
	trial_type_description: varchar(256)
	"""

@schema
class Trial(dj.Imported):
	definition = """
	# CB modeled after example bpod datastructure
	# each recording has a list of trials
	-> session.Recording
	trial : smallint # trial number (1-based indexing)
	---
	start_time : float  # (second) relative to the start of the recording
	stop_time :  float  # (second) relative to the start of the recording
	"""


@schema
class EventType(dj.Lookup):
	definition = """
	event_type: varchar(16)
	---
	event_type_description='': varchar(256)
	"""

	contents = [('WaitForPosTriggerSoftCode', ''), ('CueDelay', '')]


@schema
class Event(dj.Imported):
	definition = """
	-> session.Recording
	-> EventType
	event_start_time: decimal(8, 4)   # (s) from recording start
	---
	event_end_time=null: decimal(8, 4)   # (s) from recording start
	"""


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
		variable_name: varchar(16)
		---
		variable_value: varchar(2000)
		"""

@schema
class BehaviorIngest(dj.Imported):
	definition = """
	-> session.Recording
	"""
	def make(self, key): # reading bpod data to populate
		# could model dir navigation after element_array_ephys
		# which uses config file for root dir and csv for relative paths
		# https://github.com/datajoint/workflow-array-ephys/blob/main/workflow_array_ephys/paths.py
		bpod_root_dir = pathlib.Path(get_beh_root_dir(key))
		bpod_sess_dir = pathlib.Path(get_beh_sess_dir(key))
		bpod_dir = find_full_path(bpod_root_dir,bpod_sess_dir)

		for file in os.listdir(bpod_dir): if filename.endswith(".mat"):
			trial_info = load_bpod_matfile(key, bpod_dir + file)
		Trial.insert(trial_info, ignore_extra_fields=True)
		Event.insert(trial_info, ignore_extra_fields=True)

# --------------------- HELPER LOADER FUNCTIONS -----------------

# see full example here:
# https://github.com/mesoscale-activity-map/map-ephys/blob/master/pipeline/ingest/behavior.py

def load_bpod_matfile(key, matlab_filepath):
	"""
	Loading routine for behavioral file, bpod .mat
	"""
	#Loading the file
	SessionData = spio.loadmat(matlab_filepath.as_posix(),
                            squeeze_me=True, struct_as_record=False)['SessionData']

	# Add to dict for insertion
  for trial in range(SessionData.nTrials):
  	trial_info['start_time'] = SessionData.RawData.OriginalEventTimestamps[trial]

  return trial_info


''' NOTES on bpod example file:
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