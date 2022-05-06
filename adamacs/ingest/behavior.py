"""Ingest behavioral events from aux and bpod files.
The aux file is the only .h5 file in a scan directory.
The bpod file contains StimArenaMaster and is a .mat file."""

import numpy as np
import h5py
import matplotlib.pyplot as plt
from pywavesurfer import ws
from ..paths import get_imaging_root_data_dir
from element_interface.utils import find_full_path
import warnings
import pathlib
import re
import pdb

path = r'E:\Dropbox\Dropbox\013_INF\INF_Raw_Data\DB_WEZ-8701_2022-03-18_scan9FB2LN5C_sess9FB2LN5C\scan9FB2LN5C_DB_WEZ-8701_2027.h5'
def demultiplex(auxdata, channels=5):
    """Demultiplex the digital data"""
    auxdata = auxdata.flatten()
    binary = [[int(x) for x in f'{x:0{channels}b}'] for x in auxdata]
    return np.array(binary, dtype=bool).T

def get_timestamps(data, sr, thr=1, inverse=False ):
    if data.dtype == 'bool':
        data = data > 0.5
    else:
        data = data > thr
    if inverse: data = not data
    
    diff = np.diff(data)
    idc = np.argwhere(diff != 0)
    timestamps = idc / sr
    return timestamps

def ingest_aux(session_key, root_paths=get_imaging_root_data_dir(),
                        verbose=False):
    
    if not verbose:
        warnings.filterwarnings('ignore')

    paths = [pathlib.Path(path) for path in root_paths]
    valid_paths = [p for p in paths if p.is_dir()]
    match_paths = []
    for p in valid_paths:
        match_paths.extend(list(p.rglob(f'*{session_key}*')))
    
    n_scans = len(match_paths)
    if verbose:
        print(f'Number of scans found: {n_scans}')

    scan_pattern = "scan.{8}"
    basenames = [x.name for x in match_paths]
    scan_keys = [re.findall(scan_pattern, x) for x in basenames]
    scan_basenames = [x for x in basenames if bool(re.search(scan_pattern, x))]
    aux_files = []
    for k in scan_basenames:
        curr_path = find_full_path(root_paths, k)
        curr_file = ws.loadDataFile(filename=curr_path, format_string='double' )
        aux_files.append(curr_file)

    for curr_aux in aux_files:
        sweep = [x for x in curr_aux.keys() if 'sweep' in x][0]

        sr = curr_aux['header']['AcquisitionSampleRate'][0][0]
        timebase = np.arange(curr_aux[sweep]['analogScans'].shape[1]) / sr

        # DIGITAL SIGNALS
        digital_channels = demultiplex(curr_aux[sweep]['digitalScans'][0], 5)
        main_track_gate_chan = digital_channels[4]
        shutter_chan = digital_channels[3]
        mini2p_frame_chan = digital_channels[2]
        mini2p_line_chan = digital_channels[1]
        mini2p_vol_chan = digital_channels[0]
        
        """Calculate timestamps"""
        ts_main_track_gate_chan = get_timestamps(main_track_gate_chan, sr)
        ts_shutter_chan = get_timestamps(shutter_chan, sr)
        ts_mini2p_frame_chan = get_timestamps(mini2p_frame_chan, sr)
        ts_mini2p_line_chan = get_timestamps(mini2p_line_chan, sr)
        ts_mini2p_vol_chan = get_timestamps(mini2p_vol_chan, sr)
        
        """Analog signals"""
        cam_trigger = curr_aux[sweep]['analogScans'][0]
        bpod_trial_vis_chan = curr_aux[sweep]['analogScans'][1]
        bpod_reward1_chan = curr_aux[sweep]['analogScans'][2]
        bpod_tone_chan = curr_aux[sweep]['analogScans'][3]
        
        ts_cam_trigger = get_timestamps(cam_trigger)
        ts_bpod_visual = get_timestamps(bpod_trial_vis_chan)
        ts_bpod_reward = get_timestamps(bpod_reward1_chan)
        ts_bpod_tone = get_timestamps(bpod_tone_chan)
        


    pdb.set_trace()

    """
    # ANALOG SIGNALS
    cam_trigger = hf[sweep]['analogScans'][0]
    bpod_trial_vis_chan = hf[sweep]['analogScans'][1]
    bpod_reward1_chan = hf[sweep]['analogScans'][2]
    bpod_tone_chan = hf[sweep]['analogScans'][3]

    fig, ax = plt.subplots(9)
    ax[0].plot(timebase, main_track_gate_chan)
    ax[1].plot(timebase, shutter_chan)
    ax[2].plot(timebase, mini2p_frame_chan)
    ax[3].plot(timebase, mini2p_line_chan)
    ax[4].plot(timebase, mini2p_vol_chan)
    ax[5].plot(timebase, cam_trigger)
    ax[6].plot(timebase, bpod_trial_vis_chan)
    ax[7].plot(timebase,bpod_tone_chan)
    ax[8].plot(timebase, bpod_reward1_chan)

    for a in ax[:-1]:
        a.set_xticks([])

    ax[0].set_ylabel('Track Gate /\nMaster trigger')
    ax[1].set_ylabel('Laser Shutter')
    ax[2].set_ylabel("mini2p frames")
    ax[3].set_ylabel("mini2p lines")
    ax[4].set_ylabel("mini2p volumes")
    ax[5].set_ylabel("Track cam\nframes")
    ax[6].set_ylabel("BPOD Trial start")
    ax[7].set_ylabel("BPOD Tone")
    ax[8].set_ylabel("BPOD reward /\npunish")
    ax[8].set_xlabel("time (s)")
    """