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

# # Subject Related Data

# ## Login

# +
from adamacs import utility, nbgui, subject
import datajoint as dj

"""If you are don't have your login information, contact the administrator."""
dj.config['database.host'] = '172.26.128.53'  # Put the server name between these apostrophe
dj.config['database.user'] = 'danielmk'  # Put your user name between these apostrophe
dj.config['database.password'] = ''  # Put your password between these apostrophe
dj.conn()
utility.activate_many(name='tutorial')
sub, lab, protocol, line, mutation, user, project, subject_genotype, subject_death = (
    subject.Subject(), subject.Lab(), subject.Protocol(), subject.Line(), subject.Mutation(), subject.User(),
    subject.Project(), subject.SubjectGenotype(), subject.SubjectDeath()
    )
# -

# ## Subject Entry Sheet

"""Run this cell to load the subject entry sheet."""
mouse_gui = nbgui.MouseEntrySheet()
mouse_gui.app

# ## Lab Entry

# +
"""Run this cell to insert a single laboratory into the database.
USE ONLY IF YOU KNOW WHAT YOU ARE DOING!
Insert the data of the laboratory you want to enter into the following 4 lines.
"""
lab_key = 'Beck'  # Short, unique identifier for the lab. Maximum 8 characters. Example: 'Rose'.
lab_name = 'Neuronal input-output computation during cognition'  # A longer, more descriptive name for the laboratory.
institution = 'Institute for Experimental Epileptology and Cognition Research'  # The institution the laboratory belongs to.
address = 'Venusberg-Campus 1, 53127 Bonn'  # The postal address of the laboratory.

lab.insert1((lab_key, lab_name, institution, address))
# -

# ## Protocol Entry

# +
"""Run this cell to insert a single protocol into the database.
USE ONLY IF YOU KNOW WHAT YOU ARE DOING!
Insert the data of the protocol you want to enter into the following 2 lines.
"""
protocol_key = 'LANUF3'  # Short, unique identifier for the protocol. Maximum 16 characters.
protocol_description = 'Another dummy protocol ID for testing purposes'  # Description of the protocol.

protocol.insert1((protocol_key, protocol_description))
# -

# ## Line Entry

# +
"""Run this cell to insert a single line into the database.
USE ONLY IF YOU KNOW WHAT YOU ARE DOING!
Insert the data of the laboratory you want to enter into the following 4 lines."""
line_key = 'Thy1-Gcamp6'  # Short, unique identifier for the line.
line_description = 'Gcamp6-ThyC57BL/6J-Tg(Thy1-GCaMP6s)GP4.12Dkim/J'  # Description of the line.
target_phenotype = 'wt/tg'  # The target phenotype of the line.
is_active = True  # Whether or not the line is actively breeding.

line.insert1((line_key, line_description, target_phenotype, is_active))
# -

# ## Mutation Entry

# +
"""Run this cell to insert a single mutation into the database.
USE ONLY IF YOU KNOW WHAT YOU ARE DOING!
Insert the data of the laboratory you want to enter into the following 3 lines."""
line_key = 'Thy1-Gcamp6'  # The mouse line that has the mutation.
mutation_key = 'Thy1-Gcamp6'  # An identifying name for the mutation.
description = 'Tg(Thy1-GCaMP6s)GP4.12Dkim'  # A description of the mutation.

mutation.insert1((line_key, mutation_key, description))
# -

# ## User Entry

# +
"""Run this cell to insert a single user into the database.
Note that this user refers to the user that handles a subject, not necessarily as database user.
USE ONLY IF YOU KNOW WHAT YOU ARE DOING!
Insert the data of the laboratory you want to enter into the following 2 lines."""
user_key = 'natashak'
lab_key = 'Rose'

user.insert1((user_key, lab_key))
# -

# ## Project Entry

# +
"""Run this cell to insert a single project into the database.
USE ONLY IF YOU KNOW WHAT YOU ARE DOING!
Insert the data of the laboratory you want to enter into the following 2 lines."""
project_key = 'TEC'
project_description = 'Trace Eyeblink Conditioning'

project.insert1((project_key, project_description))
# -

# ## Subject Genotype Entry

# +
"""Run this cell to assign a genotype to the mutation of a subject.
USE ONLY IF YOU KNOW WHAT YOU ARE DOING!
Insert the data of the laboratory you want to enter into the following 4 lines.""" 
subject_key = ''
line_key = ''
mutation_key = ''
genotype = ''

subject_genotype.insert1((subject_key, line_key, mutation_key, genotype))
# -

# ## Subject Death Entry

# +
"""Run this cell to assign a death date to a subject.
USE ONLY IF YOU KNOW WHAT YOU ARE DOING!
Insert the data of the laboratory you want to enter into the following 4 lines.""" 
subject_key = ''
death_date = ''
case = ''

subject_death.insert1((subject_key, death_date, case))
# -

# ## Fetch

sub

mouse_gui.rows

sub


