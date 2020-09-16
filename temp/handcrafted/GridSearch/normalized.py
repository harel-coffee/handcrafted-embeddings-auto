import pandas as pd
from sklearn import preprocessing
import os, pathlib, shutil
import config as cf

for mtarget in cf.TOP_LABELS:
    mpath = "../../data/handcrafted/" + cf.DATASET
    fname = mpath + "/count/" + mtarget + ".csv"
    df = pd.read_csv(fname, header=None)

    #normalized df
    df_norm = df.copy()
    for c in df_norm.columns[2:-1]:
        df_norm[[c]] = preprocessing.StandardScaler().fit_transform(df_norm[[c]])
    fname = mpath + "/norm/" + mtarget + ".csv"
    pathlib.Path(os.path.dirname(fname)).mkdir(parents=True, exist_ok=True)
    df_norm.to_csv(fname, index=False, header=False)

    #binary df
    df_binary = df.copy()
    for c in df_binary.columns[2:-1]:
        df_binary[c] = df_binary[c].apply(lambda x: 1 if x>0 else 0)
    fname = mpath + "/binary/" + mtarget + ".csv"
    pathlib.Path(os.path.dirname(fname)).mkdir(parents=True, exist_ok=True)
    df_binary.to_csv(fname, index=False, header=False)

    print("Done: ", mtarget, len(df_norm), len(df_binary))
