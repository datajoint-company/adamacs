# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 17:32:15 2022

@author: Daniel
"""

import scipy.io
import numpy as np

path = r"E:\Dropbox\Dropbox\013_INF\INF_Raw_Data\T - DB_WEZ-8705_2022-02-15_exp9FAK32BA\exp9FAK32BA_WEZ-8705_StimArenaMaster_20220215_141631.mat"

data = scipy.io.loadmat(path, squeeze_me=False)

SessionData = data["SessionData"]

# np.squeeze does not work on these singleton dimensions, returns empty array
TrialData = SessionData["RawEvents"][0][0]["Trial"]
# TrialDataStates = TrialData[0][0][0][0]['States']
# TimeToPort = TrialDataStates[0][0]['WaitForResponse']
# CueDelay = TrialDataStates[0][0]['CueDelay']
# Reward = SessionData[0][0]['TrialSettings']['GUI'][0][0]['RewardDelay']
# Drinking = TrialDataStates[0][0]['Drinking']

# TODO: port ParseBpodPortEvents


SessionData["RawEvents"][0][0]["Trial"][0][0][0][0]["States"][0][0][0][0]["CueDelay"]
