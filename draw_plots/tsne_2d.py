import pandas as pd
import os, pathlib
from sklearn.manifold import TSNE
import config as cf
import common.tsne_plot as mts

methods = ["equals", "run"]

EMB_GROUPS = [
    ("handcrafted", "onehot/binary/binary"),
    ("code2vec", "binary")
]

PH_DATA_FILE = cf.DATA_VEC + "/{}/{}/test.csv"
PH_RESULT_FILE = cf.RESULT_PATH + "tsne_2d/{}/" + cf.DATASET + "/{}/{}_2d.png"

for target_name in methods:
    for emb_grp in EMB_GROUPS:
        emb_type, feature_type = emb_grp
        print("\n{}:\n".format(emb_grp))

        DATA_FILE = PH_DATA_FILE.format(emb_type, feature_type, target_name)
        RESULT_FILE = PH_RESULT_FILE.format(emb_type, feature_type, target_name)

        df_test = pd.read_csv(DATA_FILE)
        df_test["label"] = df_test["method"].apply(lambda x: 1 if x == target_name else 0)
        X, y = df_test.drop(["path", "method", "label"], axis=1), df_test["label"].tolist()

        data = TSNE(random_state=cf.MANUAL_SEED).fit_transform(X)
        data = pd.DataFrame(data=data[:, :])
        fig, _, = mts.tsne_scatter(data, y, cf.colors,
                    [target_name + " (negative)", target_name + " (positive)"])
        #fig.suptitle("title", fontsize=16)

        pathlib.Path(os.path.dirname(RESULT_FILE)).mkdir(parents=True, exist_ok=True)
        fig.savefig(RESULT_FILE, bbox_inches="tight", dpi=400)
        print("Done : {} - {}".format(emb_type, target_name))
