"""Tables related to animal surgery

A User might perform one or more surgeries on a mouse.
During a surgery, several procedures might be performed. For
example, a viral injection at a certain stereotaxic coordinate
might be followed by a cranial window at different coordinates.
Anesthesia is required for a surgery. Analgesia must be given at
least once before the surgery but could be given multiple times
and might also be given after a surgery or might be associated
with other procedures."""

# from adamacs.utility import rspace_connect
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
class Anesthesia(dj.Manual):
    definition = """
    anesthesia        : varchar(16)
    ---
    long_name   : varchar(300)
    """


@schema
class Analgesia(dj.Manual):
    definition = """
    analgesia        : varchar(16) 
    ---
    long_name   : varchar(300)
    """


@schema
class Antagonist(dj.Manual):
    definition = """
    # The compound used to counter the anesthetic after surgery
    antagonist        : varchar(16)
    ---
    long_name   : varchar(300)
    """


@schema
class Surgery(dj.Manual):
    definition = """
    -> subject.Subject
    date              : date      
    ---
    weight            : float     # subject weight
    -> subject.User
    -> Anesthesia
    anesthesia_time   : time
    anesthesis_volume : float
    -> Antagonist
    antagonist_time   : time
    antagonist_volume : float
    """
    ''' Previous code for RSpace:
    def make(self, key):  #placeholder for RSpace query -> datajoint table
        rspace_doc = rspace_connect().get_documents(query='Filename_{}'.format(key))
        surgery_data = rspace_doc['contents']
        self.insert1()
        # Which other tables below will be populated from RSpace?
        # If any, consider making dj.Part tables to share the same RSpace query
    '''


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
    -> subject.Subject
    datetime   : datetime
    ---
    """


@schema
class Coordinates(dj.Manual):
    definition = """
    coordinates        : varchar(32)
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
