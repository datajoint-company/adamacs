from cgitb import scanvars
import pathlib
import csv
from datetime import datetime
import re
from element_session import session_with_id
from itertools import groupby
from datajoint.errors import DuplicateError
import warnings
from element_calcium_imaging import scan


def ingest_session_scan(session_key, session_path=r'C:\datajoint', verbose=False):
    """Locate all directories in session_path that are part
    of the sesssion. Extract the following attributes from
    the directory names:
    Subject
    session_datetime
    User
    """

    p = pathlib.Path(session_path)

    session_pattern = session_key  # Session key can be exactly matched
    scan_pattern = "scan.{8}"

    dirs = [x for x in p.iterdir() if x.is_dir() and session_key in x.name]
    
    n_scans = len(dirs)
    if verbose: print(f"Number of scans found: {n_scans}")

    basenames = [x.name for x in dirs]
    
    scan_keys = [re.findall(scan_pattern, x) for x in basenames]
    scan_basenames = [x for x in basenames if bool(re.search(scan_pattern, x))]
    
    for idx, k in enumerate(scan_keys):
        print(scan_keys)
        print(basenames)
        if len(k) != 1:
            raise ValueError(f"Directory name contains {len(k)} scan keys. Must be 1.")
        scan_keys[idx] = k[0]

    # Find the animal ID by position
    subjects = [x.split('_')[1] for x in basenames]

    # Return true if all elements in iterable are equal
    def all_equal(iterable):
        g = groupby(iterable)
        return next(g, True) and not next(g, False)

    if not all_equal(subjects):
        raise ValueError(f"Scans from multiple animals found for session. Must be 1 animal.")
    subject = subjects[0]

    # Find the animal ID by position
    user_keys = [x.split('_')[0] for x in basenames]
    if not all_equal(user_keys):
        raise ValueError(f"Scans from multiple users found for session. Must be 1 user.")
    user = user_keys[0]

    dates = [x.split('_')[2] for x in basenames]
    if not all_equal(dates):
        raise ValueError(f"Found different dates for session. Must be on same date.")
    date = dates[0]
    
    try:
        session_with_id.Session.insert1((session_key, subject, date))
    except DuplicateError:
        warnings.warn(f'Session row {session_key, subject, date} already inserted. Skipped!')
    
    try:
        session_with_id.SessionDirectory.insert1((session_key, session_path, user))
    except DuplicateError:
        warnings.warn(f'SessionDirectory {session_key, session_path, user} already inserted. Skipped!')
        
    try:
        session_with_id.SessionUser.insert1((session_key, user))
    except DuplicateError:
       warnings.warn(f'SessionUser {session_key, user} already inserted. Skipped!')

    # Insert each scan
    for idx, s in enumerate(scan_keys):
        equipment_placeholder = "Equipment"  # Resolve how to extract equipment
        software_placeholder = "ScanImage"
        location_placeholder = "Location"
        path = p / scan_basenames[idx]
        try:
            scan.Scan.insert1((session_key, s, equipment_placeholder, software_placeholder, ''))
        except DuplicateError:
            warnings.warn(f'Scan {s} already inserted. Skipped')
        
        try:
            scan.ScanLocation.insert1((session_key, s, location_placeholder))
        except DuplicateError:
            warnings.warn(f"ScanLocation for {s} already inserted. Skipped")
            
        try:
            scan.ScanPath.insert1((session_key, s, user, path))
        except DuplicateError:
            warnings.warn(f"ScanPath for {s} already inserted. Skipped.")
