import pandas as pd
import config as cf
from sklearn.feature_selection import mutual_info_classif
import os, pathlib

EMB_GROUPS = [
    ("handcrafted", "onehot/multi/binary"),
    ("handcrafted", "onehot/multi/norm")
]
ig_threshold = 0.1

PH_DATA_FILE   = cf.DATA_VEC + "/{}/test.csv"
PH_RESULT_FILE = cf.RESULT_PATH + "mutual_info/{}/" + cf.DATASET + "/{}/test.csv"

for emb_grp in EMB_GROUPS:
    emb_type, feature_type = emb_grp
    print("\n{}:\n".format(emb_grp))

    DATA_FILE   = PH_DATA_FILE.format(emb_type, feature_type)
    RESULT_FILE = PH_RESULT_FILE.format(emb_type, feature_type)

    df_test  = pd.read_csv(DATA_FILE)
    df_test["label"] = df_test["method"].apply(lambda x: cf.LABELS2INDEX[x])
    X, y = df_test.drop(["path","method","label"], axis=1), df_test["label"].tolist()

    Ixy = list(mutual_info_classif(X, y, discrete_features=True))
    sort_Ixy = sorted(Ixy, reverse=True)
    rank_Ixy = [sort_Ixy.index(x) for x in Ixy]

    ig_features = []
    pathlib.Path(os.path.dirname(RESULT_FILE)).mkdir(parents=True, exist_ok=True)
    with open(RESULT_FILE, 'w') as f_Ixy:
        f_Ixy.write("{} : {} : {}\n".format("feature", "rank", "mutual_info"))
        for ft, rank, ig, in zip(X.columns, rank_Ixy, Ixy):
            f_Ixy.write("{},{},{}\n".format(ft, rank, ig))
            print("{},{},{}".format(ft, rank, ig))
            if ig >= ig_threshold: ig_features.append(ft)

    print("\n{}\n".format("-------"))
    print("ig_features = ", ig_features)
    print("\n{}\n".format("-------"))
