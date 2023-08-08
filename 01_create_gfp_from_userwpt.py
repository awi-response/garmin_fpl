import os 
import sys
import glob

folder = sys.argv[1]

for file in glob.glob(f"{folder}\*_user.wpt"):
    target = file[:-9]
    print(target)
    os.system(f'python 20230704_WPnameChanger.py {target}_user.wpt')
    os.system(f'python 20230704_DEC2DMM.py {target}_user_renamed.wpt')
    os.system(f'python 20230704_wpt_to_gfp.py {target}_user_renamed_DMM.wpt {target}_fpl.gfp')
