import pandas as pd
import os, pathlib
from sklearn.manifold import TSNE
import config as cf
import common.tsne_plot as mts

types = ["count", "norm", "binary"]

for mtarget in cf.TOP_LABELS:
    for ty in types:
        mpath = "../../data/handcrafted/" + cf.DATASET + "/" + ty + "/" + mtarget + ".csv"
        df = pd.read_csv(mpath, header=None)
        df = df.drop([df.columns[0], df.columns[1]], axis=1)
        mcols = ['f' + str(i) for i in range(1, len(df.columns)+1)]
        df.columns = mcols
        target_labels = df[df.columns[-1]].values
        feature_vectors = df.drop([df.columns[-1]], axis=1)
        tsne_data = TSNE(random_state=cf.MANUAL_SEED).fit_transform(feature_vectors)
        fig, _, _, _ = mts.tsne_scatter(tsne_data, target_labels)
        mtitle = mtarget + "-" + ty + ": " + "1(green) = " + mtarget + " and 0(red) = non-" + mtarget
        fig.suptitle(mtitle, fontsize=16)
        mpath = "../../result/handcrafted/tsne/" + cf.DATASET + "/" + ty + "/" + mtarget + "_2d.png"
        pathlib.Path(os.path.dirname(mpath)).mkdir(parents=True, exist_ok=True)
        fig.savefig(mpath, bbox_inches = "tight", dpi=400)
        print ("Done : " + cf.DATASET + "/" + ty + "/" + mtarget)
