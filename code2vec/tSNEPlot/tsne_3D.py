import pandas as pd
import os, pathlib
from sklearn.manifold import TSNE
import config as cf
import common.tsne_plot as mts

types = ["flat"]

for mtarget in cf.TOP_LABELS:
    for ty in types:
        mpath = "../../data/code2vec/" + cf.DATASET + "/" + ty + "/" + mtarget + ".csv"
        df = pd.read_csv(mpath, header=None)
        df = df.drop([df.columns[0], df.columns[1]], axis=1)
        mcols = ['f' + str(i) for i in range(1, len(df.columns)+1)]
        df.columns = mcols
        target_labels = df[df.columns[-1]].values
        feature_vectors = df.drop([df.columns[-1]], axis=1)
        tsne_data = TSNE(n_components=3, random_state=cf.MANUAL_SEED).fit_transform(feature_vectors)
        mpath = "../../result/code2vec/tsne/" + cf.DATASET + "/" + ty + "/" + mtarget + "_3d.gif"
        pathlib.Path(os.path.dirname(mpath)).mkdir(parents=True, exist_ok=True)
        mts.tsne_3d(tsne_data, mpath, df)
        print ("Done : " + cf.DATASET + "/" + ty + "/" + mtarget)
