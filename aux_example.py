# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 12:05:43 2022

@author: Daniel
"""

import numpy as np
import h5py
import matplotlib.pyplot as plt
from pywavesurfer import ws
import pdb

path = r'E:\Dropbox\Dropbox\013_INF\INF_Raw_Data\DB_WEZ-8701_2022-03-18_scan9FB2LN5C_sess9FB2LN5C\scan9FB2LN5C_DB_WEZ-8701_2027.h5'

hf = ws.loadDataFile(filename=path, format_string='double' )

def demultiplex(auxdata, channels=5):
    """Demultiplex the digital data"""
    auxdata = auxdata.flatten()
    binary = [[int(x) for x in f'{x:0{channels}b}'] for x in auxdata]
    return np.array(binary, dtype=bool).T

sweep = [x for x in hf.keys() if 'sweep' in x][0]

sr = hf['header']['AcquisitionSampleRate'][0][0]
timebase = np.arange(hf[sweep]['analogScans'].shape[1]) / sr

# DIGITAL SIGNALS
digital_channels = demultiplex(hf[sweep]['digitalScans'][0], 5)
main_track_gate_chan = digital_channels[4]
shutter_chan = digital_channels[3]
mini2p_frame_chan = digital_channels[2]
mini2p_line_chan = digital_channels[1]
mini2p_vol_chan = digital_channels[0]

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

"""Calculate timestamps"""
def get_timestamps(data, sr, thr=1, inverse=False):
    if data.dtype == 'bool':
        data = data > 0.5
    else:
        data = data > thr
    if inverse: data = not data
    
    diff = np.diff(data)
    idc = np.argwhere(diff != 0)[:, 0]
    timestamps = idc / sr

    return timestamps

ts_main_track_gate_chan = get_timestamps(main_track_gate_chan, sr)
ts_shutter_chan = get_timestamps(shutter_chan, sr)
ts_mini2p_frame_chan = get_timestamps(mini2p_frame_chan, sr)
ts_mini2p_line_chan = get_timestamps(mini2p_line_chan, sr)
ts_mini2p_vol_chan = get_timestamps(mini2p_vol_chan, sr)

ts_bpod_tone_chan = get_timestamps(bpod_tone_chan, sr)

