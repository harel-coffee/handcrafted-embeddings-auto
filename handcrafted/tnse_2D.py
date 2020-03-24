import pandas as pd
import numpy as np
import os, pathlib, shutil
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects

import seaborn as sns
sns.set_style('darkgrid')
sns.set_palette('muted')
sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})
mRS = 42

# visualize the outputs of t-SNE
# Refs: https://www.datacamp.com/community/tutorials/introduction-t-sne
def tsne_scatter(x, colors):
    num_classes = len(np.unique(colors))
    palette = np.array(sns.color_palette("hls", num_classes))

    plt.clf()
    f = plt.figure(figsize=(8, 8))
    ax = plt.subplot(aspect='equal')
    sc = ax.scatter(x[:,0], x[:,1], lw=0, s=40, c=palette[colors.astype(np.int)])
    plt.xlim(-25, 25)
    plt.ylim(-25, 25)
    ax.axis('off')
    ax.axis('tight')

    txts = []
    for i in range(num_classes):
        xtext, ytext = np.median(x[colors == i, :], axis=0)
        txt = ax.text(xtext, ytext, str(i), fontsize=24)
        txt.set_path_effects([
            PathEffects.Stroke(linewidth=5, foreground="w"),
            PathEffects.Normal()])
        txts.append(txt)

    return f, ax, sc, txts

# call t-SNE visualizer
mDataTypes = ["java-large"]
mDataCats = []
mTargets = []
types = ["count", "norm", "binary"]

for jt in mDataTypes:
    for jc in mDataCats:
        for mtarget in mTargets:
            for ty in types:
                mpath = "../data/handcrafted/" + jt + "/" + jc + "/" + ty + "/" + mtarget + ".csv"
                df = pd.read_csv(mpath, header=None)
                df = df.drop([df.columns[0], df.columns[1]], axis=1)
                mcols = ['f' + str(i) for i in range(1, len(df.columns)+1)]
                df.columns = mcols
                target_labels = df[df.columns[-1]].values
                feature_vectors = df.drop([df.columns[-1]], axis=1)
                tsne_data = TSNE(random_state=mRS).fit_transform(feature_vectors)
                fig, _, _, _ = tsne_scatter(tsne_data, target_labels)
                mtitle = mtarget + "-" + ty + ": " + "1(green) = " + mtarget + " and 0(red) = non-" + mtarget
                fig.suptitle(mtitle, fontsize=16)
                mpath = "../result/handcrafted/tsne/" + jt + "/" + jc + "/" + ty + "/" + mtarget + "_2d.png"
                pathlib.Path(os.path.dirname(mpath)).mkdir(parents=True, exist_ok=True)
                fig.savefig(mpath, bbox_inches = "tight", dpi=400) 
                print ("Done : " + jt + "/" + jc + "/" + ty + "/" + mtarget)

