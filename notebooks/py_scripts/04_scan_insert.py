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
#     display_name: bonn
#     language: python
#     name: bonn
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
from adamacs.pipeline import subject, session, surgery, scan
from adamacs import utility
from adamacs.ingest import session as isess

# Assign easy names for relevant tables

sub, lab, protocol, line, mutation, user, project, subject_genotype, subject_death = (
    subject.Subject(), subject.Lab(), subject.Protocol(), subject.Line(), 
    subject.Mutation(), subject.User(), subject.Project(), subject.SubjectGenotype(), 
    subject.SubjectDeath())

# ## Ingesting scan

#temporary step - insert placeholder values
equipment_placeholder = "Equipment"
location_placeholder = "Location"
from adamacs.pipeline import Equipment, Location
Equipment.insert1({'scanner' : equipment_placeholder}, skip_duplicates=True)
Location.insert1({'anatomical_location': location_placeholder}, skip_duplicates=True) 

isess.ingest_session_scan('sess9FB2LN5C')

session.Session * session.SessionDirectory

key='scan9FB2LN5C'
(scan.Scan & f'scan_id=\"{key}\"')

scan.ScanInfo.populate()

# `CB DEV NOTE:` In demo file, there are no `scan.motor_position_at_zero` values. Set to 0 here to avoid downstream type errors when adding. Future would should set these to null when not present and revise downstream code.

scan.ScanInfo()

scan.ScanInfo.Field()

# Note the relative path below:

scan.ScanInfo.ScanFile()
