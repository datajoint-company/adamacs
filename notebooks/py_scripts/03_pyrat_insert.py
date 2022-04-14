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

# # PyRAT subject ingestion

# ## Setup

# Using local config file (see [01_pipeline](./01_pipeline.ipynb))

import os
# change to the upper level folder to detect dj_local_conf.json
if os.path.basename(os.getcwd())=='notebooks': os.chdir('..')
assert os.path.basename(os.getcwd())=='adamacs', ("Please move to the main directory")
from adamacs.pipeline import subject

# Manual entry

# Manual Entry
import datajoint as dj; import getpass
dj.config['database.host'] = '172.26.128.53'        # Put the server name between these apostrophe
dj.config['database.user'] = 'danielmk'             # Put your user name between these apostrophe
dj.config['database.password'] = getpass.getpass(prompt='Database password:')
dj.config['custom']['pyrat_client_token'] = getpass.getpass(prompt="Pyrat client token:")
dj.config['custom']['pyrat_user_token'] = getpass.getpass(prompt="Pyrat user token:")
dj.conn()

# ## Initial check of tables

# subject.User.delete(); subject.Protocol.delete()
# subject.Line.delete(); subject.Subject.delete()
print('User', len(subject.User()))
print('Protocol', len(subject.Protocol()))
print('Line', len(subject.Line()))
print('Mutation', len(subject.Mutation()))
print('Subject', len(subject.Subject()))
print('SubjectGenotype', len(subject.SubjectGenotype()))

# ## Automated ingestion

from adamacs.ingest.pyrat import PyratIngestion

# This function permits wildcards when querying [the API](https://pyrat.uniklinik-bonn.de/pyrat-test/api/v2/specification/ui#/Listing/get_animals).
#
# The function is designed to list all proposed insertions and ask for a confirmation before entered into the schema.

PyratIngestion().ingest_animal("HSC-01*")

print('User', len(subject.User()))
print('Protocol', len(subject.Protocol()))
print('Line', len(subject.Line()))
print('Mutation', len(subject.Mutation()))
print('Subject', len(subject.Subject()))
print('SubjectGenotype', len(subject.SubjectGenotype()))

PyratIngestion().ingest_animal("HSC-02*")

# ## Confirm entry

print('User', len(subject.User()))
print('Protocol', len(subject.Protocol()))
print('Line', len(subject.Line()))
print('Mutation', len(subject.Mutation()))
print('Subject', len(subject.Subject()))
print('SubjectGenotype', len(subject.SubjectGenotype()))


