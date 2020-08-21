import config as cf
import pandas as pd
from sklearn import preprocessing
import os, pathlib
import helper as hp

filetype = "onehot"  # onehot/complexity
ph_file = cf.DATA_VEC.format("handcrafted") + "/{}/{}/{}"

# Split into methods
for partition in cf.PARTITIONS:
    filetype = "onehot"  # tmp
    part_file = ph_file.format(filetype, "multi/count", partition)
    df_part = pd.read_csv(part_file)
    for method in cf.TOP_LABELS:
        df_pos = df_part.loc[df_part['method'] == method]
        df_neg = df_part.loc[df_part['method'] != method]
        df_neg = df_neg.sample(frac=1, random_state=cf.LABELS2INDEX[method]).reset_index(drop=True)
        df_neg = df_neg.groupby('method').head(df_pos.shape[0] / (len(cf.TOP_LABELS) - 1))
        df_method = pd.concat([df_pos, df_neg], ignore_index=True, sort=False)
        df_method = df_method.sample(frac=1, random_state=cf.MANUAL_SEED).reset_index(drop=True)

        # Start
        cur_cols = ['path', 'method', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11', 'e12', 'e13',
                    'e14', 'e15', 'e16', 'e17', 'e18', 'e19', 'e20', 'e21', 'e22', 'e23', 'e24', 'e25', 'e26', 'e27',
                    'e28', 'e29', 'e30', 'e31', 'e32', 'e33', 'e34', 'e35', 'LOC', 'Block', 'BasicBlock', 'Parameter',
                    'LocalVariable', 'GlobalVariable', 'Loop', 'Jump', 'Decision', 'Condition', 'Instance', 'Function',
                    'TryCatch', 'Thread', 'ASTNode', 'ASTToken', 'CFGStatement', 'CFGBranch']

        ig_cols_75 = ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e9', 'e10', 'e11', 'e12', 'e13', 'e14', 'e15', 'e16',
                      'e18', 'e19', 'e22', 'e24', 'e26', 'e27', 'e28', 'e30', 'e32']
        ig_cols_25 = ['e1', 'e2', 'e3', 'e4', 'e6', 'e9', 'e27', 'e32']

        req_cols = ['path', 'method'] + ig_cols_25 # TODO
        filetype = "IG25"  # TODO
        mix_binary = False  # TODO

        df_method.columns = cur_cols
        df_method = df_method[req_cols]
        # End

        # count
        df_count = df_method.copy()
        df_count['label'] = df_count['method'].apply(lambda x: +1 if x == method else -1)
        count_file = ph_file.format(filetype, "binary/count", method + "/" + partition)
        pathlib.Path(os.path.dirname(count_file)).mkdir(parents=True, exist_ok=True)
        df_count.to_csv(count_file, index=False)
        light_file = ph_file.format(filetype, "light/count", method + "/" + partition)
        hp.save_svm_light_format(df_count, light_file)

        # normalized
        df_norm = df_method.copy()
        for c in df_norm.columns[2:]:
            df_norm[[c]] = preprocessing.StandardScaler().fit_transform(df_norm[[c]])
        df_norm['label'] = df_norm['method'].apply(lambda x: +1 if x == method else -1)
        norm_file = ph_file.format(filetype, "binary/norm", method + "/" + partition)
        pathlib.Path(os.path.dirname(norm_file)).mkdir(parents=True, exist_ok=True)
        df_norm.to_csv(norm_file, index=False)
        light_file = ph_file.format(filetype, "light/norm", method + "/" + partition)
        hp.save_svm_light_format(df_norm, light_file)

        # binary
        df_binary = df_method.copy()
        if mix_binary:
            for c in df_binary.columns[2:35]:
                df_binary[c] = df_binary[c].apply(lambda x: 1 if x > 0 else 0)
            for c in df_binary.columns[35:]:
                df_binary[[c]] = preprocessing.StandardScaler().fit_transform(df_binary[[c]])
        else:
            for c in df_binary.columns[2:]:
                df_binary[c] = df_binary[c].apply(lambda x: 1 if x > 0 else 0)
        df_binary['label'] = df_binary['method'].apply(lambda x: +1 if x == method else -1)
        binary_file = ph_file.format(filetype, "binary/binary", method + "/" + partition)
        pathlib.Path(os.path.dirname(binary_file)).mkdir(parents=True, exist_ok=True)
        df_binary.to_csv(binary_file, index=False)
        light_file = ph_file.format(filetype, "light/binary", method + "/" + partition)
        hp.save_svm_light_format(df_binary, light_file)

        print("Completed for {}-{} file.".format(method, partition))
