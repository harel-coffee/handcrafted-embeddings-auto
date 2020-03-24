import pandas as pd
from sklearn import preprocessing
import os, ast, pathlib, shutil

mDataTypes = ["java-large"]
mDataCats = ["t470"]
mTargets = ["equals", "main", "setUp", "onCreate", "toString", "run", "hashCode", "init", "execute", "get", "close", "start", "add", "write", "create", "tearDown", "clear", "read", "reset", "update"]
mTargets = ["equals", "main", "setUp", "onCreate", "toString", "run", "hashCode", "init", "execute", "get", "close"]
mEmbedSize = [384] # [embed_size(source+path+target)]

def getDataframeByTarget(mpath, mtarget):
    fname = mpath + "/raw/" + mtarget + ".csv"
    mcols = ["path","original","predict","embedding"]
    df = pd.read_csv(fname, names=mcols, header=None)
    df = df.drop(["predict"], axis=1)
    df["embedding"] = df["embedding"].apply(lambda x: eval(x))
    mcols = ['e' + str(i) for i in range(1, mEmbedSize[0] + 1)]
    df[mcols] = pd.DataFrame(df.embedding.values.tolist(), index=df.index)
    df = df.drop(["embedding"], axis=1)
    return df

for jt in mDataTypes:
    for jc in mDataCats:
        mpath = "../data/code2vec/" + jt + "/" + jc
        ntdf = getDataframeByTarget(mpath, "nonTarget")
        ntdf["label"] = 0
        for mtarget in mTargets:
            tdf = getDataframeByTarget(mpath, mtarget)
            tdf["label"] = 1
            
            #flat dataframe
            df_flat = pd.concat([tdf, ntdf], axis=0, ignore_index=True)
            fname = mpath + "/flat/" + mtarget + ".csv"
            pathlib.Path(os.path.dirname(fname)).mkdir(parents=True, exist_ok=True)
            df_flat.to_csv(fname, index=False, header=False)

            print("Done: ", mtarget, len(df_flat))
