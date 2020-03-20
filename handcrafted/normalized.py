import pandas as pd
from sklearn import preprocessing
import os, pathlib, shutil

mDataTypes = ["java-large"]
mDataCats = ["t470"]
mTargets = ["equals", "main", "setUp", "onCreate", "toString", "run", "hashCode", "init", "execute", "get", "close", "start", "add", "write", "create", "tearDown", "clear", "read", "reset", "update"]
mTargets = ["equals", "main", "setUp", "onCreate", "toString", "run", "hashCode", "init", "execute", "get", "close"]

for jt in mDataTypes:
    for jc in mDataCats:
        for mtarget in mTargets:
            mPath = "../data/handcrafted/" + jt + "/" + jc
            fname = mPath + "/count/" + mtarget + ".csv"
            df = pd.read_csv(fname, header=None)

            #normalized dataframe
            df_norm = df.copy()
            for c in df_norm.columns[2:-1]:
                df_norm[[c]] = preprocessing.StandardScaler().fit_transform(df_norm[[c]])
            fname = mPath + "/norm/" + mtarget + ".csv"
            pathlib.Path(os.path.dirname(fname)).mkdir(parents=True, exist_ok=True)
            df_norm.to_csv(fname, index=False, header=False)

            #binary dataframe
            df_binary = df.copy()
            for c in df_binary.columns[2:-1]:
                df_binary[c] = df_binary[c].apply(lambda x: 1 if x>0 else 0)
            fname = mPath + "/binary/" + mtarget + ".csv"
            pathlib.Path(os.path.dirname(fname)).mkdir(parents=True, exist_ok=True)
            df_binary.to_csv(fname, index=False, header=False)

            print("Done: ", mtarget, len(df_norm), len(df_binary))

