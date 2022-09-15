# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3.8.13 ('bon')
#     language: python
#     name: python3
# ---

# # File Ingestion

# ## Setup

# Using local config file (see [01_pipeline](./01_pipeline.ipynb))

import os
# change to the upper level folder to detect dj_local_conf.json
if os.path.basename(os.getcwd())=='notebooks': os.chdir('..')
assert os.path.basename(os.getcwd())=='adamacs', ("Please move to the main directory")
from adamacs.pipeline import subject, behavior

# Manual entry

# Manual Entry
import datajoint as dj; import getpass
dj.config['database.host'] = '172.26.128.53'        # Put the server name between these apostrophe
dj.config['database.user'] = 'danielmk'             # Put your user name between these apostrophe
dj.config['database.password'] = getpass.getpass(prompt='Database password:')
dj.conn()

# ### BPod Path Setup

# Your `dj.config` file should have a section for your BPod root directory under `custom`: `exp_root_data_dir`. This is a list of one or more paths where the ingestion tool will look for the relative paths it is given.

# +
import datajoint as dj
from element_interface.utils import find_full_path
from adamacs.pipeline import session, event, trial
from adamacs.ingest.bpod import Bpodfile
from adamacs.paths import get_experiment_root_data_dir

bpod_path = "scan9FB2LN5C_WEZ-8701_StimArenaMaster_20220318_165447.mat"
root_dirs = dj.config["custom"]["exp_root_data_dir"]
bpod_path_full = find_full_path(get_experiment_root_data_dir(),bpod_path)

print(f"Root: {root_dirs}\nFull: {bpod_path_full}")
# -

# ### Initial check of tables

# +
from adamacs.pipeline import session, event, trial

session.Session.delete()
print('Sessions:', len(session.Session()))
print('Trials  :', len(trial.Trial()))
print('Events  :', len(event.Event()))
# -

# ## Automated BPod ingestion

# The function is designed ask for a confirmation before entered into the schema.

bpod_path = "scan9FB2LN5C_WEZ-8701_StimArenaMaster_20220318_165447.mat"
bpod_object = Bpodfile(bpod_path)
bpod_object.ingest()

# Check that insertion worked:

trial.TrialEvent & 'trial_id=1'

# We can also interact with bpod objects. For example:

bpod_object.trial(1).attributes

bpod_object.trial(1).events

# # Add Harp recording

from adamacs.pipeline import behavior, event
event_recording = event.BehaviorRecording.fetch('KEY')[0]
behavior.HarpRecording()

behavior.HarpRecording.populate()

behavior.HarpRecording.Channel()


