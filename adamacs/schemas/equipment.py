"""Tables related to equipment.

We use a variety of different equipment 
"""
import datajoint as dj
from .. import db_prefix
schema = dj.schema(db_prefix + 'equipment')

__all__ = ['db_prefix']

# -------------- Table declarations --------------


@schema
class Equipment(dj.Manual):
    definition = """
    scanner: varchar(32)
    """

# CB DEV NOTE: I suggest adding Device here as a foreign key for DLC camera and then
#              changing the reference in adamacs.pipeline. Currently, dlc relies on
#              the above 'scanner' table for camera information, see model_videos.csv
