import datajoint as dj
from pathlib import Path
from element_interface.utils import find_full_path


# ------------------- Session  -------------------
def get_session_dir(session_key: dict) -> str:
    """"""
    from .pipeline import session
    session_dir = (session.SessionDirectory & session_key).fetch1('session_dir')
    return session_dir


# ------------------- Behavior -------------------
def get_experiment_root_data_dir():
    """Common root directory for all bpod, harp, and aux files"""
    beh_root_dirs = dj.config.get('custom', {}).get('exp_root_data_dir', None)
    return beh_root_dirs if beh_root_dirs else None

# ------------------ DeepLabCut ------------------
def get_dlc_root_data_dir():
    dlc_root_dirs = dj.config.get('custom', {}).get('dlc_root_data_dir')
    if not dlc_root_dirs:
        return None
    elif not isinstance(dlc_root_dirs, list):
        return list(dlc_root_dirs)
    else:
        return dlc_root_dirs


def get_dlc_processed_data_dir() -> str:
    """ Optional. Returns session_dir relative to custom 'dlc_output_dir' root """
    from pathlib import Path
    dlc_output_dir = dj.config.get('custom', {}).get('dlc_output_dir')
    if dlc_output_dir:
        return Path(dlc_output_dir)
    else:
        # If upgrade to element-deeplabcut 0.2, return None here
        return get_dlc_root_data_dir()[0]


# ---------------- Calcium Imaging ---------------
def get_imaging_root_data_dir():
    """"""
    root_data_dirs = dj.config.get('custom', {}).get('imaging_root_data_dir', None)
    return root_data_dirs if root_data_dirs else [r'C:\datajoint']


def get_scan_image_files(scan_key):
    """"""
    # Folder structure: root / subject / session / .tif (raw)
    from .pipeline import session
    data_dir = get_imaging_root_data_dir()
    sess_dir = (session.SessionDirectory & scan_key).fetch1('session_dir')
    scan_dir = find_full_path(data_dir, sess_dir)

    if not scan_dir.exists():
        raise FileNotFoundError(f'Session directory not found ({scan_dir})')

    tiff_filepaths = [fp.as_posix() for fp in scan_dir.glob('*.tif')]
    if tiff_filepaths:
        return tiff_filepaths
    else:
        raise FileNotFoundError(f'No tiff file found in {scan_dir}')


def get_scan_box_files(scan_key):
    """"""
    # Folder structure: root / subject / session / .sbx
    from .pipeline import session
    data_dir = get_imaging_root_data_dir()
    sess_dir = (session.SessionDirectory & scan_key).fetch1('session_dir')
    scan_dir = find_full_path(data_dir, sess_dir)

    if not scan_dir.exists():
        raise FileNotFoundError(f'Session directory not found ({scan_dir})')

    sbx_filepaths = [fp.as_posix() for fp in scan_dir.glob('*.sbx')]
    if sbx_filepaths:
        return sbx_filepaths
    else:
        raise FileNotFoundError(f'No .sbx file found in {scan_dir}')
