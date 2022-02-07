"""Tables related to a session.

During a Session, a user acquires data from a single animal.
Data is acquired during multiple Recordings.
The exact kinds of data acquired depend on a variety of factors
and might change over time.
"""

import datajoint as dj
import importlib
import inspect

schema = dj.schema()
_linking_module = None

# ------------------ Activation ------------------


def activate(schema_name, create_schema=True, create_tables=True,
             linking_module=None):
    """
    activate(schema_name, create_schema=True, create_tables=True, linking_module=None)
        :param schema_name: schema name on the database server
        :param create_schema: when True, create schema if it does not yet exist
        :param create_tables: when True, create tables if they do not yet exist
        :param linking_module: a module module containing required dependencies
            Upstream tables:
                + Subject: the subject with which an experimental session is associated
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
class Session(dj.Manual):
    definition = """
    -> subject.Subject
    session_datetime: datetime(3)
    """


@schema
class SessionDirectory(dj.Manual):
    definition = """
    -> Session
    ---
    session_dir: varchar(256) # Path to the data directory for a particular session
    """


@schema
class ProjectSession(dj.Manual):
    definition = """
    -> subject.Project
    -> Session
    """
