import pandas as pd
import config as cf
from sklearn.feature_selection import mutual_info_classif
import os, pathlib
import scipy.stats

ig_threshold = 0.1
is_discrete = False

# discrete_features --> True/False
EMB_GROUPS = [
    ("handcrafted", "onehot/multi/binary", True),
    ("handcrafted", "onehot/multi/norm", False),
    ("code2vec", "flat", False)
]

label_dict = {"binary": "HF(Binary)", "norm": "HF(Normalized)", "flat": "code2vec"}

PH_DATA_FILE = cf.DATA_VEC + "/{}/test.csv"
PH_RESULT_FILE = cf.RESULT_PATH + "mutual_info/{}/" + cf.DATASET + "/{}/test.csv"


def get_entropy(data):
    s_data = pd.Series(data)
    p_data = s_data.value_counts()
    entropy = scipy.stats.entropy(p_data)
    return entropy


for emb_grp in EMB_GROUPS:
    emb_type, feature_type, is_discrete = emb_grp
    print("\n{}:\n".format(emb_grp))
    short_feature_type = label_dict[feature_type.split("/")[-1]]

    DATA_FILE = PH_DATA_FILE.format(emb_type, feature_type)
    RESULT_FILE = PH_RESULT_FILE.format(emb_type, feature_type)

    df_test = pd.read_csv(DATA_FILE)
    df_test["label"] = df_test["method"].apply(lambda x: cf.LABELS2INDEX[x])
    X, y = df_test.drop(["path", "method", "label"], axis=1), df_test["label"].tolist()

    Ixy = list(mutual_info_classif(X, y, discrete_features=is_discrete))
    H_y = get_entropy(y)
    Ixy = [x / H_y for x in Ixy]
    sort_Ixy = sorted(Ixy, reverse=True)
    rank_Ixy = [sort_Ixy.index(x) + 1 for x in Ixy]

    ig_features = []
    pathlib.Path(os.path.dirname(RESULT_FILE)).mkdir(parents=True, exist_ok=True)
    with open(RESULT_FILE, 'w') as f_Ixy:
        f_Ixy.write("{},{},{},{},{}\n".format("emb_type", "feature_type", "feature", "rank", "mutual_info"))
        for ft, rank, ig, in zip(X.columns, rank_Ixy, Ixy):
            f_Ixy.write("{},{},{},{},{}\n".format(emb_type, short_feature_type, ft, rank, ig))
            print("{},{},{},{},{}".format(emb_type, short_feature_type, ft, rank, ig))
            if ig >= ig_threshold: ig_features.append(ft)

    print("\n{}\n".format("-------"))
    print("{} ig [{}] = {}".format(emb_grp, len(ig_features), ig_features))
    print("\n{}\n".format("-------"))
