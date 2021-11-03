import datajoint as dj

schema = dj.schema()

@schema
class Lab(dj.Manual):
    definition = """
    lab             : varchar(8)   # short lab name   
    ---
    lab_name        : varchar(255)
    institution     : varchar(255)
    address         : varchar(255)
    time_zone       : varchar(64)  # If all labs in Bonn, could drop
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
    -> Lab
    ---
    lab_id=''               : varchar(16)
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

