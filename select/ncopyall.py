import pandas as pd
import os, pathlib, shutil, glob

mDataTypes = ["java-large"]
mDataCats = ["training", "validation", "test"]

def handleSpaceComma(p1, p2):
    if not os.path.exists(p1):
        p1 = p1.replace("_space_", " ")
        p1 = p1.replace("_comma_", ",")
    if os.path.exists(p1):
        p2 = p2.replace(" ", "_r_space_r_");
        p2 = p2.replace(",", "_r_comma_r_");
    else:
        return "", ""
    return p1, p2

def saveOnCopy(mpaths, mtarget):
    for p1 in mpaths:
        p2 = p1.replace("/transforms/Methods/", "/handcrafted/top20/"+mtarget+"/")
        fp1, fp2 = handleSpaceComma(p1, p2)
        if len(fp1)==0 or len(fp2)==0:
            print(p1, "does not exist!")
        else:
            pathlib.Path(os.path.dirname(fp2)).mkdir(parents=True, exist_ok=True)
            shutil.copy2(fp1, fp2)

for jt in mDataTypes:
    for jc in mDataCats:
        fname = "../data/nall/" + jt + "/" + jc + "/*.txt"
        print("Start: ", fname)
        mTargetFiles = glob.glob(fname)
        for fname in mTargetFiles:
            mtarget = (fname.split("/")[-1]).replace(".txt","")
            mdf = pd.read_csv(fname, sep=",", names=["path"])
            saveOnCopy(list(mdf.path), mtarget)
            print("Done:", mtarget)
        print("Done: ", fname)

