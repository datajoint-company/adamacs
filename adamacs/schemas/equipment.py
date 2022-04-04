"""Tables related to equipment.

We use a variety of different equipment 
"""
import datajoint as dj
from .. import db_prefix
# db_prefix + 'equipment'
schema = dj.schema()


# -------------- Table declarations --------------


@schema
class Equipment(dj.Manual):
    definition = """
    scanner: varchar(32)
    """