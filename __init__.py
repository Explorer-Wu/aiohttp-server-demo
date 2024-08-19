#!/usr/bin/python3 
#coding=utf-8
import sys
# print(sys.modules)
import os

__version__ = '0.0.1'

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

if sys.version >= '3':
    with open(outputFile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for item in sortsim:
            writer.writerow([item[0], item[1], item[2]])
else:
    with open(outputFile, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for item in sortsim:
            writer.writerow([item[0], item[1], item[2]])
