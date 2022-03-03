# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 17:32:15 2022

@author: Daniel
"""

import scipy.io

path = r'E:\Dropbox\Dropbox\013_INF\INF_Raw_Data\T - DB_WEZ-8705_2022-02-15_exp9FAK32BA\exp9FAK32BA_WEZ-8705_StimArenaMaster_20220215_141631.mat'

data = scipy.io.loadmat(path, squeeze_me=False)

TrialData = data['SessionData']['RawEvents'][0][0]['Trial']
