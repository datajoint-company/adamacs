"""Tables related to equipment.

We use a variety of different equipment 
"""

import datajoint as dj

schema = dj.schema()

@schema
class EquiptmentID(dj.Manual):
    definition = """
    equipment_id             : int unsigned
    ---
    """

@schema
class Camera(dj.Manual):
    definition = """
    -> EquipmentID
    ---
    camera_type             : varchar(256)
    model=''                : varchar(256)
    description=''          : varchar(256)
    """


@schema
class RetireEquipment(dj.Manual):
    definition = """
    -> EquipmentID
    ---
    retire_date            : date
    """

