import pandas as pd
import numpy as np
import os, pathlib, shutil
from sklearn.model_selection import train_test_split
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects

import seaborn as sns
sns.set_style('darkgrid')
sns.set_palette('muted')
sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})
mRS = 42

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation

# visualize the outputs of t-SNE
# Refs: http://blog.mahler83.net/2019/10/rotating-3d-t-sne-animated-gif-scatterplot-with-matplotlib/
def tsne_3d(tsne_data, mpath, df):
    fig = plt.figure(figsize=(10,10))
    ax = Axes3D(fig)
    colors = 'g', 'r'
    labels = '1', '0'

    for i, mcolor, mlabel in zip(range(len(labels)), colors, labels):
        ax.scatter(tsne_data[df[df.columns[-1]]==i, 0], tsne_data[df[df.columns[-1]]==i, 1], tsne_data[df[df.columns[-1]]==i, 2], s=30, c=mcolor, label=mlabel, alpha=0.5)
    fig.legend()
    
    def rotate(angle):
         ax.view_init(azim=angle)

    angle = 1
    ani = animation.FuncAnimation(fig, rotate, frames=np.arange(0, 360, angle), interval=100)
    ani.save(mpath, writer=animation.PillowWriter(fps=20))

# call t-SNE visualizer
mDataTypes = ["java-large"]
mDataCats = ["training"]
mTargets = ["equals", "setUp", "toString"]
types = ["flat"]

for jt in mDataTypes:
    for jc in mDataCats:
        for mtarget in mTargets:
            for ty in types:
                mpath = "../data/code2vec/" + jt + "/" + jc + "/" + ty + "/" + mtarget + ".csv"
                df = pd.read_csv(mpath, header=None)
                df = df.drop([df.columns[0], df.columns[1]], axis=1)
                mcols = ['f' + str(i) for i in range(1, len(df.columns)+1)]
                df.columns = mcols
                target_labels = df[df.columns[-1]].values
                feature_vectors = df.drop([df.columns[-1]], axis=1)
                tsne_data = TSNE(n_components=3, random_state=mRS).fit_transform(feature_vectors)
                mpath = "../result/code2vec/tsne/" + jt + "/" + jc + "/" + ty + "/" + mtarget + "_3d.gif"
                pathlib.Path(os.path.dirname(mpath)).mkdir(parents=True, exist_ok=True)
                tsne_3d(tsne_data, mpath, df)
                print ("Done : " + jt + "/" + jc + "/" + ty + "/" + mtarget)
