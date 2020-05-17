import pandas as pd
from collections import Counter

DATA_TYPE = ["java-small", "java-med", "java-large"]
DATA_CATEGORY = ["test", "validation", "training"]

def save_distribution(labels, f_name):
    labels_dict = dict(Counter(labels))
    print("# Total  Labels = ", sum(labels_dict.values()))
    print("# Unique Labels = ", len(labels_dict.keys()))
    tdf = pd.DataFrame(labels_dict.items(), columns=['Label', 'Frequency'])
    tdf = tdf.sort_values(['Frequency'], ascending=[False]).reset_index(drop=True)
    tdf.to_csv("../data/distribution/" + f_name, index=None)

for jt in DATA_TYPE:
    for jc in DATA_CATEGORY:
        f_name = jt + "-" + jc + ".csv"
        print(f_name + ":")
        mpath = "../data/filter/" + f_name
        mdf = pd.read_csv(mpath, sep=",", names=["path","method","size"])
        save_distribution(list(mdf.method), f_name)
        print("\n")
