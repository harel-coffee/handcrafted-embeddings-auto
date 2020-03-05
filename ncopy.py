import pandas as pd
import os, pathlib, shutil

mDataTypes = ["java-large"]
mDataCats = ["training"]

mTargets = ["nonTarget", "equals", "setUp", "toString"]
mN = 1000

def saveOnCopy(pathList, mtarget):
    for p1 in pathList:
        if not os.path.exists(p1):
            p1 = p1.replace("_space_", " ")
            p1 = p1.replace("_comma_", ",")
        p2 = p1.replace("/transforms/Methods/", "/handcrafted/t"+str(mN)+"/"+mtarget+"/")
        pathlib.Path(os.path.dirname(p2)).mkdir(parents=True, exist_ok=True)
        shutil.copy2(p1,p2)

for jt in mDataTypes:
    for jc in mDataCats:
        for mtarget in mTargets:
            fname = jt + "/" + jc + "/" + mtarget
            print (fname)
            mpath = "data/nrandom/" + fname + ".txt"
            mdf = pd.read_csv(mpath, sep=",", names=["path"])
            saveOnCopy(list(mdf.path), mtarget)
