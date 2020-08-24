import os
import pathlib

import pandas as pd
from sklearn.manifold import TSNE

import config as cf
import helper as hp

# For each feature embeddings of method
for hfe_type in cf.HFE_TYPES:
    for emb_type in ["binary"]:  # cf.EMB_TYPES
        usual_root = cf.DATA_VEC + "/usual/{}/{}".format(hfe_type, emb_type)
        for target_name in ["equals", "run"]:  # cf.TOP_LABELS:
            usual_file = usual_root + "/" + target_name + "/test.csv"
            tSNE2d_file = usual_root + "/" + target_name + "/test_tSNE2d.png"

            df_test = pd.read_csv(usual_file)
            df_test["label"] = df_test["method"].apply(lambda x: 1 if x == target_name else 0)
            X, y = df_test.drop(["path", "method", "label"], axis=1), df_test["label"].tolist()

            data = TSNE(random_state=cf.MANUAL_SEED).fit_transform(X)
            data = pd.DataFrame(data=data[:, :])
            fig, _, = hp.tsne_scatter(data, y, cf.TOP_COLORS,
                                      [target_name + " (negative)", target_name + " (positive)"])

            pathlib.Path(os.path.dirname(tSNE2d_file)).mkdir(parents=True, exist_ok=True)
            fig.savefig(tSNE2d_file, bbox_inches="tight", dpi=400)
            print("t-SNE : {} - {} - {}".format(hfe_type, emb_type, target_name))
