import config as cf
import pandas as pd
import os, pathlib
import helper as hp

# Split into methods
for partition in cf.PARTITIONS:
    file_c2v_all = cf.DATA_VEC.format("code2vec") + "/flat/" + partition
    df_c2v_all = pd.read_csv(file_c2v_all)
    for method in cf.TOP_LABELS:
        file_hfe_method = cf.DATA_VEC.format("handcrafted") + "/binary/count/" + method + "/" + partition
        df_hfe_method = pd.read_csv(file_hfe_method)
        idx_c2v = df_c2v_all.set_index('path').index
        idx_hfe = df_hfe_method.set_index('path').index
        df_c2v_method = df_c2v_all[idx_c2v.isin(idx_hfe)]
        df_c2v_method['label'] = df_c2v_method['method'].apply(lambda x: +1 if x == method else -1)
        binary_file = cf.DATA_VEC.format("code2vec") + "/binary/" + method + "/" + partition
        pathlib.Path(os.path.dirname(binary_file)).mkdir(parents=True, exist_ok=True)
        df_c2v_method.to_csv(binary_file, index=False)

        # Light format file
        light_file = cf.DATA_VEC.format("code2vec") + "/light/" + method + "/" + partition
        hp.save_svm_light_format(df_c2v_method, light_file)

        print("Completed for {}-{} file.".format(method, partition))
