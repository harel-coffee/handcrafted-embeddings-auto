import pandas as pd
import os, pathlib, shutil, glob

mDataTypes = ["java-large"]
mN = 1000

def saveOnCopy(mpaths, mtarget):
    for p1 in mpaths:
        p2 = p1.replace("/transforms/Methods/", "/handcrafted/t"+str(mN)+"/"+mtarget+"/")
        pathlib.Path(os.path.dirname(p2)).mkdir(parents=True, exist_ok=True)
        shutil.copy2(p1,p2)

for jt in mDataTypes:
    fname = "../data/nrandom/" + jt + "/*.txt"
    mTargetFiles = glob.glob(fname)
    for fname in mTargetFiles:
        mtarget = (fname.split("/")[-1]).replace(".txt","")
        mdf = pd.read_csv(fname, sep=",", names=["path"])
        saveOnCopy(list(mdf.path), mtarget)
        print("Done:", mtarget)

