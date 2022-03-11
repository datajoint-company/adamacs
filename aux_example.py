# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 12:05:43 2022

@author: Daniel
"""

import numpy as np
import h5py
import matplotlib.pyplot as plt

path = r'E:\Dropbox\Dropbox\013_INF\INF_Raw_Data\T - DB_WEZ-8705_2022-02-15_exp9FAK32BA\exp9FAK32BA_TR_ROS-0005_0043.h5'

hf = h5py.File(path, 'r')

def demultiplex(auxdata, channels=5):
    """Demultiplex the digital data"""
    auxdata = auxdata.flatten()
    binary = [[int(x) for x in f'{x:0{channels}b}'] for x in auxdata]
    return np.array(binary, dtype=bool).T

sr = hf['header']['AcquisitionSampleRate'][0][0]
timebase = np.arange(hf['sweep_0043']['analogScans'].shape[1]) / sr

# DIGITAL SIGNALS
digital_channels = demultiplex(hf['sweep_0043']['digitalScans'][0], 5)
main_track_gate_chan = digital_channels[4]
shutter_chan = digital_channels[3]
mini2p_frame_chan = digital_channels[2]
mini2p_line_chan = digital_channels[1]
mini2p_vol_chan = digital_channels[0]

# ANALOG SIGNALS
cam_trigger = hf['sweep_0043']['analogScans'][0]
bpod_trial_vis_chan = hf['sweep_0043']['analogScans'][1]
bpod_reward1_chan = hf['sweep_0043']['analogScans'][2]
bpod_tone_chan = hf['sweep_0043']['analogScans'][3]

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
def get_timestamps(auxdata, thr=1, inverse=False):
    if auxdata.dtype == 'bool':
        auxdata = auxdata > thr
        
    digithr = 0.5
    diff = np.diff(auxdata)
    idc = np.argwhere(diff != 0)

