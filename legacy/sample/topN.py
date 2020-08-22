import pandas as pd
import numpy as np
import os, pathlib, shutil, random
import config as cf
random.seed(cf.MANUAL_SEED)
np.random.seed(cf.MANUAL_SEED)

DATA_TYPE = ["java-large"]
DATA_CATEGORY = ["training", "validation", "test"]

def handle_space_comma(p1, p2):
    if not os.path.exists(p1):
        p1 = p1.replace("_space_", " ")
        p1 = p1.replace("_comma_", ",")
    if os.path.exists(p1):
        p2 = p2.replace(" ", "_r_space_r_")
        p2 = p2.replace(",", "_r_comma_r_")
    else:
        return "", ""
    return p1, p2

def copy_all_sample(m_paths, method):
    for p1 in m_paths:
        p2 = p1.replace("/transforms/Methods/", "/handcrafted/top{}/Methods/".format(len(cf.TOP_LABELS)))
        fp1, fp2 = handle_space_comma(p1, p2)
        if len(fp1)==0 or len(fp2)==0:
            print("{} does not exist!".format(p1))
        else:
            pathlib.Path(os.path.dirname(fp2)).mkdir(parents=True, exist_ok=True)
            shutil.copy2(fp1, fp2)

def save_all_sample(m_paths, f_name):
    f_name = "../data/top{}/".format(len(cf.TOP_LABELS)) + f_name + ".txt"
    pathlib.Path(os.path.dirname(f_name)).mkdir(parents=True, exist_ok=True)
    with open(f_name, 'w') as f:
        for t_path in m_paths:
            f.write("%s\n" % t_path)
    print("Done: ", f_name, len(set(m_paths)))

for jt in DATA_TYPE:
    for jc in DATA_CATEGORY:
        t_path = "../data/filter/" + jt + "-" + jc + ".csv"
        t_df = pd.read_csv(t_path, sep=",", names=["path", "method", "size"])
        for method in cf.TOP_LABELS:
            m_df = t_df.loc[t_df['method'] == method]
            f_name = jt + "/" + jc + "/" + method
            #save_all_sample(list(m_df.path), f_name)
            copy_all_sample(list(m_df.path), method)
        print("Done: ", t_path)
