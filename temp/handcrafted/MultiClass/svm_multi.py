import pandas as pd
import numpy as np
import os, pathlib
from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import _pickle as pk
import sys, warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")
    os.environ["PYTHONWARNINGS"] = "ignore"
import config as cf
import helper as hp

# Set Params
EMB_TYPE = "handcrafted"
FEATURE_TYPE = ["norm", "binary"]

for ft in FEATURE_TYPE:
    cf.auto_update_types(EMB_TYPE, ft)

    # Create Log File
    pathlib.Path(cf.LOG_PATH).parent.mkdir(parents=True, exist_ok=True)
    open(cf.LOG_PATH, 'w').close()
    hp.save_log_msg("Logging at {}...".format(cf.LOG_PATH))

    # Loading Dataset
    hp.save_log_msg("\nLoading dataset...")
    df_train = pd.read_csv(cf.DATA_VEC + "/multi/{}/train.csv".format(ft))
    df_val   = pd.read_csv(cf.DATA_VEC + "/multi/{}/val.csv".format(ft))
    df_test  = pd.read_csv(cf.DATA_VEC + "/multi/{}/test.csv".format(ft))
    hp.save_log_msg("#Train={}, #Dev={}, #Test={}".format(len(df_train), len(df_val), len(df_test)))
    if cf.DEBUG:
        dfs = [df_train, df_val, df_test]
        for i, df_cur in enumerate(dfs):
            df_cur = df_cur.sample(frac=1, random_state=cf.MANUAL_SEED).reset_index(drop=True)
            dfs[i] = df_cur.groupby('method').head(cf.SAMPLE_SIZE)
        df_train, df_val, df_test = dfs[0], dfs[1], dfs[2]
        hp.save_log_msg("#Train={}, #Dev={}, #Test={}".format(len(df_train), len(df_val), len(df_test)))

    # Encode Labels
    le = preprocessing.LabelEncoder()
    if cf.LABEL_ENCODER:
        le.fit(df_train["method"].tolist())
        df_train["label"] = le.transform(df_train["method"].tolist())
        df_val["label"] = le.transform(df_val["method"].tolist())
        df_test["label"] = le.transform(df_test["method"].tolist())
    else:
        df_train["label"] = df_train["method"].apply(lambda x: cf.LABELS2INDEX[x])
        df_val["label"] = df_val["method"].apply(lambda x: cf.LABELS2INDEX[x])
        df_test["label"] = df_test["method"].apply(lambda x: cf.LABELS2INDEX[x])

    X_train, y_train = df_train.drop(["path","method","label"], axis=1), df_train["label"].tolist()
    X_val, y_val = df_val.drop(["path","method","label"], axis=1), df_val["label"].tolist()
    X_test, y_test = df_test.drop(["path","method","label"], axis=1), df_test["label"].tolist()
    hp.save_log_msg("Loaded dataset.")

    hp.save_log_msg("\nShuffling train dataset...")
    X_train, y_train = shuffle(X_train, y_train)
    hp.save_log_msg("Shuffled train dataset.")

    hp.save_log_msg("\nTraining {}...".format(cf.CLF_NAME))
    clf, clf_best_f1, clf_best_params = None, -1, None
    for gamma_tune in cf.GAMMA_RANGE:
        for C_tune in cf.C_RANGE:
            clf = SVC(C=C_tune, gamma=gamma_tune, kernel=cf.KERNEL_TYPE,
                      cache_size=cf.CACHE_SIZE, random_state=cf.MANUAL_SEED)
            clf.fit(X_train, y_train)
            y_pred = clf.predict(X_val)
            clf_report = classification_report(y_val, y_pred, output_dict=True)
            f1_val = clf_report['weighted avg']['f1-score']
            hp.save_log_msg("Checking for C={} and gamma={}: {}".format(C_tune, gamma_tune, f1_val))
            if f1_val > clf_best_f1:
                clf_best_f1 = f1_val
                clf_best_params = clf.get_params()
                hp.save_log_msg("Best F1-Score: {}".format(clf_best_f1))
                hp.save_log_msg("Best Params: {}".format(clf_best_params))
                with open(cf.MODEL_PATH, 'wb') as fmod:
                    pk.dump(clf, fmod)
                hp.save_log_msg("Saved updated model for C={} and gamma={}.".format(C_tune, gamma_tune))
    hp.save_log_msg("Training completed.")

    hp.save_log_msg("\nLoading best model from {}...".format(cf.MODEL_PATH))
    with open(cf.MODEL_PATH, 'rb') as fmod:
        clf = pk.load(fmod)
    hp.save_log_msg("Loaded best model: \n {}".format(clf))

    hp.save_log_msg("\nEvaluating test dataset...")
    y_pred = clf.predict(X_test)
    if cf.LABEL_ENCODER:
        y_pred = le.inverse_transform(y_pred)
        y_test = le.inverse_transform(y_test)
    else:
        y_pred = [cf.INDEX2LABELS[y] for y in y_pred]
        y_test = [cf.INDEX2LABELS[y] for y in y_test]
    acc_score = accuracy_score(y_test, y_pred)
    hp.save_log_msg("Accuracy Score:{}\n".format(acc_score))
    clf_report = classification_report(y_test, y_pred, output_dict=False)
    hp.save_log_msg("Classification Report:\n{}\n".format(clf_report))
    conf_matrix = confusion_matrix(y_test, y_pred)
    hp.save_log_msg("Confusion Matrix:\n{}\n".format(conf_matrix))
    hp.save_log_msg("Evaluation completed.")

