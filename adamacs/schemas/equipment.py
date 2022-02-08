"""Tables related to equipment.

We use a variety of different equipment 
"""
import datajoint as dj

from .. import db_prefix

schema = dj.schema(db_prefix + 'equipment')


# -------------- Table declarations --------------


@schema
class Equipment(dj.Manual):
    definition = """
    equipment_id             : int unsigned
    ---
    """


@schema
class Camera(dj.Manual):
    definition = """
    -> Equipment
    ---
    camera_type             : varchar(256)
    model=''                : varchar(256)
    description=''          : varchar(256)
    """


@schema
class RetireEquipment(dj.Manual):
    definition = """
    -> Equipment
    ---
    retire_date            : date
    """
