import pandas as pd
from sklearn import preprocessing
import os, ast, pathlib, shutil
import config as cf

mEmbedSize = [384] # [embed_size(source+path+target)]

def get_df_by_target(mpath, mtarget):
    fname = mpath + "/raw/" + mtarget + ".csv"
    mcols = ["path","original","predict","embedding"]
    df = pd.read_csv(fname, names=mcols, header=None)
    df = df.drop(["predict"], axis=1)
    df["embedding"] = df["embedding"].apply(lambda x: eval(x))
    mcols = ['e' + str(i) for i in range(1, mEmbedSize[0] + 1)]
    df[mcols] = pd.DataFrame(df.embedding.values.tolist(), index=df.index)
    df = df.drop(["embedding"], axis=1)
    return df

mpath = "../data/code2vec/" + cf.DATASET
ntdf = get_df_by_target(mpath, "nonTarget")
ntdf["label"] = 0
for mtarget in cf.TOP_LABELS:
    tdf = get_df_by_target(mpath, mtarget)
    tdf["label"] = 1

    #flat df
    df_flat = pd.concat([tdf, ntdf], axis=0, ignore_index=True)
    fname = mpath + "/flat/" + mtarget + ".csv"
    pathlib.Path(os.path.dirname(fname)).mkdir(parents=True, exist_ok=True)
    df_flat.to_csv(fname, index=False, header=False)

    print("Done: ", mtarget, len(df_flat))
