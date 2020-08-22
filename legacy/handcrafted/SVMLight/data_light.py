import config as cf
import pandas as pd
from sklearn import preprocessing
import os, pathlib
import helper as hp

filetype = "onehot" #onehot/complexity
ph_file = cf.DATA_VEC.format("handcrafted") + "/{}/{}/{}"

# Split into methods
for partition in cf.PARTITIONS:
    part_file = ph_file.format(filetype, "multi/count", partition)
    df_part = pd.read_csv(part_file)
    for method in cf.TOP_LABELS:
        df_pos = df_part.loc[df_part['method'] == method]
        df_neg = df_part.loc[df_part['method'] != method]
        df_neg = df_neg.sample(frac=1, random_state=cf.LABELS2INDEX[method]).reset_index(drop=True)
        df_neg = df_neg.groupby('method').head(df_pos.shape[0]/(len(cf.TOP_LABELS)-1))
        df_method = pd.concat([df_pos, df_neg], ignore_index=True, sort =False)
        df_method = df_method.sample(frac=1, random_state=cf.MANUAL_SEED).reset_index(drop=True)

        #count
        df_count = df_method.copy()
        df_count['label'] = df_count['method'].apply(lambda x: +1 if x == method else -1)
        count_file = ph_file.format(filetype, "binary/count", method + "/" + partition)
        pathlib.Path(os.path.dirname(count_file)).mkdir(parents=True, exist_ok=True)
        df_count.to_csv(count_file, index=False)
        light_file = ph_file.format(filetype, "light/count", method + "/" + partition)
        hp.save_svm_light_format(df_count, light_file)

        #normalized
        df_norm = df_method.copy()
        for c in df_norm.columns[2:]:
            df_norm[[c]] = preprocessing.StandardScaler().fit_transform(df_norm[[c]])
        df_norm['label'] = df_norm['method'].apply(lambda x: +1 if x == method else -1)
        norm_file = ph_file.format(filetype, "binary/norm", method + "/" + partition)
        pathlib.Path(os.path.dirname(norm_file)).mkdir(parents=True, exist_ok=True)
        df_norm.to_csv(norm_file, index=False)
        light_file = ph_file.format(filetype, "light/norm", method + "/" + partition)
        hp.save_svm_light_format(df_norm, light_file)

        #binary
        df_binary = df_method.copy()
        for c in df_binary.columns[2:]:
            df_binary[c] = df_binary[c].apply(lambda x: 1 if x>0 else 0)
        df_binary['label'] = df_binary['method'].apply(lambda x: +1 if x == method else -1)
        binary_file = ph_file.format(filetype, "binary/binary", method + "/" + partition)
        pathlib.Path(os.path.dirname(binary_file)).mkdir(parents=True, exist_ok=True)
        df_binary.to_csv(binary_file, index=False)
        light_file = ph_file.format(filetype, "light/binary", method + "/" + partition)
        hp.save_svm_light_format(df_binary, light_file)

        #mix:binary[e1-e35]+normalized[e36-e53]
        df_mix = df_method.copy()
        for c in df_mix.columns[2:37]:
            df_mix[c] = df_mix[c].apply(lambda x: 1 if x>0 else 0)
        for c in df_mix.columns[37:]:
            df_mix[[c]] = preprocessing.StandardScaler().fit_transform(df_mix[[c]])
        df_mix['label'] = df_mix['method'].apply(lambda x: +1 if x == method else -1)
        mix_file = ph_file.format(filetype, "binary/mix", method + "/" + partition)
        pathlib.Path(os.path.dirname(mix_file)).mkdir(parents=True, exist_ok=True)
        df_mix.to_csv(mix_file, index=False)
        light_file = ph_file.format(filetype, "light/mix", method + "/" + partition)
        hp.save_svm_light_format(df_mix, light_file)

        print("Completed for {}-{} file.".format(method, partition))
