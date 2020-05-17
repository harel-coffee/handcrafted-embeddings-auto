import pandas as pd
import os, pathlib
from sklearn import preprocessing
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import config as cf

mRS =  42 #int(datetime.now().timestamp())
types = ["flat", "norm"]
mcols = ['clf', 'accuracy', 'precision', 'recall', 'f1-score', 'type-1', 'type-2']

def get_dataset(filename):
    df = pd.read_csv(filename, header=None, index_col=None)
    training_data = df.drop([df.columns[0], df.columns[1]], axis=1) #drop path,method
    correct_labels = training_data.iloc[:,-1]
    feature_vectors = training_data.drop(training_data.columns[-1], axis=1) #drop label
    scaler = preprocessing.StandardScaler().fit(feature_vectors)
    scaled_features = scaler.transform(feature_vectors)
    X_all, y_all = scaled_features, correct_labels
    return X_all, y_all

def get_model(X_train, y_train):
    clf = SVC(kernel='rbf', C=1000, gamma=0.0001) #pre-tuning
    clf.fit(X_train, y_train)
    return clf

def evaluate_model(tclf, X_all, y_all):
    rskf = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=mRS)
    rlist = []
    for train_index, test_index in rskf.split(X_all, y_all):
        clist = []
        X_train, X_test = X_all[train_index], X_all[test_index]
        y_train, y_test = y_all[train_index], y_all[test_index]
        clf = get_model(X_train, y_train)
        y_pred = clf.predict(X_test)
        clist.append(tclf)
        ascore = accuracy_score(y_test, y_pred)
        # print("accuracy_score: ", ascore)
        clist.append(ascore)
        # print("classification_report:\n", classification_report(y_test, y_pred))
        creport = classification_report(y_test, y_pred, output_dict=True)
        clist.append(creport['weighted avg']['precision'])
        clist.append(creport['weighted avg']['recall'])
        clist.append(creport['weighted avg']['f1-score'])
        cmatrix = confusion_matrix(y_test, y_pred)
        # print("confusion_matrix:\n", cmatrix)
        clist.append(cmatrix[0][1])
        clist.append(cmatrix[1][0])
        rlist.append(clist)
    return rlist

mdf = pd.DataFrame(columns=mcols)
for mtarget in cf.TOP_LABELS:
    for ty in types:
        tclf = mtarget + "_" + ty
        mpath = "../../data/code2vec/" + cf.DATASET + "/" + ty + "/" + mtarget + ".csv"
        X_train, y_train = get_dataset(mpath)
        rlist = evaluate_model(tclf, X_train, y_train)
        tdf = pd.DataFrame(rlist, columns=mcols)
        mdf = mdf.append(tdf, ignore_index=True)
        print("Done : " + mpath)
mpath = "../../result/code2vec/score/" + cf.DATASET + "/" + "rskf_svm.csv"
pathlib.Path(os.path.dirname(mpath)).mkdir(parents=True, exist_ok=True)
mdf.to_csv(mpath, index=None)
print(mdf.head())
