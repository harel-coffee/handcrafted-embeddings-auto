import pandas as pd
import numpy as np
from datetime import datetime
import os, pathlib, shutil, random
from sklearn.utils import shuffle
mRS = 42 #int(datetime.now().timestamp())
random.seed(mRS)
np.random.seed(mRS)

mDataTypes = ["java-large"]
mDataCats = ["training", "validation", "test"]

mN = 1000
mTargets = ["equals", "main", "setUp", "onCreate", "toString", "run", "hashCode", "init", "execute", "get", "close", "start", "add", "write", "create", "tearDown", "clear", "read", "reset", "update"]

def saveNRadomSample(mpaths, fname):
    np.random.shuffle(mpaths)
    npaths = random.sample(population=mpaths, k=mN)
    fname = "data/nrandom/" + fname + ".txt"
    pathlib.Path(os.path.dirname(fname)).mkdir(parents=True, exist_ok=True)
    with open(fname, 'w') as f:
        for tpath in npaths:
            f.write("%s\n" % tpath)
    print("Done: ", fname, len(set(npaths)))

def getDataframe():
    dfs = []
    for jt in mDataTypes:
        for jc in mDataCats:
            fpath = "data/filter/" + jt + "-" + jc + ".csv"
            fdf = pd.read_csv(fpath, sep=",", names=["path","method","size"])
            fdf = fdf[~fdf['path'].astype(str).str.contains("space|comma")]
            dfs.append(fdf)
    mdf = pd.concat(dfs, axis=0, ignore_index=True)
    return mdf

for jt in mDataTypes:
    mdf = getDataframe()
    for mtarget in mTargets:
        tdf = mdf.loc[mdf['method'] == mtarget]
        fname = jt + "/" + mtarget
        saveNRadomSample(list(tdf.path), fname)
    ntdf = mdf.loc[~mdf['method'].isin(mTargets)]
    saveNRadomSample(list(ntdf.path), jt + "/nonTarget")

