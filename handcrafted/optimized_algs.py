import pandas as pd
import numpy as np
from datetime import datetime
import os, pathlib, shutil
from sklearn import preprocessing
from sklearn import model_selection
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import sys, warnings
warnings.filterwarnings("ignore")
if not sys.warnoptions:
    warnings.simplefilter("ignore")

# params
mRS =  42 #int(datetime.now().timestamp())
mEPOCHS = 3000 #max_iter to converge
mPATIENCE = 10 #n_iter_no_change for early stopping
mTOL = 0.001 #Tolerance for stopping criterion
mVF = 0.1 #validation_fraction for early stopping
mSKF = 10 #n_splits of StratifiedKFold for GridSearchCV
mRSKF = [5, 3] #(n_splits,n_repeats) of RepeatedStratifiedKFold for Train/Test split

mClfs = ["NB", "LR", "SVM", "GBDT", "PT"]
mDataTypes = ["java-large"]
mDataCats = ["training"]
mTargets = ["equals", "setUp", "toString"]
mFeatureTypes = ["norm", "binary"]

mDebug = False

# methods
def getDataset(filename):
    df = pd.read_csv(filename, header=None, index_col=None)
    training_data = df.drop([df.columns[0], df.columns[1]], axis=1) #drop path,method
    correct_labels = training_data.iloc[:,-1]
    feature_vectors = training_data.drop(training_data.columns[-1], axis=1) #drop label
    scaler = preprocessing.StandardScaler().fit(feature_vectors)
    scaled_features = scaler.transform(feature_vectors)
    X_all, y_all = scaled_features, correct_labels
    return X_all, y_all

def getBestNB(nbType=None):
    clf, param_dict = None, None
    if nbType == "binary":
        alpha_range = np.linspace(start=0.1, stop=1.0, num=10)
        param_dict = dict(alpha=alpha_range)
        clf = BernoulliNB()
    else:
        smoothing_range = np.logspace(start=-9, stop=1, num=11, base=10)
        param_dict = dict(var_smoothing=smoothing_range)
        clf = GaussianNB()
return clf, param_dict

def getBestLR():
    C_range = np.logspace(start=-5, stop=5, num=11, base=10)
    param_dict1 = dict(C=C_range, solver=['liblinear'], penalty=['l1', 'l2'])
    param_dict2 = dict(C=C_range, solver=['lbfgs'], penalty=['l2'])
    param_dict = [param_dict1, param_dict2]
    clf = LogisticRegression(max_iter=mEPOCHS, tol=mTOL, n_jobs=-1, random_state=mRS)
    return clf, param_dict

def getBestSVM():
    C_range = np.logspace(start=-5, stop=5, num=11, base=10)
    gamma_range = np.logspace(start=-5, stop=3, num=9, base=10)
    param_dict1 = dict(C=C_range, kernel=['linear'])
    param_dict2 = dict(C=C_range, gamma=gamma_range, kernel=['rbf'])
    param_dict = [param_dict1, param_dict2]
    clf = SVC(max_iter=mEPOCHS, tol=mTOL, random_state=mRS)
    return clf, param_dict

def getBestGBDT():
    n_range = np.array([1, 5, 10, 25, 50, 75, 100])
    lr_range = np.array([0.001, 0.005, 0.01, 0.05, 0.1, 0.5])
    depth_range = np.array([3, 5, 7])
    param_dict = dict(n_estimators=n_range, learning_rate=lr_range, max_depth=depth_range)
    clf = GradientBoostingClassifier(validation_fraction=mVF, n_iter_no_change=mPATIENCE, tol=mTOL, random_state=mRS)
    return clf, param_dict

def getBestPT():
    alpha_range = np.logspace(start=-5, stop=5, num=11, base=10)
    param_dict = dict(alpha=alpha_range, penalty=['l1', 'l2'])
    clf = Perceptron(max_iter=mEPOCHS, tol=mTOL, shuffle=True,
                     early_stopping=True, validation_fraction=mVF, n_iter_no_change=mPATIENCE,
                     n_jobs=-1, random_state=mRS)
    return clf, param_dict

def getGridModel(salg, sft):
    clf, param_dict = None, None
    if salg == "NB":
        clf, param_dict = getBestNB(sft)
    elif salg == "LR":
        clf, param_dict = getBestLR()
    elif salg == "SVM":
        clf, param_dict = getBestSVM()
    elif salg == "GBDT":
        clf, param_dict = getBestGBDT()
    elif salg == "PT":
        clf, param_dict = getBestPT()
    cv_skf = StratifiedKFold(n_splits=mSKF, shuffle=True, random_state=mRS)
    gclf = GridSearchCV(estimator=clf,
                        refit=True,
                        scoring='f1_weighted',
                        n_jobs=-1,
                        param_grid=param_dict,
                        cv=cv_skf)
return gclf

def evaluateModel(smodel, salg, sft, X_all, y_all):
    rskf = RepeatedStratifiedKFold(n_splits=mRSKF[0], n_repeats=mRSKF[1], random_state=mRS)
    rlist = []
    for train_index, test_index in rskf.split(X_all, y_all):
        clist = []
        X_train, X_test = X_all[train_index], X_all[test_index]
        y_train, y_test = y_all[train_index], y_all[test_index]
        clf = None
        clf = getGridModel(salg, sft)
        clf.fit(X_train, y_train)
        if mDebug == True:
            print("*" * 13)
            print(clf.best_params_)
            print(clf.best_estimator_)
            print("*" * 13)
            print("\n")
        y_pred = clf.predict(X_test)
        clist.append(smodel)
        clist.append(salg)
        ascore = accuracy_score(y_test, y_pred)
        #print("accuracy_score: ", ascore)
        clist.append(ascore)
        #print("classification_report:\n", classification_report(y_test, y_pred))
        creport = classification_report(y_test, y_pred, output_dict=True)
        clist.append(creport['weighted avg']['precision'])
        clist.append(creport['weighted avg']['recall'])
        clist.append(creport['weighted avg']['f1-score'])
        cmatrix = confusion_matrix(y_test, y_pred)
        #print("confusion_matrix:\n", cmatrix)
        clist.append(cmatrix[0][1])
        clist.append(cmatrix[1][0])
        rlist.append(clist)
    return rlist

def computeAvgResult(mroot):
    mpath = mroot + "_rskf.csv"
    mdf = pd.read_csv(mpath)
    adf = mdf.groupby(['methodClf']).mean().reset_index()
    for c in adf.columns[1:]:
        adf[c] = adf[c].apply(lambda x: '{:.3f}'.format(round(x, 3)))
    mpath = mroot + "_avg.csv"
    adf.to_csv(mpath, index=None)
    print("Done: ", mroot)

# main
for salg in mClfs:
    for jt in mDataTypes:
        for jc in mDataCats:
            mroot = "../result/handcrafted/score/" + jt + "/" + jc + "/" + salg
            print("Start: ", mroot)
            mcols = ['methodClf','algClf','accuracy','precision','recall','f1-score','type-1','type-2']
            mdf = pd.DataFrame(columns=mcols)
            for mtarget in mTargets:
                for sft in mFeatureTypes:
                    smodel = mtarget + "_" + sft
                    mpath = "../data/handcrafted/" + jt + "/" + jc + "/" + sft + "/" + mtarget + ".csv"
                    X_all, y_all = getDataset(mpath)
                    rlist = evaluateModel(smodel, salg, sft, X_all, y_all)
                    tdf = pd.DataFrame(rlist, columns=mcols)
                    mdf = mdf.append(tdf, ignore_index=True)
            mpath = mroot + "_rskf.csv"
            pathlib.Path(os.path.dirname(mpath)).mkdir(parents=True, exist_ok=True)
            mdf.to_csv(mpath, index=None)
            computeAvgResult(mroot)

