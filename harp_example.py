# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 17:32:15 2022

@author: Daniel
"""

import scipy.io
import numpy as np
import matplotlib.pyplot as plt

path = r'D:\Dropbox\013_INF\INF_Raw_Data\DB_WEZ-8701_2022-03-18_scan9FB2LN5C_sess9FB2LN5C\scan9FB2LN5C_IMU_harp_weardata_2022-03-18T16_55_33.bin'

file = open(path, 'rb')

reg34data=[]
reg35data=[]
reg34time=[]
reg35time=[]
reg35DI0=[]
reg35DI1=[]

def set_bit(value, bit):
    return value | (1<<bit)

def clear_bit(value, bit):
    return value & ~(1<<bit)

def bitget(value, bit_no):
    return (value >> bit_no) & 1

while file:
    messageType = file.read(1)
    if messageType:
        messageType = messageType[0]
    else:
        break
    messageLength = file.read(1)[0]
    if messageLength == 4:
        message = file.read(messageLength - 1)
        checksum = file.read(1)
        # MATLAB code has an if statement here that doesn't seem to do anything???
    elif messageLength >= 10:
        message = file.read(messageLength - 1)
        checksum = file.read(1)
        # MATLAB only does this if the checksum fulfills a certain condition
        dataLength = messageLength - 10
        elements = dataLength / (message[2] & 15)
        elementType = message[2] & 239
        register = message[0]
        if register == 35:
            if (message[2] & 16) == 0:
                reg35time.append(0)
            else:
                seconds = int.from_bytes(message[3:7], "little")  # Not sure if this is the correct byteorder
                milliseconds_to_seconds = int.from_bytes(message[7:9], "little") * 32 * 1e-6
                reg35time.append(seconds + milliseconds_to_seconds)
            if elementType == 2:
                reg35_16bit = int.from_bytes(message[9:11], "little")
                reg35_16bit = clear_bit(reg35_16bit, 15)  # set bits 16 and 15 to 0
                reg35_16bit = clear_bit(reg35_16bit, 14)
                reg35data.append(reg35_16bit)
                reg35DI1.append(bitget(reg35_16bit, 15))
                reg35DI0.append(bitget(reg35_16bit, 14))
        elif register == 34:
            if (message[2] & 16) == 0:
                reg34time.append(0)
            else:
                seconds = int.from_bytes(message[3:7], "little")  # Not sure if this is the correct byteorder
                milliseconds_to_seconds = int.from_bytes(message[7:9], "little") * 32 * 1e-6
                reg34time.append(seconds + milliseconds_to_seconds)
            if elementType == 130:
                reg34data.append(int.from_bytes(message[9:11], "little"))
                reg34data.append(int.from_bytes(message[11:13], "little"))
                reg34data.append(int.from_bytes(message[13:15], "little"))
                reg34data.append(int.from_bytes(message[15:17], "little"))
                reg34data.append(int.from_bytes(message[17:19], "little"))
                reg34data.append(int.from_bytes(message[19:21], "little"))
                reg34data.append(int.from_bytes(message[21:23], "little"))
                reg34data.append(int.from_bytes(message[23:25], "little"))
                reg34data.append(int.from_bytes(message[25:27], "little"))
                reg34data.append(int.from_bytes(message[27:29], "little"))
                
                
                
                
                
                
                