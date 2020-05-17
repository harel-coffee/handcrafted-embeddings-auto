import pandas as pd
import os, pathlib, shutil
import config as cf
SAMPLE_LIMIT = 1000

train_path = "../data/handcrafted/top11/Methods/java-large/multi/count/training.csv"
df_train = pd.read_csv(train_path)
df_train = df_train.sample(frac=1, random_state=cf.MANUAL_SEED).reset_index(drop=True)
df_train = df_train.groupby('method').head(SAMPLE_LIMIT)

train_path = df_train["path"].tolist()
for src_path in train_path:
    dst_path = src_path.replace("/top11/Methods/", "/top11/Reduce/")
    pathlib.Path(os.path.dirname(dst_path)).mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_path, dst_path)

