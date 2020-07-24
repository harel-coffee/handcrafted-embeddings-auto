import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('darkgrid')
sns.set_palette('muted')
sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation


def tsne_scatter(x, y, colors, labels):
    classes = list(np.unique(y))
    plt.clf()
    fig, ax = plt.subplots(figsize=(8, 8))
    for i in classes:
        x_rows = np.where(np.array(y, dtype=np.int) == i)[0].tolist()
        ax.scatter(x.iloc[x_rows, 0], x.iloc[x_rows, 1],
                   s=40, alpha=0.9, c=colors[i], label=labels[i])
    ax.legend(loc='upper right')
    ax.grid(False)
    ax.set_facecolor('white')
    for spine in ['left', 'right', 'top', 'bottom']:
        ax.spines[spine].set_color('black')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()
    return fig, ax


# Refs: https://www.datacamp.com/community/tutorials/introduction-t-sne
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
