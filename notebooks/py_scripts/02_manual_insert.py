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
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Subject Related Data

# `CB DEV NOTES`
# 1. Some table structures and data types changed for pyrat ingestion
# 2. The GUI didn't work for me. Maybe an error on my end.

# ## Login
#
# Either log in via a local config file (see [01_pipeline](./01_pipeline.ipynb)), or enter login information manually. If you are don't have your login information, contact the administrator.
#

# Local Config
import os
if os.path.basename(os.getcwd())=='notebooks': os.chdir('..')
assert os.path.basename(os.getcwd())=='adamacs', ("Please move to the main directory")
import datajoint as dj; dj.conn()

# Manual Entry
import datajoint as dj; import getpass
dj.config['database.host'] = '172.26.128.53'        # Put the server name between these apostrophe
dj.config['database.user'] = 'danielmk'             # Put your user name between these apostrophe
dj.config['database.password'] = getpass.getpass()  # Put your password in the prompt
dj.conn()

# ## Activation
# Next, import from `adamacs.pipeline` to activate the relevant schema.

# from adamacs.utility import *
# from adamacs.nbgui import *
from adamacs.pipeline import subject

# Assign easy names for relevant tables

sub, lab, protocol, line, mutation, user, project, subject_genotype, subject_death = (
    subject.Subject(), subject.Lab(), subject.Protocol(), subject.Line(), 
    subject.Mutation(), subject.User(), subject.Project(), subject.SubjectGenotype(), 
    subject.SubjectDeath()
    )

# ## Entry via GUI

"""Run this cell to load the subject entry sheet."""
mouse_gui = MouseEntrySheet()
mouse_gui.app

# ## Entry via `insert()`
#
# ### **WARNING** 
# Only run these manual entry cells if you know what you are doing!
#
# Strings for these values may be edited to insert single rows into corresponding tables.
#
# ### Lab

# +
lab_key = 'Rose'  # Short, unique identifier for the lab. Maximum 8 characters. Example: 'Rose'.
lab_name = 'Neuronal input-output computation during cognition'  # A longer, more descriptive name for the laboratory.
institution = 'Institute for Experimental Epileptology and Cognition Research'  # The institution the laboratory belongs to.
address = 'Venusberg-Campus 1, 53127 Bonn'  # The postal address of the laboratory.

lab.insert1((lab_key, lab_name, institution, address))
# -

# ### Protocol

# +
protocol_key = 'LANUF3'  # Short, unique identifier for the protocol. Maximum 16 characters.
protocol_description = 'Another dummy protocol ID for testing purposes'  # Description of the protocol.

protocol.insert1((protocol_key, protocol_description))
# -

# ### User Entry

# insert multiple entries
data = [{'user_id': 1, 'name': 'natashak', 'lab': 'Rose'},
        {'user_id': 2, 'name': 'georgejk', 'lab': 'Rose'}]
user.insert(data)

# ### Line/Mutation

# +
line_id = 1  # Unique identifier for the line.
line_name = 'Gcamp6-ThyC57BL/6J-Tg(Thy1-GCaMP6s)GP4.12Dkim/J'  # Description of the line.
is_active = 1  # Whether or not the line is actively breeding.

mutation_id = 2  # Unique identifier for the mutation.
mutation_description = 'Tg(Thy1-GCaMP6s)GP4.12Dkim'  # A description of the mutation.

line.insert1((line_id, line_name, is_active))
mutation.insert1((line_id, mutation_id, mutation_description))
# -

# ### Subject

# +
subject_id = 'Testmouse1'
earmark = ''
sex = 'F'
birth_date = ''
subject_description = ''
generation = ''
parents = {}
owner_id = ''
responsible_id = ''
line_id = ''
protocol_key = 'LANUF3'

sub.insert1((subject_id, earmark, sex, birth_date, subject_description, generation, 
             parents, owner_id, responsible_id, line_id, protocol_key))
# -

sub

# +
subject_id = 'WEZ-8701'
earmark = ''
sex = 'M'
birth_date = ''
subject_description = ''
generation = ''
parents = ''
owner_id = ''
responsible_id = ''
line_id = ''
protocol_key = 'LANUF3'

sub.insert1((subject_id, earmark, sex, birth_date, subject_description, generation, 
             parents, owner_id, responsible_id, line_id, protocol_key))
# -

# ### Subject Genotype

# +
subject = 'WEZ-8701'
line_id = 1
mutation_id = 2  # Unique identifier for the mutation.
genotype = 'wt/tg'  # The target phenotype of the line.

subject_genotype.insert1((subject, line_id, mutation_id, genotype))
# -

# ### Project Entry

# +
project_key = 'TEC'
project_description = 'Trace Eyeblink Conditioning'

project.insert1((project_key, project_description))
# -

# ### Subject Death

# +
subject = 'WEZ-8701'
death_date = '2010-12-01'
case = 'natural'

subject_death.insert1((subject, death_date, case))
# -

# ## Fetch

# ### As table

user * lab

sub

line * subject_genotype

subject_genotype

# ### As dictionary

# One item:

(sub & 'subject="Rose_ROS-0019"').fetch1()

# List of dictionaries:

(subject_genotype & 'subject="Rose_ROS-0019"').fetch(as_dict=True)

user


