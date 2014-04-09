#!/usr/bin/env python
import csv
import os
import serial
import sys
import time

usbname = '/dev/ttyACM0'
failed = False
filename = 'file.csv'
starttime = None
itemsForFile = []

try:
    fileObject = open(filename, 'w+')
    csvWriter = csv.writer(fileObject)
except:
    print("failed to open file for writing: ", filename)
    sys.exit()

try:
    arduino = serial.Serial(usbname, 9600)
    for i in range(10):
        garbage = arduino.readline()
except:
    print("failed to open serial connection to arduino (permissions?): ", usbname)
    sys.exit()

try:
    print("Capturing Takktile Data ctrl^C to stop")
    while not failed:
        data = arduino.readline()
        if data:
            try:
                if starttime is None:
                    starttime = time.time()
                currentTime = ['%.3f' %(time.time() - starttime)]
                values =  currentTime + [j for j in data.translate(None, ' []\r\n').split(",")]
                itemsForFile.append(values)
            except ValueError:
                print ("invalid data line ignored:", data)
except KeyboardInterrupt:
    print("Writing File...")

tactileDataType = 'takknumber' 
header = ['Time [s]']
for i, item in enumerate(itemsForFile[0][1:]):
    header.append('Elem%d [%s]' % (i, tactileDataType))
csvWriter.writerow(header)
for item in itemsForFile:
    csvWriter.writerow(item)
