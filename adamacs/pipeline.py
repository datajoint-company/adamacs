import datajoint as dj
from adamacs.schemas import subject, surgery, session, behavior, equipment
from adamacs.schemas.session import Session
from adamacs.schemas.equipment import Equipment
from element_calcium_imaging import scan, imaging

from .paths import get_session_dir, get_bpod_root_data_dir
from .paths import get_imaging_root_data_dir, get_scan_image_files, get_scan_box_files

__all__ = ['subject', 'surgery', 'session', 'behavior', 'equipment', 'Session',
           'Equipment', 'scan', 'imaging',
           'get_session_dir', 'get_bpod_root_data_dir', 'get_imaging_root_data_dir',
           'get_scan_image_files', 'get_scan_box_files']

if 'custom' not in dj.config:
    dj.config['custom'] = {}

db_prefix = dj.config['custom'].get('database.prefix', '')


# Activate "subject", "session" schema ----------------------------------

subject.activate(db_prefix + 'subject', linking_module=__name__)

surgery.activate(db_prefix + 'surgery', linking_module=__name__)

session.activate(db_prefix + 'session', linking_module=__name__)

surgery.activate(db_prefix + 'surgery', linking_module=__name__)

behavior.activate(db_prefix + 'behavior', linking_module=__name__)

equipment.activate(db_prefix + 'equipment')

# Activate "imaging" and "scan" schema ----------------------------------_


@session.schema
class Location(dj.Manual):
    definition = """
    scan_location_id    : varchar(16)
    ---
    anatomical_location : varchar(256)
    """


imaging.activate(db_prefix + 'imaging',
                 db_prefix + 'scan',
                 linking_module=__name__)
