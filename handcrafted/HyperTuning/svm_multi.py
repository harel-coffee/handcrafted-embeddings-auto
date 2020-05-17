import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import _pickle as pickle
import os, sys, warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")
    os.environ["PYTHONWARNINGS"] = "ignore"
mRS =  42

def save_log_msg(msg):
    print(msg)
    with open(mLogFile, "a") as myfile:
        myfile.write(msg + "\n")

mRootPath = "../../data/handcrafted/java-large/top11/multi"
mFeatureTypes = ["norm", "binary"]

for ft in mFeatureTypes:
    save_log_msg("\nStart for {}...".format(ft))
    mModelPath = "svm-" + ft + ".pk"
    mLogFile = "svm-" + ft + ".log"
    open(mLogFile, 'w').close()
    le = preprocessing.LabelEncoder()

    save_log_msg("\nLoading dataset...")
    df_train = pd.read_csv(mRootPath + "/" + ft + "/" + "training.csv")
    df_val = pd.read_csv(mRootPath + "/" + ft + "/" + "validation.csv")
    df_test = pd.read_csv(mRootPath + "/" + ft + "/" + "test.csv")

    le.fit(df_train["Method"].tolist())
    df_train["Label"] = le.transform(df_train["Method"].tolist())
    df_val["Label"] = le.transform(df_val["Method"].tolist())
    df_test["Label"] = le.transform(df_test["Method"].tolist())

    X_train, y_train = df_train.drop(["Path","Method","Label"], axis=1), df_train["Label"].tolist()
    X_val, y_val = df_val.drop(["Path","Method","Label"], axis=1), df_val["Label"].tolist()
    X_test, y_test = df_test.drop(["Path","Method","Label"], axis=1), df_test["Label"].tolist()
    save_log_msg("Loaded dataset...")

    save_log_msg("\nTraining svm...")
    clf_best_f1, clf_best_params = -1, None
    C_range = list(np.logspace(start=-4, stop=4, num=9, base=10))
    gamma_range = ['auto','scale'] + C_range
    save_log_msg("Shuffling train dataset...")
    X_train, y_train = shuffle(X_train, y_train, random_state=mRS)
    save_log_msg("Shuffled train dataset...")

    for gamma_tune in gamma_range:
        for C_tune in C_range:
            clf = SVC(C=C_tune, gamma=gamma_tune, cache_size=10240, kernel='rbf', random_state=mRS)
            clf.fit(X_train, y_train)
            y_pred = clf.predict(X_val)
            creport = classification_report(y_val, y_pred, output_dict=True)
            f1_val = creport['weighted avg']['f1-score']
            if f1_val > clf_best_f1:
                clf_best_f1 = f1_val
                clf_best_params = clf.get_params()
                save_log_msg("*" * 39)
                save_log_msg("Best F1-Score: {}".format(clf_best_f1))
                save_log_msg("Best Params: {}".format(clf_best_params))
                with open(mModelPath, 'wb') as fmod:
                    pickle.dump(clf, fmod)
                save_log_msg("Saved updated model for C={} and gamma={}".format(C_tune, gamma_tune))
    save_log_msg("Training done...")

    save_log_msg("\nLoading best svm...")
    clf = None
    with open(mModelPath, 'rb') as fmod:
        clf = pickle.load(fmod)
    save_log_msg("Loaded svm: \n {}".format(clf))

    save_log_msg("\nEvaluating test dataset...")
    y_pred = clf.predict(X_test)
    y_pred = le.inverse_transform(y_pred)
    y_true = le.inverse_transform(y_test)
    ascore = accuracy_score(y_true, y_pred)
    save_log_msg("accuracy_score:{}\n".format(ascore))
    creport = classification_report(y_true, y_pred, output_dict=True)
    save_log_msg("classification_report:\n{}\n".format(classification_report(y_true, y_pred)))
    cmatrix = confusion_matrix(y_true, y_pred)
    save_log_msg("confusion_matrix:\n{}\n".format(cmatrix))
    save_log_msg("Evaluation done...")

