'''Tables related to animal surgery

An experimenter might perform one or more surgeries on a mouse. During a surgery, several procedures might be performed. For example, a viral injection at a certain stereotaxic
coordinate might be followed by a cranial window at different coordinates. Anesthesia is required for a surgery. Analgesia must be given at least once before the surgery but could
be given multiple times and might also be given after a surgery or might be associated with other procedures.'''

import datajoint as dj
from adamacs.subject import *

schema = dj.schema()

@schema
class Anesthesia(dj.Manual):
    definition = """
    name        : varchar(16)
    ---
    long_name   : varchar(300)
    """


@schema
class Analgesia(dj.Manual):
    definition = """
    name        : varchar(16) 
    ---
    long_name   : varchar(300)
    """

@schema
class Antagonist(dj.Manual):
    definition = """
    # The compound used to counter the anesthetic after surgery
    name        : varchar(16)
    ---
    long_name   : varchar(300)
    """


@schema
class Surgery(dj.Manual):
    definition = """
    -> Subject
    date        : date      
    ---
    weight      : float     # subject weight
    start       : time 
    finish      : time
    -> User
    -> Anesthesia
    anesthesia_time : time
    """

@schema
class SurgeryNote(dj.Manual):
    definition = """
    -> Surgery
    ---
    note    : varchar(30000)
    """


@schema
class Virus(dj.Manual):
    definition = """
    name        : varchar(16) 
    serotype    : varchar(64)
    ---
    long_name   : varchar(300)

    """


@schema
class AnalgesiaSubject(dj.Manual):
    definition = """
    -> Analgesia
    -> Subject
    datetime   : datetime
    ---
    
    """


@schema
class Coordinates(dj.Manual):
    definition = """
    location        : varchar(16)
    ---
    x_coordinate    : float  # in mm
    y_coordinate    : float  # in mm
    z_coordinate    : float  # in mm
    description=''  : varchar(300)
    """

@schema
class ViralInjection(dj.Manual):
    definition = """
    -> Surgery
    -> Virus
    -> Coordinates
    ---
    datetime   : time
    volume     : float  # in ul
    """


@schema
class CranialWindow(dj.Manual):
    definition = """
    -> Surgery
    ---
    time   : time
    """