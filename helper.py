import os
import pathlib

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import dump_svmlight_file

import config as cf


# Save Log Message
def save_log_msg(msg):
    print(msg)
    with open(cf.LOG_PATH, "a") as log_file:
        log_file.write(msg + "\n")


# Save Light Format
def save_svm_light_format(df, light_file):
    light_file = light_file.replace(".csv", ".dat")
    vector_X, target_y = df.iloc[:, 2:-1], df.iloc[:, -1]
    pathlib.Path(os.path.dirname(light_file)).mkdir(parents=True, exist_ok=True)
    with open(light_file, "wb") as f_light:
        dump_svmlight_file(X=vector_X, y=target_y, f=f_light, zero_based=False, multilabel=False)


# Parse output of svm
def parse_svm_light_output(output):
    acc, pre, rec, f1s = 0.0, 0.0, 0.0, 0.0
    try:
        lines = output.split('\n')
        for line in lines:
            if "Accuracy" in line:
                acc = float((line.split('%')[0]).split()[-1])
            elif "Precision" in line:
                pre = float((line.split('%')[0]).split()[-1])
                rec = float((line.split('%')[1]).replace('/', ''))
                f1s = round(2 * (pre * rec) / (pre + rec), 2)
    except:
        acc, pre, rec, f1s = -1.0, -1.0, -1.0, -1.0
    return acc, pre, rec, f1s


# Draw 2d t-SNE plot
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
