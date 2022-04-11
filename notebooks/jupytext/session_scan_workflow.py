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

# # Connect to the Database

# +
import datajoint as dj
from adamacs.schemas import subject, surgery
from adamacs import utility
from element_session import session_with_id
from element_calcium_imaging import scan
from adamacs.ingest import session as isess

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
session_with_id.activate('tutorial', create_schema=True, create_tables=True,
             linking_module=subject)
scan.activate('tutorial', create_schema=True, create_tables=True,
             linking_module=session_with_id)

# -

isess.ingest_session_scan('sess9FB2LN5C')

scan.ScanInfo().make(key='scan9FB2LN5C')

key='scan9FB2LN5C'

query = (scan.Scan & f"scan_id = '{key}'").fetch1()
query

scan.ScanInfo()

scan.ScanInfo.Field()

scan.ScanInfo.ScanFile()


