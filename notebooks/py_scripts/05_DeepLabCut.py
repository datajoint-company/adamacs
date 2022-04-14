# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: bonn
#     language: python
#     name: bonn
# ---

# # DeepLabCut Ingestion/Inference

# `Dev notes:` Currently, the path structure assumes you have one DLC project directory for all models, as specified within `adamacs.pipeline.get_dlc_root_data_dir`. The parallel function `get_dlc_processed_data_dir` can specify the output directory. 

# ## Setup

# ### Connect to the database

# If you are don't have your login information, contact the administrator.
#
# Using local config file (see [01_pipeline](./01_pipeline.ipynb)):

import os
# change to the upper level folder to detect dj_local_conf.json
if os.path.basename(os.getcwd())=='notebooks': os.chdir('..')
assert os.path.basename(os.getcwd())=='adamacs', ("Please move to the main directory")
import datajoint as dj; dj.conn()

# Manual entry:

# Manual Entry
import datajoint as dj; import getpass
dj.config['database.host'] = '172.26.128.53'        # Put the server name between these apostrophe
dj.config['database.user'] = 'danielmk'             # Put your user name between these apostrophe
dj.config['database.password'] = getpass.getpass()  # Put your password in the prompt
dj.config['custom']['dlc_root_data_dir'] = 'path'   # Path of your DLC project folder
dj.conn()

# ### Imports and activation
#
# Importing schema from `adamacs.pipeline` automatically activates items.

from adamacs.pipeline import subject, train, model

# + [markdown] tags=[]
# ## Ingesting videos and training parameters
#
# ### Automated
#
# Refer the `user_data` folder in the `adamacs` directory contains CSVs for inserting values into DeepLabCut tables.
#
# 1. `config_params.csv` is used for training parameter sets in `train.TrainingParamSet`. The following items are required, but others will also be passed to DLC's `train_network` function when called 
#     + ``
#     + `shuffle` - Training data shuffle 
#     + `trainingsetindex` - Training fraction in 0-indexed list
# 2. `train_videosets.csv` and `model_videos.csv` pass values to `train.VideoSet` and `model.VideoRecording` respectively.
# 3. `adamacs.ingest.dlc.ingest_dlc_items` will load each of these CSVs
#
# For more information, see [this notebook](https://github.com/CBroz1/workflow-deeplabcut/blob/main/notebooks/04-Automate_Optional.ipynb)
# -

from adamacs.ingest.dlc import ingest_dlc_items
ingest_dlc_items()

# ### Manual
#
# The same training parameters as above can be manually inserted as follows.

# +
import yaml
from element_interface.utils import find_full_path
from adamacs.paths import get_dlc_root_data_dir

paramset_idx = 1; paramset_desc='from_top_5iters'
config_path = find_full_path(get_dlc_root_data_dir(), 
                             'DLC_tracking/config.yaml')
with open(config_path, 'rb') as y:
    config_params = yaml.safe_load(y)
training_params = {'shuffle': '1',
                   'trainingsetindex': '0',
                   'maxiters': '5',
                   'scorer_legacy': 'False',
                   'maxiters': '5', 
                   'multianimalproject':'False'}
config_params.update(training_params)
train.TrainingParamSet.insert_new_params(paramset_idx=paramset_idx,
                                         paramset_desc=paramset_desc,
                                         params=config_params)
# -

key = {'subject': 'subject',
       'session_id': 'id',
       'recording_id': 1, 
       'scanner': 1, # Currently 'scanner' due to in equipment tables
       'recording_start_time': '0000-00-00 00:00:00'}
model.VideoRecording.insert1(key)
# do not include an initial `/` in relative file paths   
key.update({'file_path': 'relative/path'})
model.VideoRecording.File.insert1(key, ignore_extra_fields=True)

# ## Model Training

# The `TrainingTask` table queues up training. To launch training from a different machine, one needs to edit DLC's config files to reflect updated paths. For training, this includes `dlc-models/*/*/train/pose_cfg.yaml`
#
# `CB DEV NOTE:` I'm missing the following videos used to originally train the model:
# - top_video2022-02-17T15_56_10.mp4
# - top_video2022-02-21T12_18_09.mp4

key={'video_set_id': 1, 'paramset_idx':1,
     'training_id':1, # uniquely defines training task
     'project_path':'DLC_tracking/' # relative to dlc_root in dj.config
    }
train.TrainingTask.insert1(key, skip_duplicates=True)
train.TrainingTask()

# + tags=[]
train.ModelTraining.populate()
# -

train.ModelTraining()

# To start training from a previous instance, one would need to 
# [edit the relevant config file](https://github.com/DeepLabCut/DeepLabCut/issues/70) and
# adjust the `maxiters` paramset (if present) to a higher threshold (e.g., 10 for 5 more itterations).
# Emperical work from the Mathis team suggests 200k iterations for any true use-case.

# ## Tracking Joints/Body Parts

# The `model` schema uses a lookup table for managing Body Parts tracked across models.

model.BodyPart.heading

# This table is equipped with two helper functions. First, we can identify all the new body parts from a given config file.

from adamacs.paths import get_dlc_root_data_dir
config_path = get_dlc_root_data_dir()[0] + "/DLC_tracking/config.yaml"
model.BodyPart.extract_new_body_parts(config_path)

# Now, we can make a list of descriptions in the same order, and insert them into the table

bp_desc=['Body Center', 'Head', 'Base of Tail']
model.BodyPart.insert_from_config(config_path,bp_desc)

# If we skip this step, body parts (without descriptions) will be added when we insert a model. We can [update](https://docs.datajoint.org/python/v0.13/manipulation/3-Cautious-Update.html) empty descriptions at any time.

# ## Declaring a Model

# If training appears successful, the result can be inserted into the `Model` table for automatic evaluation.

model.Model.insert_new_model(model_name='from_top_5iters',dlc_config=config_path,
                             shuffle=1,trainingsetindex=0,
                             model_description='From Top, trained 5 iterations',
                             paramset_idx=1)

model.Model()

model.Model.BodyPart()

# ## Model Evaluation

# Next, all inserted models can be evaluated with a similar `populate` method, which will
# insert the relevant output from DLC's `evaluate_network` function.

model.ModelEvaluation.heading

# If your project was initialized in a version of DeepLabCut other than the one you're currently using, model evaluation may report key errors. Specifically, your `config.yaml` may not specify `multianimalproject: false`.

model.ModelEvaluation.populate()

model.ModelEvaluation()

# ## Pose Estimation

model.VideoRecording.File()

# For demonstration purposes, we'll make a shorter video that will process relatively quickly `ffmpeg`, a DLC dependency ([more info here](https://github.com/datajoint/workflow-deeplabcut/blob/main/notebooks/00-DataDownload_Optional.ipynb))

from adamacs.paths import get_dlc_root_data_dir
vid_path =  get_dlc_root_data_dir()[0] + '/DLC_tracking/videos/exp9FANLWRZ_top_video2022-02-21T12_18_09'
print(vid_path)
cmd = (f'ffmpeg -n -hide_banner -loglevel error -ss 0 -t 2 -i {vid_path}.mp4 '
       + f'-vcodec copy -acodec copy {vid_path}-copy.mp4')
import os; os.system(cmd)

# Next, we need to specify if the `PoseEstimation` table should load results from an existing file or trigger the estimation command. Here, we can also specify parameters accepted by the `analyze_videos` function as a dictionary. `task_mode` determines if pose estimation results should be loaded or triggered (i.e., load vs. trigger).

key = (model.VideoRecording & {'recording_id': '1'}).fetch1('KEY')
key.update({'model_name': 'from_top_5iters', 'task_mode': 'trigger'})
key

# The `PoseEstimationTask` table queues items for pose estimation. Additional parameters are passed to DLC's `analyze_videos` function.

model.PoseEstimationTask.insert_estimation_task(key,params={'save_as_csv':True})

model.PoseEstimation.populate()

model.PoseEstimation()

# By default, DataJoint will store the results of pose estimation in a subdirectory
# >  processed_dir / videos / device_<#>_recording_<#>_model_<name>
#
# Pulling processed_dir from `get_dlc_processed_dir`, and device/recording information 
# from the `VideoRecording` table. The model name is taken from the primary key of the
# `Model` table, with spaced replaced by hyphens.
#     
# We can get this estimation directly as a pandas dataframe.

model.PoseEstimation.BodyPartPosition()

model.PoseEstimation.get_trajectory(key)


