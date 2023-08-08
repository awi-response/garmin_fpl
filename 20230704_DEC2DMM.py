import pandas as pd
import numpy as np
import os
import glob

import sys

def decimal_degrees_to_dmm(decimal_degrees):
    # function to calculate decimal degrees to decimal mintes
    degrees = int(decimal_degrees) # get degrees
    decimal_minutes = (decimal_degrees - degrees) * 60 # convert minutes to decimal minutes
    decimal_minutes = np.round(decimal_minutes, decimals=1) # round to format necessary for gfp format (1 decimal)
    return degrees, decimal_minutes # get degree integer and decimal minutes

def convert2stringLon(val):
    # function to convert Longitude to string with E/W indicator and d/m as deg and minute sign
    deg = val[0]
    min = val[1]
    if deg<0:
        EastWest = 'W'
        min = abs(min) # remove minus sign
        deg = abs(deg) # remove minus sign
    else:
        EastWest = 'E'
    return('{:1}{:02d}d{:04.1f}m'.format(EastWest,deg,min))

def convert2stringLat(val):
    #function to convert Latitude to string with S/N indicator and d/m as deg and minute sign
    deg = val[0]
    min = val[1]
    if deg<0:
        NorthSouth = 'S'
        min = abs(min) # remove minus sign
        deg = abs(deg) # remove minus sign
    else:
        NorthSouth = 'N'
    return('{:1}{:02d}d{:04.1f}m'.format(NorthSouth,deg,min))

def dec2dmm(fname):
    # function to read in wpt file as exported by MACS, converts DECDeg to DMM, and save it back
    # output remains same in overall format, only DECDeg will be in DMM
    f = pd.read_csv(fname, header=None)

    lat = list(map(decimal_degrees_to_dmm, f.iloc[:,2]))
    lon = list(map(decimal_degrees_to_dmm, f.iloc[:,3]))

    lon = list(map(convert2stringLon,lon))
    lat = list(map(convert2stringLat,lat))
    f[2] = lat
    f[3] = lon

    f.to_csv(fname[:-4]+'_DMM.wpt',header=False,index = False) # saves file with extension DMM

if __name__ == '__main__':
    fname = sys.argv[1]
    dec2dmm(fname)