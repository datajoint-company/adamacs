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

# # Pipeline Activation

# ## Setup

# First, login information. If you are don't have your login information, contact the administrator. To set this information, you can
# 1. One can either change to a directory with a local config file `dj_local_conf.json`, example below.
# 2. Set these permissions on a machine globally (see [documentation](https://docs.datajoint.org/python/v0.13/setup/01-Install-and-Connect.html))
# 3. Set these values for each session.
#
# Example local config:
# ```json
# {
#     "database.host": "host",
#     "database.password": "pass",
#     "database.user": "USER",
#     "database.port": 3306,
#     "database.reconnect": true,
#     "connection.init_function": null,
#     "connection.charset": "",
#     "loglevel": "INFO",
#     "safemode": true,
#     "fetch_format": "array",
#     "display.limit": 12,
#     "display.width": 14,
#     "display.show_tuple_count": true,
#     "database.use_tls": null,
#     "enable_python_native_blobs": true,
#     "database.ingest_filename_short": "",
#     "database.ingest_filename_full": "",
#     "custom": {
#         "database.prefix": "adamacs_",
#         "dlc_root_data_dir": [
#             "/My/Local/Dir1",
#             "/My/Local/Dir2"
#         ],
#         "dlc_output_dir": "/My/Local/Dir3/optional",
#         "imaging_root_data_dir" : [
#             "/My/Local/Dir4",
#             "/My/Local/Dir5"
#         ],
#         "pyrat_user_token": "token",
#         "pyrat_client_token": "token"
#     }
# }
#
# ```

# Move to detect local config:

import datajoint as dj
dj.config

import os
if os.path.basename(os.getcwd())=='notebooks': os.chdir('..')
assert os.path.basename(os.getcwd())=='adamacs', ("Please move to the main directory")
import datajoint as dj; dj.conn()

# Alternatively, set login information during this session:

import datajoint as dj; import getpass
dj.config['database.host'] = '172.26.128.53'
dj.config['database.user'] = 'danielmk'
dj.config['database.password'] = getpass.getpass() # enter the password securily
dj.conn()

# ## Activation

# Next, activate the schema. 
#
# `adamacs/pipeline.py` includes all the pieces required to activate the whole pipeline via import.

from adamacs.pipeline import subject, session, surgery, session, behavior, equipment, \
                             imaging, scan, train, model

# To visualize the pipeline, we can generate diagrams for any combination of schemas.

dj.Diagram(session) + dj.Diagram(subject)

dj.Diagram(subject) + dj.Diagram(behavior) 

dj.Diagram(subject) + dj.Diagram(model)




