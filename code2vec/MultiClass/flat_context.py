import config as cf
import pandas as pd
import os, pathlib

# Set Params
EMB_TYPE = "code2vec"
FEATURE_TYPE = "vector"
cf.auto_update_types(EMB_TYPE, FEATURE_TYPE)
EMB_SIZE = 384

# Execution
for file_name in cf.PARTITIONS:
    file_path = cf.DATA_VEC + "/vec/" + file_name
    print("Loading vec embedding from {}...".format(file_path))
    cols_name = ["path", "method", "predict", "embedding"]
    df = pd.read_csv(file_path, names=cols_name)
    def fix_method_name(m):
        if "|" in m:
            m = m.split("|")
            m = [m[0]] + [x.capitalize() for x in m[1:]]
            m = "".join(m)
        return m
    df["method"] = df["method"].apply(lambda m: fix_method_name(m))
    df["predict"] = df["predict"].apply(lambda m: fix_method_name(m))
    df = df.drop(["predict"], axis=1)
    def get_numeric_embedding(emb):
        emb = (emb[1:-1]).split()
        emb = [float(x) for x in emb]
        return emb
    df["embedding"] = df["embedding"].apply(lambda emb: get_numeric_embedding(str(emb)))
    cols_name = ['e' + str(i) for i in range(1, EMB_SIZE + 1)]
    df[cols_name] = pd.DataFrame(df.embedding.values.tolist(), index=df.index)
    df = df.drop(["embedding"], axis=1)
    save_path = cf.DATA_VEC + "/flat/" + file_name
    os.remove(save_path) if os.path.exists(save_path) else None
    pathlib.Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(save_path, index=False)
    print("Saved flat embedding to {}.".format(save_path))

