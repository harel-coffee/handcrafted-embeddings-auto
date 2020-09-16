import pandas as pd
import os, pathlib
from sklearn.manifold import TSNE
import config as cf
import common.tsne_plot as mts
import _pickle as pk

types = ["flat", "pca"]

def get_pca_data(filename):
    dict_xy = {}
    with open(filename, 'rb') as xy_file:
        dict_xy = pk.load(xy_file)
    X_all, y_all = dict_xy["Xpk"], dict_xy["ypk"]
    return X_all, y_all

def get_df_data(filename):
    df = pd.read_csv(filename, header=None)
    df = df.drop([df.columns[0], df.columns[1]], axis=1)
    mcols = ['f' + str(i) for i in range(1, len(df.columns)+1)]
    df.columns = mcols
    y_all = df[df.columns[-1]].values
    X_all = df.drop([df.columns[-1]], axis=1)
    return X_all, y_all

for mtarget in cf.TOP_LABELS:
    for ty in types:
        feature_vectors, target_labels = "", ""
        if ty == "flat":
            mpath = "../../data/code2vec/" + cf.DATASET + "/" + ty + "/" + mtarget + ".csv"
            feature_vectors, target_labels = get_df_data(mpath)
        elif ty == "pca":
            mpath = "../../data/code2vec/" + cf.DATASET + "/" + ty + "/" + mtarget + ".pk"
            feature_vectors, target_labels = get_pca_data(mpath)
        tsne_data = TSNE(random_state=cf.MANUAL_SEED).fit_transform(feature_vectors)
        fig, _, _, _ = mts.tsne_scatter(tsne_data, target_labels)
        mtitle = mtarget + "-" + ty + ": " + "1(green) = " + mtarget + " and 0(red) = non-" + mtarget
        fig.suptitle(mtitle, fontsize=16)
        mpath = "../../result/code2vec/tsne/" + cf.DATASET + "/" + ty + "/" + mtarget + "_2d.png"
        pathlib.Path(os.path.dirname(mpath)).mkdir(parents=True, exist_ok=True)
        fig.savefig(mpath, bbox_inches = "tight", dpi=400)
        print ("Done : " + cf.DATASET + "/" + ty + "/" + mtarget)
