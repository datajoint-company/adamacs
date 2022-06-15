# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 17:32:15 2022

@author: Daniel
"""

import scipy.io
import numpy as np

path = r'D:\Dropbox\013_INF\INF_Raw_Data\DB_WEZ-8701_2022-03-18_scan9FB2LN5C_sess9FB2LN5C\scan9FB2LN5C_IMU_harp_weardata_2022-03-18T16_55_33.bin'

file = open(path, 'rb')

reg34data=[]
reg35data=[]
reg34time=[]
reg35time=[]
reg35DI0=[]
reg35DI1=[]

while file:
    messageType = file.read(1)[0]
    messageLength = file.read(1)[0]
    if messageLength == 4:
        message = file.read(messageLength - 1)
        checksum = file.read(1)
        # MATLAB code has an if statement here that doesn't seem to do anything???
    elif:
        messageLength >= 10:
        message = file.read(messageLength - 1)
        checksum = file.read(1)
        