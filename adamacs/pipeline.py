from . import db_prefix

from adamacs.schemas import subject, surgery
from adamacs.schemas.subject import Subject, Project, Lab
from adamacs.schemas import session, behavior, equipment
from adamacs.schemas.session import Session
from adamacs.schemas.equipment import Equipment
from adamacs.schemas.surgery import AnatomicalLocation as Location
from element_calcium_imaging import scan, imaging
from element_deeplabcut import train, model
# from element_deeplabcut import dlc

from .paths import get_session_dir, get_bpod_root_data_dir, get_dlc_root_data_dir
from .paths import get_imaging_root_data_dir, get_scan_image_files, get_scan_box_files

__all__ = ['subject', 'surgery', 'session', 'behavior', 'equipment', 'scan', 'imaging',
           'train', 'model',
           'Session', 'Equipment', 'Location', 'Subject', 'Project', 'Lab',
           'get_session_dir', 'get_bpod_root_data_dir', 'get_dlc_root_data_dir',
           'get_imaging_root_data_dir', 'get_scan_image_files', 'get_scan_box_files']

# Activate adamacs-defined schema ---------------------------------------
# dj.schema.activate(db_prefix + 'subject', create_schema=True,
#                 create_tables=True, add_objects=__name__)

# Activate "imaging" and "scan" schema ----------------------------------

# requires Location activated above
imaging.activate(db_prefix + 'imaging',
                 db_prefix + 'scan',
                 linking_module=__name__)

# Activate "train" and "model" schema -----------------------------------

Device = Equipment  # Inherited in model.VideoRecording

# Note that train is optional. For model training within DataJoint
train.activate(db_prefix + 'train', linking_module=__name__)
model.activate(db_prefix + 'model', linking_module=__name__)
