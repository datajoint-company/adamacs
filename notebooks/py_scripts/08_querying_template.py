# ---
# jupyter:
#   jupytext:
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

# # Basic Querying Template
#
# Connect to the database with config file:

import os
if os.path.basename(os.getcwd())=='notebooks': os.chdir('..')
assert os.path.basename(os.getcwd())=='adamacs', ("Please move to the main directory")
import datajoint as dj; dj.conn()
from adamacs.pipeline import subject, session, surgery, session, behavior, equipment, \
                             imaging, scan, train, model

# Manually connect:

import datajoint as dj; import getpass
dj.config['database.host'] = '172.26.128.53'
dj.config['database.user'] = 'user'
dj.config['database.password'] = getpass.getpass() # enter the password securily
dj.conn()
from adamacs.pipeline import subject, session, surgery, session, behavior, equipment, \
                             imaging, scan, train, model

# ### How many mice?

query = subject.Subject()
query.fetch().size

# ### How many scans per mouse?

query = session.Session() * scan.Scan() & 'subject = "WEZ-8701"'
query.fetch().size

query


