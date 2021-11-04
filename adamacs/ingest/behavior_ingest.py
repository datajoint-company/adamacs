import os
import pathlib

import datajoint as dj
import element_data_loader.utils #github.com/datajoint/element-data-loader

from adamacs import db_prefix, session, behavior

import scipy.io as spio
import numpy as np


schema = dj.schema(db_prefix + 'behavior_ingest')

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

		bpod_filepath = next(bpod_dir.glob('*.mat'))
		trial_info = load_bpod_matfile(key, bpod_filepath )
		behavior.Trial.insert(trial_info, ignore_extra_fields=True)
		behavior.Event.insert(trial_info, ignore_extra_fields=True)

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

	# Add to dict for insertion. For example:
  # for trial in range(SessionData.nTrials):
  # 	trial_info['start_time'] = SessionData.RawData.OriginalEventTimestamps[trial]
  # return trial_info