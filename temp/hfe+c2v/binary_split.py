import config as cf
import pandas as pd
import os, pathlib
import helper as hp

ph_hfe = cf.DATA_VEC.format("handcrafted") + "/{}/{}/{}"
ph_c2v = cf.DATA_VEC.format("code2vec")    + "/{}/{}/{}"
ph_c2v_hfe = cf.DATA_VEC.format("c2v_hfe") + "/{}/{}/{}"

# Join code2vec and hfe
for emb_type in cf.HFE_TYPES:
    for method in cf.TOP_LABELS:
        for partition in cf.PARTITIONS:
            c2v_file = ph_c2v.format("binary", method, partition)
            df_c2v = pd.read_csv(c2v_file)

            hfe_file = ph_hfe.format("binary", emb_type, method + "/" + partition)
            df_hfe = pd.read_csv(hfe_file)

            df_c2v_hfe = df_c2v.merge(df_hfe, on=['path', 'method', 'label'])
            df_c2v_hfe = df_c2v_hfe.drop(['label'], axis=1)
            df_c2v_hfe['label'] = df_c2v['label']

            c2v_hfe_file = ph_c2v_hfe.format("binary", emb_type, method + "/" + partition)
            pathlib.Path(os.path.dirname(c2v_hfe_file)).mkdir(parents=True, exist_ok=True)
            df_c2v_hfe.to_csv(c2v_hfe_file, index=False)

            light_file = ph_c2v_hfe.format("light", emb_type, method + "/" + partition)
            pathlib.Path(os.path.dirname(light_file)).mkdir(parents=True, exist_ok=True)
            hp.save_svm_light_format(df_c2v_hfe, light_file)

            print("Completed for {}-{}-{} file.".format(emb_type, method, partition))
