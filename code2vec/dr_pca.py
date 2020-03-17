import pandas as pd
import numpy as np
import os, pathlib, shutil
from datetime import datetime
import _pickle as pk
from sklearn import preprocessing
from sklearn.decomposition import PCA

# params
mRS =  42 #int(datetime.now().timestamp())

mDataTypes = ["java-large"]
mDataCats = ["training"]
mTargets = ["equals", "setUp", "toString"]
mFeatureTypes = ["flat"]

# methods
def decompositionPCA(X_pca):
    pca = PCA(n_components=min(len(X_pca), len(X_pca[0])), svd_solver='randomized', random_state=mRS)
    X_pca = pca.fit_transform(X_pca)
    return X_pca

def getDataset(filename):
    df = pd.read_csv(filename, header=None, index_col=None)
    training_data = df.drop([df.columns[0], df.columns[1]], axis=1) #drop path,method
    correct_labels = training_data.iloc[:,-1]
    feature_vectors = training_data.drop(training_data.columns[-1], axis=1) #drop label
    scaler = preprocessing.StandardScaler().fit(feature_vectors)
    scaled_features = scaler.transform(feature_vectors)
    X_all, y_all = scaled_features, correct_labels
    X_all = decompositionPCA(X_all)
    return X_all, y_all

# main
for jt in mDataTypes:
    for jc in mDataCats:
        for mtarget in mTargets:
            for sft in mFeatureTypes:
                mpath = "../data/code2vec/" + jt + "/" + jc + "/" + sft + "/" + mtarget + ".csv"
                print("Start: ", mpath)
                X_all, y_all = getDataset(mpath)
                dict_xy = {"Xpk":X_all, "ypk":y_all}
                mpath = "../data/code2vec/" + jt + "/" + jc + "/" + "pca" + "/" + mtarget + ".pk"
                pathlib.Path(os.path.dirname(mpath)).mkdir(parents=True, exist_ok=True)
                with open(mpath, 'wb') as xy_file:
                    pk.dump(dict_xy, xy_file)
                print("Done: ", mpath)
