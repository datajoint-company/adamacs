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

# \* minor outstanding issue - confirmation message shows duplicate mutations
#
# ---
#
# First, change to directory with config file:

import os
# change to the upper level folder to detect dj_local_conf.json
if os.path.basename(os.getcwd())=='notebooks': os.chdir('..')
assert os.path.basename(os.getcwd())=='adamacs', ("Please move to the main directory")
from adamacs.pipeline import subject

# Checking length before run

# subject.User.delete(); subject.Protocol.delete()
# subject.Line.delete(); subject.Subject.delete()
print('User', len(subject.User()))
print('Protocol', len(subject.Protocol()))
print('Line', len(subject.Line()))
print('Mutation', len(subject.Mutation()))
print('Subject', len(subject.Subject()))
print('SubjectGenotype', len(subject.SubjectGenotype()))

from adamacs.ingest.pyrat import PyratIngestion

# PyratIngestion().get_animal("HSC-01*")
PyratIngestion().get_animal("HSC-01*")

print('User', len(subject.User()))
print('Protocol', len(subject.Protocol()))
print('Line', len(subject.Line()))
print('Mutation', len(subject.Mutation()))
print('Subject', len(subject.Subject()))
print('SubjectGenotype', len(subject.SubjectGenotype()))

PyratIngestion().get_animal("HSC-02*")

print('User', len(subject.User()))
print('Protocol', len(subject.Protocol()))
print('Line', len(subject.Line()))
print('Mutation', len(subject.Mutation()))
print('Subject', len(subject.Subject()))
print('SubjectGenotype', len(subject.SubjectGenotype()))


