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
    while not failed:
        data = arduino.readline()
        if data:
            try:
                if starttime is None:
                    starttime = time.time()
                currentTime = ['%.3f' %(time.time() - starttime)]
                values =  currentTime + [float(j) for j in data.translate(None, ' []').split(",") if len(j) > 2]
                print values
                itemsForFile.append(values)
            except ValueError:
                print ("invalid data ignored:", data)
except KeyboardInterrupt:
    print("Writing File...")

csvWriter.writerow(['Time [s]','Data Marker'])
csvWriter.writerow(['0.000','Start'])
csvWriter.writerow([itemsForFile[-1][0],'Finish'])
csvWriter.writerow([])

tactileDataType = 'takkPSI' 
temp = ['Time [s]']
print itemsForFile[0]
for i, item in enumerate(itemsForFile[0]):
    temp.append('Elem%d [%s]' % (i, tactileDataType))
for item in itemsForFile:
    csvWriter.writerow(item)
