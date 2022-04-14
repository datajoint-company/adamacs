"""Tables related to behavioral data.

During some recordings behavioral data is recorded.
This module organizes the different types of behavioral
raw data and relates them to the Recording.
"""

import datajoint as dj
from ..pipeline import session
from .. import db_prefix
# db_prefix + 'behavior'
schema = dj.schema(db_prefix + 'behavior')

__all__ = ['session', 'RecordingBpod', 'TrialType', 'Trial', 'EventType', 'Event',
           'TrialEvent', 'BehaviorTrial', 'db_prefix']

# -------------- Table declarations --------------


@schema
class RecordingBpod(dj.Manual):
    definition = """
    # CB: Does this recording_dir differ from session.Recording recording_dir?
    -> session.Session
    ---
    recording_dir : varchar(1024) # Path to the data directory for a particular session
    """


@schema
class TrialType(dj.Lookup):
    definition = """
    trial_type: varchar(16)
    ---
    trial_type_description: varchar(256)
    """


@schema
class Trial(dj.Imported):
    definition = """
    # CB modeled after example bpod datastructure
    # each recording has a list of trials
    -> session.Session
    trial : smallint # trial number (1-based indexing)
    ---
    start_time : float  # (second) relative to the start of the recording
    stop_time :  float  # (second) relative to the start of the recording
    """


@schema
class EventType(dj.Lookup):
    definition = """
    event_type: varchar(255)
    ---
    event_type_description='': varchar(256)
    """

    contents = [('WaitForPosTriggerSoftCode', ''), ('CueDelay', '')]


@schema
class Event(dj.Imported):
    definition = """
    -> session.Session
    -> EventType
    event_start_time: decimal(8, 4)   # (s) from recording start
    ---
    event_end_time=null: decimal(8, 4)   # (s) from recording start
    """


@schema
class TrialEvent(dj.Imported):

    definition = """
    -> Trial
    -> Event
    """


@schema
class BehaviorTrial(dj.Imported):
    definition = """
    -> Trial
    ---
    -> TrialType
    # -> Outcome
    """

    class TrialVariable(dj.Part):
        definition = """
        -> master
        variable_name: varchar(16)
        ---
        variable_value: varchar(2000)
        """
