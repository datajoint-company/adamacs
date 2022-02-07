"""Tables related to behavioral data.

During some recordings behavioral data is recorded.
This module organizes the different types of behavioral
raw data and relates them to the Recording.
"""

import datajoint as dj
import importlib
import inspect

schema = dj.schema()

_linking_module = None

# ------------------ Activation ------------------


def activate(schema_name, *, create_schema=True, create_tables=True,
             linking_module=None):
    """
    activate(schema_name, create_schema=True, create_tables=True, linking_module=None)
        :param schema_name: schema name on the database server
        :param create_schema: when True, create schema if it does not yet exist
        :param create_tables: when True, create tables if they do not yet exist.
        :param linking_module: a module name containing the required dependencies
             Upstream tables:
                + Session: parent table to RecordingBpod, identifying a session
    """
    if isinstance(linking_module, str):
        linking_module = importlib.import_module(linking_module)
    assert inspect.ismodule(linking_module), "The argument 'dependency' must "\
                                             + "be a module's name or a module"

    global _linking_module
    _linking_module = linking_module

    schema.activate(schema_name, create_schema=create_schema,
                    create_tables=create_tables,
                    add_objects=linking_module.__dict__)

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
