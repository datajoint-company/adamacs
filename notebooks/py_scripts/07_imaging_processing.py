# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Scanning Session Ingestion

# ## Setup

# ### Connect to the database

# If you are don't have your login information, contact the administrator.
#
# Using local config file (see [01_pipeline](./01_pipeline.ipynb)):

# +
import os
# change to the upper level folder to detect dj_local_conf.json
if os.path.basename(os.getcwd())=='notebooks': os.chdir('..')
assert os.path.basename(os.getcwd())=='adamacs', ("Please move to the main directory")
import datajoint as dj; dj.conn()

from adamacs.pipeline import subject, session, surgery, scan, event, trial, imaging
from adamacs import utility
from adamacs.ingest import behavior as ibe
import numpy as np
# -

# Manual entry:

# +
# Manual Entry
import datajoint as dj; import getpass
dj.config['database.host'] = '172.26.128.53'        # Put the server name between these apostrophe
dj.config['database.user'] = 'root'             # Put your user name between these apostrophe
dj.config['database.password'] = getpass.getpass()  # Put your password in the prompt
dj.conn()

from adamacs.pipeline import subject, session, surgery, scan, event, trial, imaging
from adamacs import utility
from adamacs.ingest import behavior as ibe
import numpy as np
# -

# ### Creating a Parameter Set

# What exactly happens during processing dependso on the parameter set. This is an example of a parameter set and its insert:

# +
# Insert the param_set
params_suite2p = {'look_one_level_down': 0.0,
                  'fast_disk': [],
                  'delete_bin': False,
                  'mesoscan': False,
                  'h5py': [],
                  'h5py_key': 'data',
                  'save_path0': [],
                  'subfolders': [],
                  'nplanes': 1,
                  'nchannels': 1,
                  'functional_chan': 1,
                  'tau': 1.0,
                  'fs': 10.0,
                  'force_sktiff': False,
                  'preclassify': 0.0,
                  'save_mat': False,
                  'combined': True,
                  'aspect': 1.0,
                  'do_bidiphase': False,
                  'bidiphase': 0.0,
                  'do_registration': True,
                  'keep_movie_raw': False,
                  'nimg_init': 300,
                  'batch_size': 500,
                  'maxregshift': 0.1,
                  'align_by_chan': 1,
                  'reg_tif': False,
                  'reg_tif_chan2': False,
                  'subpixel': 10,
                  'smooth_sigma': 1.15,
                  'th_badframes': 1.0,
                  'pad_fft': False,
                  'nonrigid': True,
                  'block_size': [128, 128],
                  'snr_thresh': 1.2,
                  'maxregshiftNR': 5.0,
                  '1Preg': False,
                  'spatial_hp': 50.0,
                  'pre_smooth': 2.0,
                  'spatial_taper': 50.0,
                  'roidetect': True,
                  'sparse_mode': False,
                  'diameter': 12,
                  'spatial_scale': 0,
                  'connected': True,
                  'nbinned': 5000,
                  'max_iterations': 20,
                  'threshold_scaling': 1.0,
                  'max_overlap': 0.75,
                  'high_pass': 100.0,
                  'inner_neuropil_radius': 2,
                  'min_neuropil_pixels': 350,
                  'allow_overlap': False,
                  'chan2_thres': 0.65,
                  'baseline': 'maximin',
                  'win_baseline': 60.0,
                  'sig_baseline': 10.0,
                  'prctile_baseline': 8.0,
                  'neucoeff': 0.7,
                  'xrange': np.array([0, 0]),
                  'yrange': np.array([0, 0])}

imaging.ProcessingParamSet.insert_new_params('suite2p', 1, 'basic params', params_suite2p)
# -

# ### Create and Run a Processing Task

imaging.ProcessingTask.insert1(('sessJ49456FR',
                                'scan7954564G',
                                1,
                                'DB_Testmouse1_2021-08-09_scan7954564G_sessJ49456FR',
                                'trigger'))

# To run all unprocessed processing task we call populate on processing:

imaging.Processing.populate(display_progress=True)
