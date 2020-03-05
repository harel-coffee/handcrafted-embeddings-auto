import pandas as pd
import numpy as np
from datetime import datetime
import os, pathlib, shutil
from sklearn.utils import shuffle
mRS = int(datetime.now().timestamp()) #42
np.random.seed(mRS)

mDataTypes = ["java-large"]
mDataCats = ["training"]

mTargets = ["equals", "setUp", "toString"]
mN = 1000

def saveRadomSample(tdf, fname):
    print(fname)
    sdf = shuffle(tdf, n_samples=mN, random_state=mRS)
    sdf = sdf.drop(['method', 'size'], axis=1)
    fname = "data/nrandom/" + fname + ".txt"
    pathlib.Path(os.path.dirname(fname)).mkdir(parents=True, exist_ok=True)
    sdf.to_csv(fname, header=None, index=None)

for jt in mDataTypes:
    for jc in mDataCats:
        mpath = "data/filter/" + jt + "-" + jc + ".csv"
        mdf = pd.read_csv(mpath, sep=",", names=["path","method","size"])
        for mtarget in mTargets:
            tdf = mdf.loc[mdf['method'] == mtarget]
            fname = jt + "/" + jc + "/" + mtarget
            saveRadomSample(tdf, fname)
        ntdf = mdf.loc[~mdf['method'].isin(mTargets)]
        saveRadomSample(ntdf, jt + "/" + jc + "/nonTarget")

