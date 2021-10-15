"""Tables related to behavioral data.

During some recordings behavioral data is recorded.
This module organizes the different types of behavioral
raw data and relates them to the Recording.
"""

import datajoint as dj
from adamacs import session

schema = dj.schema()

@schema
class RecordingBpod(dj.Manual):
    definition = """
    -> session.Recording
    ---
    recording_dir            : varchar(1000)       # Path to the data directory for a particular session
    """
