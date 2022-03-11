import datajoint as dj
from .. import db_prefix

schema = dj.schema(db_prefix + 'subject')


# -------------- Table declarations --------------


@schema
class Lab(dj.Manual):
    definition = """
    lab             : varchar(8)   # short lab name, pyrad labid
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
    -> [nullable] Lab
    """


@schema
class Protocol(dj.Manual):
    definition = """
    # PyRAT licence number and title
    protocol                        : varchar(32)
    ---
    protocol_description=''         : varchar(64)
    """


@schema
class Line(dj.Manual):
    definition = """
    # animal line 
    line                        : varchar(32)
    ---
    line_name=''                : varchar(64)
    is_active                   : int
    """


@schema
class Mutation(dj.Manual):
    definition = """
    # The mutations of animal lines
    -> Line
    mutation_id                 : varchar(32)
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

    subject                 : varchar(16)  # PyRat import uses this for earmark value
    ---
    earmark=''              : varchar(16)  #
    sex                     : enum('M', 'F', 'U')  # Geschlecht
    birth_date=''           : varchar(32) # date  # Geb.
    subject_description=''  : varchar(1024)
    generation=''           : varchar(64)     # Generation (F2 in example sheet)
    parent_ids=NULL         : tinyblob        # dict of parent_sex: parent_eartag
    -> [nullable] User.proj(owner_id='user_id')          # Besitzer
    -> [nullable] User.proj(responsible_id='user_id')    # Verantwortlicher
    -> [nullable] Line                 # Linie / Stamm
    -> [nullable] Protocol
    """


@schema
class SubjectGenotype(dj.Manual):
    definition = """
    -> Subject
    -> Mutation
    ---
    genotype        : varchar(8)
    """


@schema
class SubjectDeath(dj.Manual):
    definition = """
    -> Subject
    ---
    death_date      : date       # death date
    cause           :    varchar(255)
    """
