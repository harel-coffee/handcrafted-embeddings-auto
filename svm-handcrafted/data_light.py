import os
import pathlib

import pandas as pd
from sklearn import preprocessing

import config as cf
import helper as hp

# split into methods
for hfe_type in cf.HFE_TYPES:
    for partition in cf.PARTITIONS:
        part_file = cf.DATA_VEC + "/all/{}/{}.csv".format(hfe_type, partition)
        df_part = pd.read_csv(part_file, header=None)
        df_part.columns = ["path", "method"] + ["e"+str(i) for i in range(1, df_part.shape[1]-1)]
        for method in cf.TOP_LABELS:
            ph_file = cf.DATA_VEC + "/{}/" + hfe_type + "/{}" + "/{}/{}.csv".format(method, partition)

            def save_usual_and_light_file(df_this, emb_this):
                df_this['label'] = df_this['method'].apply(lambda x: +1 if x == method else -1)
                usual_file = ph_file.format("usual", emb_this)
                pathlib.Path(os.path.dirname(usual_file)).mkdir(parents=True, exist_ok=True)
                df_this.to_csv(usual_file, index=False)
                light_file = ph_file.format("light", emb_this)
                pathlib.Path(os.path.dirname(light_file)).mkdir(parents=True, exist_ok=True)
                hp.save_svm_light_format(df_this, light_file)

            # pos & neg
            df_pos = df_part.loc[df_part['method'] == method]
            df_neg = df_part.loc[df_part['method'] != method]
            df_neg = df_neg.sample(frac=1, random_state=cf.LABELS2INDEX[method]).reset_index(drop=True)
            df_neg = df_neg.head(df_pos.shape[0])
            df_method = pd.concat([df_pos, df_neg], ignore_index=True, sort=False)
            df_method = df_method.sample(frac=1, random_state=cf.MANUAL_SEED).reset_index(drop=True)

            # count
            df_count = df_method.copy()
            save_usual_and_light_file(df_count, "count")

            # normalized
            df_norm = df_method.copy()
            for c in df_norm.columns[2:]:
                df_norm[[c]] = preprocessing.StandardScaler().fit_transform(df_norm[[c]])
            save_usual_and_light_file(df_norm, "norm")

            # binary
            df_binary = df_method.copy()
            if hfe_type == "HC33X":
                for c in df_binary.columns[2:35]:
                    df_binary[c] = df_binary[c].apply(lambda x: 1 if x > 0 else 0)
                for c in df_binary.columns[35:]:
                    df_binary[[c]] = preprocessing.StandardScaler().fit_transform(df_binary[[c]])
            else:
                for c in df_binary.columns[2:]:
                    df_binary[c] = df_binary[c].apply(lambda x: 1 if x > 0 else 0)
            save_usual_and_light_file(df_binary, "binary")

            print("[{}-{}-{}] df_pos = {}, df_neg = {}".format(hfe_type, partition, method, len(df_pos), len(df_neg)))
