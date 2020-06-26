import config as cf
import pandas as pd
from sklearn import preprocessing
import os, pathlib
import helper as hp

filetype1 = "onehot" #onehot/complexity
filetype2 = "infogain"  # infogain/entropy

ig_bin_ft  =  ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e9', 'e12', 'e13', 'e14', 'e15', 'e16', 'e19', 'e24', 'e32', 'e39', 'e40', 'e43', 'e44', 'e45', 'e46', 'e53']
ig_norm_ft =  ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e9', 'e12', 'e13', 'e14', 'e15', 'e16', 'e19', 'e24', 'e27', 'e32', 'e33', 'e36', 'e37', 'e39', 'e40', 'e41', 'e43', 'e44', 'e45', 'e46', 'e47', 'e48', 'e50', 'e51', 'e52', 'e53']

ph_file = cf.DATA_VEC.format("handcrafted") + "/{}/{}/{}"

# Split into methods
for partition in cf.PARTITIONS:
    for method in cf.TOP_LABELS:
        #count
        count_file = ph_file.format(filetype1, "binary/count", method + "/" + partition)
        df_count = pd.read_csv(count_file)

        #normalized
        df_norm = df_count.copy()
        ig_norm_cols = list(df_norm.columns[0:2]) + ig_norm_ft + [df_norm.columns[-1]]
        df_norm = df_norm[ig_norm_cols]
        for c in df_norm.columns[2:-1]:
            df_norm[[c]] = preprocessing.StandardScaler().fit_transform(df_norm[[c]])
        df_norm['label'] = df_norm['method'].apply(lambda x: +1 if x == method else -1)
        norm_file = ph_file.format(filetype2, "binary/norm", method + "/" + partition)
        pathlib.Path(os.path.dirname(norm_file)).mkdir(parents=True, exist_ok=True)
        df_norm.to_csv(norm_file, index=False)
        light_file = ph_file.format(filetype2, "light/norm", method + "/" + partition)
        hp.save_svm_light_format(df_norm, light_file)

        #binary
        df_binary = df_count.copy()
        ig_bin_cols = list(df_binary.columns[0:2]) + ig_bin_ft + [df_binary.columns[-1]]
        df_binary = df_binary[ig_bin_cols]
        for c in df_binary.columns[2:-1]:
            df_binary[c] = df_binary[c].apply(lambda x: 1 if x>0 else 0)
        df_binary['label'] = df_binary['method'].apply(lambda x: +1 if x == method else -1)
        binary_file = ph_file.format(filetype2, "binary/binary", method + "/" + partition)
        pathlib.Path(os.path.dirname(binary_file)).mkdir(parents=True, exist_ok=True)
        df_binary.to_csv(binary_file, index=False)
        light_file = ph_file.format(filetype2, "light/binary", method + "/" + partition)
        hp.save_svm_light_format(df_binary, light_file)

        print("Completed for {}-{} file.".format(method, partition))
