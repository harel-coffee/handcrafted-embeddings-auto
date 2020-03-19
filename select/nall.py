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

mTargets = ["equals", "main", "setUp", "onCreate", "toString", "run", "hashCode", "init", "execute", "get", "close", "start", "add", "write", "create", "tearDown", "clear", "read", "reset", "update"]

def saveAllSample(mpaths, fname):
    fname = "../data/nall/" + fname + ".txt"
    pathlib.Path(os.path.dirname(fname)).mkdir(parents=True, exist_ok=True)
    with open(fname, 'w') as f:
        for tpath in mpaths:
            f.write("%s\n" % tpath)
    print("Done: ", fname, len(set(mpaths)))

def getDataframe(tpath):
    tdf = pd.read_csv(tpath, sep=",", names=["path","method","size"])
    #tdf = tdf[~tdf['path'].astype(str).str.contains("space|comma")]
    return tdf

for jt in mDataTypes:
    for jc in mDataCats:
        tpath = "../data/filter/" + jt + "-" + jc + ".csv"
        print("Start: ", tpath)
        tdf = getDataframe(tpath)
        for mtarget in mTargets:
            mdf = tdf.loc[tdf['method'] == mtarget]
            fname = jt + "/" + jc + "/" + mtarget
            saveAllSample(list(mdf.path), fname)
        print("Done: ", tpath)
