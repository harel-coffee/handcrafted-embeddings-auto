import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import os, sys, warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")
    os.environ["PYTHONWARNINGS"] = "ignore"
import config as cf

# params
mRS =  42 #int(datetime.now().timestamp())
mEPOCHS = 3000 #max_iter to converge
mPATIENCE = 10 #n_iter_no_change for early stopping
mTOL = 0.001 #Tolerance for stopping criterion
mVF = 0.1 #validation_fraction for early stopping
mSKF = [5,10] #Train/Test and GridSearch

mDebug = False

# methods
def get_dataset(filename):
    df = pd.read_csv(filename, header=None, index_col=None)
    training_data = df.drop([df.columns[0], df.columns[1]], axis=1) #drop path,mtarget
    correct_labels = training_data.iloc[:,-1]
    feature_vectors = training_data.drop(training_data.columns[-1], axis=1) #drop label
    scaler = preprocessing.StandardScaler().fit(feature_vectors)
    scaled_features = scaler.transform(feature_vectors)
    X_all, y_all = scaled_features, correct_labels
    return X_all, y_all

def get_best_NB(nbType=None):
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

def get_best_LR():
    C_range = np.logspace(start=-5, stop=5, num=11, base=10)
    param_dict1 = dict(C=C_range, solver=['liblinear'], penalty=['l1', 'l2'])
    param_dict2 = dict(C=C_range, solver=['lbfgs'], penalty=['l2'])
    param_dict = [param_dict1, param_dict2]
    clf = LogisticRegression(max_iter=mEPOCHS, tol=mTOL, n_jobs=-1, random_state=mRS)
    return clf, param_dict

def get_best_SVM():
    C_range = np.logspace(start=-5, stop=5, num=11, base=10)
    gamma_range = np.logspace(start=-5, stop=3, num=9, base=10)
    param_dict1 = dict(C=C_range, kernel=['linear'])
    param_dict2 = dict(C=C_range, gamma=gamma_range, kernel=['rbf'])
    param_dict = [param_dict1, param_dict2]
    clf = SVC(max_iter=mEPOCHS, tol=mTOL, random_state=mRS)
    return clf, param_dict

def get_best_GBDT():
    n_range = np.array([1, 5, 10, 25, 50, 75, 100])
    lr_range = np.array([0.001, 0.005, 0.01, 0.05, 0.1, 0.5])
    depth_range = np.array([3, 5, 7])
    param_dict = dict(n_estimators=n_range, learning_rate=lr_range, max_depth=depth_range)
    clf = GradientBoostingClassifier(validation_fraction=mVF, n_iter_no_change=mPATIENCE, tol=mTOL, random_state=mRS)
    return clf, param_dict

def get_best_PT():
    alpha_range = np.logspace(start=-5, stop=5, num=11, base=10)
    param_dict = dict(alpha=alpha_range, penalty=['l1', 'l2'])
    clf = Perceptron(max_iter=mEPOCHS, tol=mTOL, shuffle=True,
                     early_stopping=True, validation_fraction=mVF, n_iter_no_change=mPATIENCE,
                     n_jobs=-1, random_state=mRS)
    return clf, param_dict

def get_grid_model(salg, sft):
    clf, param_dict = None, None
    if salg == "NB":
        clf, param_dict = get_best_NB(sft)
    elif salg == "LR":
        clf, param_dict = get_best_LR()
    elif salg == "SVM":
        clf, param_dict = get_best_SVM()
    elif salg == "GBDT":
        clf, param_dict = get_best_GBDT()
    elif salg == "PT":
        clf, param_dict = get_best_PT()
    cv_skf = StratifiedKFold(n_splits=mSKF[1], shuffle=True, random_state=mRS)
    gclf = GridSearchCV(estimator=clf,
                        refit=True,
                        scoring='f1_weighted',
                        n_jobs=-1,
                        param_grid=param_dict,
                        cv=cv_skf)
    return gclf

def evaluate_model(smodel, salg, sft, X_all, y_all):
    skf = StratifiedKFold(n_splits=mSKF[0], random_state=mRS)
    rlist = []
    for train_index, test_index in skf.split(X_all, y_all):
        clist = []
        X_train, X_test = X_all[train_index], X_all[test_index]
        y_train, y_test = y_all[train_index], y_all[test_index]
        clf = None
        clf = get_grid_model(salg, sft)
        clf.fit(X_train, y_train)
        if mDebug == True:
            print(smodel, salg, sft, ":")
            print(clf.best_params_)
            print(clf.best_estimator_)
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

def compute_avg_result(mroot):
    mpath = mroot + "_skf.csv"
    mdf = pd.read_csv(mpath)
    adf = mdf.groupby(by=['methodClf'], sort=False).mean().reset_index()
    for c in adf.columns[1:]:
        adf[c] = adf[c].apply(lambda x: '{:.3f}'.format(round(x, 3)))
    mpath = mroot + "_avg.csv"
    adf.to_csv(mpath, index=None)
    print("Done: ", mroot)
