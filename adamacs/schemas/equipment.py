"""Tables related to equipment.

We use a variety of different equipment 
"""

import datajoint as dj

schema = dj.schema()
_linking_module = None

# ------------------ Activation ------------------


def activate(schema_name, *, create_schema=True, create_tables=True):
    """
    activate(schema_name, create_schema=True, create_tables=True, linking_module=None)
        :param schema_name: schema name on the database server
        :param create_schema: when True, create schema if it does not yet exist
        :param create_tables: when True, create tables if they do not yet exist
    """

    schema.activate(schema_name, create_schema=create_schema,
                    create_tables=create_tables)

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
