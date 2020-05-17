import config as cf
import pandas as pd
from sklearn import preprocessing
import os, pathlib

ph_file = cf.DATA_VEC.format("handcrafted") + "/multi/{}/{}.csv"

# Split into train/val/test
hfe_file = ph_file.format("count", "OneHotPCA")
df = pd.read_csv(hfe_file, header=None)
for part1, part2 in zip(['training','validation','test'], ['train','val','test']):
    df_part   = df[df[0].str.contains(cf.DATASET+'/' + part1 + '/')]
    part_file = ph_file.format("count", part2)
    df_part.columns = ['path','method'] + ['e'+str(i) for i in range(1, int(df.shape[1])-1)]
    df_part.to_csv(part_file, index=False)

    #normalized
    df_norm = df_part.copy()
    for c in df_norm.columns[2:]:
        df_norm[[c]] = preprocessing.StandardScaler().fit_transform(df_norm[[c]])
    norm_file = ph_file.format("norm", part2)
    pathlib.Path(os.path.dirname(norm_file)).mkdir(parents=True, exist_ok=True)
    df_norm.to_csv(norm_file, index=False)

    #binary
    df_binary = df_part.copy()
    for c in df_binary.columns[2:]:
        df_binary[c] = df_binary[c].apply(lambda x: 1 if x>0 else 0)
    binary_file = ph_file.format("binary", part2)
    pathlib.Path(os.path.dirname(binary_file)).mkdir(parents=True, exist_ok=True)
    df_binary.to_csv(binary_file, index=False)

    print("Completed for {} file.".format(part1))
