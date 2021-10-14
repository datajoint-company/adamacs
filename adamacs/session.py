"""Tables related to a session.

During a session, a user acquires data from a single animal.
The exact kinds of data acquired depend on a variety of factors
and might change over time.
"""

import datajoint as dj

schema = dj.schema()

@schema
class Session(dj.Manual):
    definition = """
    -> Subject
    session_datetime: datetime(3)
    """


@schema
class SessionUser(dj.Manual):
    definition = """
    -> Session
    -> User
    """

@schema
class SessionDirectory(dj.Manual):
    definition = """
    -> Session
    ---
    session_dir: varchar(256)       # Path to the data directory for a particular session
    """


@schema
class ProjectSession(dj.Manual):
    definition = """
    -> Project
    -> Session
    """
