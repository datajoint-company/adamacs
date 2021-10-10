
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