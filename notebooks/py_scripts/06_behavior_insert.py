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
dj.conn()

# ### Imports and activation
#
# Importing schema from `adamacs.pipeline` automatically activates relevant schema.

import datajoint as dj
from adamacs.pipeline import subject, session, surgery, scan, event, trial
from adamacs import utility
from adamacs.ingest import behavior as ibe

# Assign easy names for relevant tables

sub, lab, protocol, line, mutation, user, project, subject_genotype, subject_death = (
    subject.Subject(), subject.Lab(), subject.Protocol(), subject.Line(), 
    subject.Mutation(), subject.User(), subject.Project(), subject.SubjectGenotype(), 
    subject.SubjectDeath())

# +
event_types = ['main_track_gate', 'shutter', 'mini2p_frames', 'mini2p_lines', 'mini2p_volumes', 'aux_bpod_cam',
               'aux_bpod_visual', 'aux_bpod_reward', 'aux_bpod_tone']

for e in event_types:
    event.EventType.insert1({'event_type': e, 'event_type_description': ''}, skip_duplicates=True,)
# -

# ## Ingesting behavior

ibe.ingest_aux("sess9FB2LN5C")

event.Event()

isess.ingest_session_scan('sess9FB2LN5C', verbose=True)

session.Session * session.SessionDirectory

key='scan9FB2LN5C'
(scan.Scan & f'scan_id=\"{key}\"')

scan.ScanInfo.populate()

# `CB DEV NOTE:` In demo file, there are no `scan.motor_position_at_zero` values. Set to 0 here to avoid downstream type errors when adding. Future would should set these to null when not present and revise downstream code.

scan.ScanInfo()

scan.ScanInfo.Field()

# Note the relative path below:

scan.ScanInfo.ScanFile()


