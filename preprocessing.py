import numpy as np
import pickle as pk
import uproot3 as ur
import pandas as pd

### This script will likely crash if you have too many other memory constraints on your computer.
### the root file, when first opened, has 16 channels which consume a large amount of memory.
### I recommend having nothing else running besides this terminal to avoid crashing.


run_number = 70    
pathin = f"/home/joey/research/data/TUNL/4MeVrootfiles/" # directory for rootfiles to pre-process
pathout = "/home/joey/research/data/TUNL/pkl/raw/"       # directory for reduced .pkl files to be output
                        

infile = f"root_data_SSA_0{run_number}.bin_tree.root"
infile = pathin+infile
outfile = f"SSA{run_number}.pkl"
outfile = pathout+outfile
treestr = f"SSA{run_number}_HPGE"


columns = ['amplitude', # 16 channels
                'channel_time', # 16 channels
                'trigger_time' # 2 channels
                ]
dflist=[]
for col in columns:
    with ur.open(infile) as inFile: # the with statement should acquire and then release
        tree = inFile[treestr]       # the file memory on upon completion.
        testdf = tree.pandas.df(col)#.astype(dtype=tree_dtypes)
        testdf = testdf.dropna(axis=1,how="all")
        dflist.append(testdf)
    print("finished column:", col)

print("concatenating columns and writing to .pkl...")
pd.concat(dflist, axis=1).to_pickle(outfile) # concatenate the indiviudal columns
