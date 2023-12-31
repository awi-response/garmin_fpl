import pandas as pd
import numpy as np
import os
import glob
import sys

def wpNameChanger(fname):
    # fname requirement:
    #       iii_sitecode_user.wpt with iii being a 3 digit ID code. 
    #       the waypointName will be composed of iiillo (i: ID code,l: linenumber such as 01,o:order such as A/B) 
    ID = str(os.path.basename(fname)).split('_')[0]
    # check if ID has only 2 digits
    if len(ID)<3:
        ID = '0'+ ID #make sure id is only 3 digits long and upper case
        ID = ID.upper()
    if len(ID)>3:
        ID = ID[0:3]#make sure id is only 3 digits long and upper case
        ID = ID.upper()
    f = pd.read_csv(fname,header=None) #import file

    #create names
    numbers = [wpName[2:4] for wpName in f.iloc[:,0]] # the default export of MAC mission planner is FL_01_A
    order = [wpName[5] for wpName in f.iloc[:,0]] # the last digit of the default export
    WPrenamed = [str(ID)+n+o for n,o in zip(numbers, order)] # combine the info

    f[0] = WPrenamed # overwrite names

    siteCode = os.path.basename(fname).split('_')# get the remaining site code of filename
    siteCode = [s.upper() for s in siteCode] # Garmin required only capitals
    siteCode = ''.join(siteCode[0:-1]) # get all info in filename apart from user.wpt
    comment = [siteCode+n+o for n,o in zip(numbers,order)] #combine comment line
    f[1] = comment # overwrite comment name in original file

    if len(siteCode[0])>25: # garmin only allows for 25 digits in the comment column
        print('Caution: Comment has more than 25 characters - no file exported')
    else:
        f.to_csv(fname[:-4]+'_renamed.wpt',header=False,index = False) # export file

if __name__ == '__main__':
    fname = sys.argv[1]
    print(f'name_changer input {fname}')
    wpNameChanger(fname)