import datajoint as dj
from pathlib import Path


# ------------------- Session  -------------------
def get_session_dir(session_key: dict) -> str:
    """"""
    from .pipeline import session
    session_dir = (session.SessionDirectory & session_key).fetch1('session_dir')
    return session_dir


# ------------------- Behavior -------------------
def get_bpod_root_data_dir():
    """Common root directory for all bpod files"""
    beh_root_dirs = dj.config.get('custom', {}).get('beh_root_data_dir', None)
    return beh_root_dirs if beh_root_dirs else None


# ---------------- Calcium Imaging ---------------
def get_imaging_root_data_dir():
    """"""
    root_data_dirs = dj.config.get('custom', {}).get('imaging_root_data_dir', None)
    return root_data_dirs if root_data_dirs else None


def get_scan_image_files(scan_key):
    """"""
    # Folder structure: root / subject / session / .tif (raw)
    data_dir = get_imaging_root_data_dir()
    sess_dir = Path(data_dir + "/" + get_session_dir())

    if not sess_dir.exists():
        raise FileNotFoundError(f'Session directory not found ({sess_dir})')

    tiff_filepaths = [fp.as_posix() for fp in sess_dir.glob('*.tif')]
    if tiff_filepaths:
        return tiff_filepaths
    else:
        raise FileNotFoundError(f'No tiff file found in {sess_dir}')


def get_scan_box_files(scan_key):
    """"""
    # Folder structure: root / subject / session / .sbx
    data_dir = get_imaging_root_data_dir()
    sess_dir = Path(data_dir + "/" + get_session_dir())

    if not sess_dir.exists():
        raise FileNotFoundError(f'Session directory not found ({sess_dir})')

    sbx_filepaths = [fp.as_posix() for fp in sess_dir.glob('*.sbx')]
    if sbx_filepaths:
        return sbx_filepaths
    else:
        raise FileNotFoundError(f'No .sbx file found in {sess_dir}')
