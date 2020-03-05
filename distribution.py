import pandas as pd
from collections import Counter

mDataTypes = ["java-small","java-med","java-large"]
mDataCats = ["test","validation","training"]

def saveDistribution(labels, fname):
    labels_dict = dict(Counter(labels))
    print("# Total Labels = ", sum(labels_dict.values()))
    print("# Unique Labels = ", len(labels_dict.keys()))
    tdf = pd.DataFrame(labels_dict.items(), columns=['Label', 'Frequency'])
    tdf = tdf.sort_values(['Frequency'], ascending=[False]).reset_index(drop=True)
    tdf.to_csv("data/distribution/" + fname, index=None)

for jt in mDataTypes:
    for jc in mDataCats:
        fname = jt + "-" + jc + ".csv"
        print(fname + ":")
        mpath = "data/filter/" + fname 
        mdf = pd.read_csv(mpath, sep=",", names=["path","method","size"])
        saveDistribution(list(mdf.method), fname)
        print("\n")

