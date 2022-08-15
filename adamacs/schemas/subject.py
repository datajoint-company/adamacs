import datajoint as dj
from .. import db_prefix

schema = dj.schema(db_prefix + 'subject')


# -------------- Table declarations --------------


@schema
class Lab(dj.Manual):
    definition = """
    lab             : varchar(8)   # short lab name, pyrat labid
    ---
    lab_name        : varchar(255)
    institution     : varchar(255)
    address         : varchar(255)
    """


@schema
class User(dj.Lookup):
    definition = """
    user_id        : int
    ---
    name           : varchar(32)
    initials=''    : varchar(2)  # Update after pyrat ingestion
    -> [nullable] Lab
    """


@schema
class Protocol(dj.Manual):
    definition = """
    # PyRAT licence number and title
    protocol                        : varchar(32)
    ---
    protocol_description=''         : varchar(255)
    """


@schema
class Line(dj.Manual):
    definition = """
    # animal line 
    line                        : int  # strain_id within PyRAT. Not name_id seen in GUI
    ---
    line_name=''                : varchar(64)
    is_active                   : enum('active','inactive','unknown')  # TODO BUGFIX expects float for unknown reason
    """


@schema
class Mutation(dj.Manual):
    definition = """
    # The mutations of animal lines
    -> Line
    mutation_id                 : int
    ---
    description=''              : varchar(32)
    """


@schema
class Project(dj.Lookup):
    definition = """
    project                 : varchar(32)
    ---
    project_description=''  : varchar(1024)
    """


@schema
class Subject(dj.Manual):
    definition = """
    # Animal Subject
    # Our Animals are not uniquely identified by their ID
    # because different labs use different animal facilities.

    subject                 : varchar(16)     # PyRat import uses this for earmark value
    ---
    earmark                 : varchar(16)     #
    sex                     : enum('M', 'F', 'U')  # Geschlecht
    birth_date              : varchar(32)          # Geb.
    generation=''           : varchar(64)     # Generation (F2 in example sheet)
    parent_ids              : tinyblob        # dict of parent_sex: parent_eartag
    -> User.proj(owner_id='user_id')          # Besitzer
    -> User.proj(responsible_id='user_id')    # Verantwortlicher
    -> Line                                   # Linie / Stamm
    -> Protocol
    """


@schema
class SubjectGenotype(dj.Manual):
    definition = """
    -> Subject
    -> Mutation
    ---
    genotype        : enum('wt/wt', 'wt/tg', 'tg/wt', 'tg/tg')
    """


@schema
class SubjectDeath(dj.Manual):
    definition = """
    -> Subject
    ---
    death_date      : date
    cause           : varchar(255)
    """
