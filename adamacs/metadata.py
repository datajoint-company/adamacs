import datajoint as dj

schema = dj.schema()

@schema
class Subject(dj.Manual):
    definition = """
    # Animal Subject
    # Our Animals are not uniquely identified by their ID
    # because different labs use different animal facilities.
    subject                 : varchar(32)
    -> Lab
    ---
    sex                     : enum('M', 'F', 'U')
    subject_birth_date      : date
    subject_description=''  : varchar(1024)
    # [nullable] cull_date    : date
    # [nullable] cull_method  : varchar(1024)
    # -> Line
    # -> User
    # -> Protocol
    # -> Project
    """

@schema
class Lab(dj.Manual):
    definition = """
    lab             : varchar(24)  #  Abbreviated lab name 
    ---
    lab_name        : varchar(255)   # full lab name
    institution     : varchar(255)
    address         : varchar(255)
    time_zone       : varchar(64)
    """

@schema
class Line(dj.Manual):
    definition = """
    line                    : varchar(32)	# abbreviated name for the line
    ---
    line_description=''     : varchar(2000)
    target_phenotype=''     : varchar(255)
    is_active               : boolean		# whether the line is in active breeding
    """

@schema
class User(dj.Lookup):
    definition = """
    user                : varchar(32)
    ---
    -> Lab
    """

@schema
class Protocol(dj.Lookup):
    definition = """
    # protocol approved by some institutions like IACUC, IRB
    protocol                : varchar(16)
    ---
    # -> ProtocolType
    protocol_description=''        : varchar(255)
    """

@schema
class Project(dj.Lookup):
    definition = """
    project                 : varchar(32)
    ---
    project_description=''         : varchar(1024)
    """