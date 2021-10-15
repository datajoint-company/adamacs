"""Tables related to a session.

During a Session, a user acquires data from a single animal.
Data is acquired during multiple Recordings.
The exact kinds of data acquired depend on a variety of factors
and might change over time.
"""

import datajoint as dj
from adamacs import subject

schema = dj.schema()

@schema
class Session(dj.Manual):
    definition = """
    -> subject.Subject
    session_datetime: datetime(3)
    """


@schema
class SessionUser(dj.Manual):
    definition = """
    -> Session
    -> subject.User
    """


@schema
class Recording(dj.Manual):
    definition = """
    -> Session
    recording                : tinyint unsigned
    ---
    recording_dir            : varchar(1000)       # Path to the data directory for a particular session
    """


@schema
class ProjectSession(dj.Manual):
    definition = """
    -> subject.Project
    -> Session
    """

