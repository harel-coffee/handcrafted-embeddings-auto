import pandas as pd
import numpy as np
import scipy as sp
from sklearn.feature_selection import mutual_info_classif
import config as cf

# Path
data_path = cf.DATA_VEC + "/{}/"
data_test = "train.csv"

VecEmb = [
    ("handcrafted", "HC33/binary/binary", True),
    ("handcrafted", "HC33/binary/norm", False),
    ("handcrafted", "HC33X/binary/norm", False),
    ("code2vec", "binary", False)
]

TopLabels = ["equals", "main", "setUp", "onCreate", "toString", "run", "hashCode", "init", "execute", "get"]
FeatureIndex = {"equals": (1, 4), "main": (5, 6), "setUp": (7, 11), "onCreate": (12, 15), "toString": (16, 20),
                "run": (21, 23), "hashCode": (24, 25), "init": (26, 28), "execute": (29, 31), "get": (32, 33)}


# X and y
def calc_inf_gain(m, v):
    df_test = pd.read_csv(data_path.format(v[0], v[1]) + "/" + m + "/" + data_test)
    df_test["label"] = df_test["method"].apply(lambda x: 1 if x == m else 0)
    X, y = df_test.drop(["path", "method", "label"], axis=1), df_test["label"].tolist()

    # mutual_info
    IGxy = list(mutual_info_classif(X, y, discrete_features=v[2]))
    print("{} = {}".format(m, IGxy))

    # method-specific IG
    # if v[0] == "handcrafted":
    #     sidx, eidx = FeatureIndex[m][0]-1, FeatureIndex[m][1]
    #     IGsub = [IGxy[i] for i in range(sidx, eidx)]
    #     print("{}({}):\nAll:{}\nSub:{}\n".format(m, FeatureIndex[m], IGxy, IGsub))
    #     print("{}: {}\nmin={}, max={}, mean={}\n".format(m, IGsub, np.min(IGsub), np.max(IGsub), np.mean(IGsub)))

    # print rank
    th = 0.25  # TODO
    all_cols = list(X.columns)
    sort_IGxy = sorted(IGxy, reverse=True)
    rank_IGxy = [sort_IGxy.index(x) + 1 for x in IGxy]
    rank_cols = [all_cols[i] for i in range(len(all_cols)) if rank_IGxy[i] < th * len(rank_IGxy)]

    # print("all_cols ({}) = {}".format(len(all_cols), all_cols))
    print("rank_cols ({}) = {}".format(len(rank_cols), rank_cols))

    # stats.describe
    # print("====================")
    # f = len(df_test) == (len(df_test.loc[df_test["label"] == 1]) + len(df_test.loc[df_test["label"] == 0]))
    # r = sp.stats.describe(IGxy)
    # r0 = [m,k[0],r[0],r[1][0],r[1][1],r[2],r[3],r[4],r[5]]
    # print(m, f)
    # print(r)
    # print(r0)


# Top 10 labels
for v in VecEmb:
    print(v)
    for m in TopLabels:
        calc_inf_gain(m, v)
        break
    print()
