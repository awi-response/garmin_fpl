import pandas as pd
import numpy as np
import glob
import os
import sys

def combineWPT(directory):
    
    wpts = glob.glob(os.path.join(directory,'*_renamed.wpt'))

    def get_df():
        # list of files
        df=pd.DataFrame()
        for file in wpts:
                f=pd.read_csv(file, header=None)
                df=df.append(f)
        return df

    df = get_df()
    df.to_csv(os.path.join(directory,'user.wpt'), header=False,index = False)

if __name__ == '__main__':
    folder = sys.argv[1]
    combineWPT(folder)