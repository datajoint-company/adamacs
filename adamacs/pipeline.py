from adamacs.schemas import subject, surgery
from adamacs.schemas.subject import Subject, Project
from adamacs.schemas import session, behavior, equipment
from adamacs.schemas.session import Session
from adamacs.schemas.equipment import Equipment
from adamacs.schemas.surgery import AnatomicalLocation as Location
from element_calcium_imaging import scan, imaging
# from element_deeplabcut import dlc

from . import db_prefix
from .paths import get_session_dir, get_bpod_root_data_dir
from .paths import get_imaging_root_data_dir, get_scan_image_files, get_scan_box_files

__all__ = ['subject', 'surgery', 'session', 'behavior', 'equipment', 'Session',
           'Equipment', 'Location', 'scan', 'imaging', 'Subject', 'Project',
           'get_session_dir', 'get_bpod_root_data_dir', 'get_imaging_root_data_dir',
           'get_scan_image_files', 'get_scan_box_files']

# Activate "imaging" and "scan" schema ----------------------------------_

# requires Location activated above
imaging.activate(db_prefix + 'imaging',
                 db_prefix + 'scan',
                 linking_module=__name__)

# dlc.activate(db_prefix + 'dlc', linking_module=__name__)
