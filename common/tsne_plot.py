import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
import seaborn as sns
sns.set_style('darkgrid')
sns.set_palette('muted')
sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation

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

# Refs: http://blog.mahler83.net/2019/10/rotating-3d-t-sne-animated-gif-scatterplot-with-matplotlib/
def tsne_3d(tsne_data, mpath, df):
    fig = plt.figure(figsize=(10, 10))
    ax = Axes3D(fig)
    colors = 'g', 'r'
    labels = '1', '0'

    for i, mcolor, mlabel in zip(range(len(labels)), colors, labels):
        ax.scatter(tsne_data[df[df.columns[-1]] == i, 0], tsne_data[df[df.columns[-1]] == i, 1],
                   tsne_data[df[df.columns[-1]] == i, 2], s=30, c=mcolor, label=mlabel, alpha=0.5)
    fig.legend()

    def rotate(angle):
        ax.view_init(azim=angle)

    angle = 1
    ani = animation.FuncAnimation(fig, rotate, frames=np.arange(0, 360, angle), interval=100)
    ani.save(mpath, writer=animation.PillowWriter(fps=20))
