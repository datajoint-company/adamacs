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
class Lab(dj.Manual):
    definition = """
    lab             : varchar(8)   # short lab name   
    ---
    lab_name        : varchar(255)
    institution     : varchar(255)
    address         : varchar(255)
    """


@schema
class Protocol(dj.Manual):
    definition = """
    # protocol approved by some institutions like IACUC, IRB
    protocol                        : varchar(16)
    ---
    protocol_description=''         : varchar(255)
    """


@schema
class Line(dj.Manual):
    definition = """
    # animal line 
    line                        : varchar(32)
    ---
    line_description=''         : varchar(255)
    target_genotype=''          : varchar(255)
    is_active                   : boolean
    """


@schema
class Mutation(dj.Manual):
    definition = """
    # The mutations of animal lines
    -> Line
    mutation                    : varchar(32)
    ---
    description=''              : varchar(2000)
    """


@schema
class User(dj.Lookup):
    definition = """
    user                : varchar(32)
    ---
    -> Lab
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
    # CB: I see cage as an item in PyRAT export - relevant in analysis?

    subject                 : varchar(16)
    ---
    -> Lab
    earmark=''              : varchar(16)  # aka lab_id
    sex                     : enum('M', 'F', 'U')
    birth_date              : date
    subject_description=''  : varchar(1024)
    -> Line
    -> User
    -> Project
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
    death_date      : date       # death date
    cause           :    varchar(255)
    """
