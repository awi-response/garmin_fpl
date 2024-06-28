import os 
import sys
import glob
from pathlib import Path

folder = sys.argv[1]

'''
folder: folder which contains all iii_siteName_user.wpt files of single targets of one day 
output: 
20230704_WPnameChanger.py: changes the names output depending on:
    - route type (grid or transect)
    - choosen filename
    to iiillo (i: ID code,l: linenumber such as 01,o:order such as A/B) for grids (e.g. 00401A: Target 004, line 01, point A)
    WPTnames(i: ID code,l: linenumber such as 01,o:order such as A/B): 
    - for grid: iiillA / iiillB (e.g. 00112A,00112B for line 12 of target with ID 001 and direction A to B)
    - for transect: iii##, iii##+1 ( e.g 00112,00113 for waypoint 12 and 13 of target with ID 001 )
    input: iii_sitename_user.wpt file (or exported from MACS Mission planner or manually defined.
                                        if manually defined follow strictly the guidlines of naming convention described in the ReadMe)
    output:
    iii_sitename_user_renamed.wpt file:
    file has identical columns as the iii_sitename_user.wpt file but changed waypoint and waypoint comment names
    
20230704_DEC2DMM.py: Converts Decimal degree coordinates to Degree Decimal Minutes coordinates
    - input: the output file of 20230704_WPnameChange.py:  iii_sitename_user_renamed.wpt
    - output: iii_sitename_user_renamed_DMM.wpt: coordinates are changed to DDM format

20230704_wpt_to_gfp.py: Converts the information to a flightplan which is readable by Garmin
    - input: iii_sitename_user_renamed_DMM.wpt
    - output: returns a iii_sitename_flp.gfp file which can be imported to the Garmin
'''

renamed_user_wpt = []
for file in glob.glob(f"{folder}\*_user.wpt"):
    target = file[:-9]
    target_name = Path(file).name[:-9]
    print(target)
    print(target_name)
    fpl_dir = Path(folder) / 'FPL'
    os.makedirs(fpl_dir, exist_ok=True)
    # Script 1: rename waypoints
    os.system(f'python 20230704_WPnameChanger.py {target}_user.wpt')
    # Script 2: change coordinate format
    os.system(f'python 20230704_DEC2DMM.py {target}_user_renamed.wpt')
    # Script 3: create flightplans
    outfile = fpl_dir / f'{target_name}_fpl.gfp'
    os.system(f'python 20230704_wpt_to_gfp.py {target}_user_renamed_DDM.wpt {outfile}')
