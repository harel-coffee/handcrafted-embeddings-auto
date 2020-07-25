import numpy as np

ROOT_PATH = "/scratch/rabin/deployment/root-handcrafted/handcrafted-analysis/"
DATASET = "top11/Reduce/java-large"

PARTITIONS = ['train.csv', 'val.csv', 'test.csv']
TOP_LABELS = ["equals", "main", "setUp", "onCreate", "toString", "run", "hashCode", "init", "execute", "get", "close"]
LABELS2INDEX = {m: i for i, m in enumerate(TOP_LABELS)}
INDEX2LABELS = {i: m for i, m in enumerate(TOP_LABELS)}

MODE = "train"  # train/test
DEBUG = False
SAMPLE_SIZE = 10
LABEL_ENCODER = False

CLF_NAME = "svm"
CLF_TYPE = "binary"  # multi/binary

CLF_TYPES = ["multi", "binary"]
HFE_TYPES = ["mix", "binary", "norm"]

DATA_PATH = ROOT_PATH + "data/"
DATA_VEC = DATA_PATH + "{}/" + DATASET  # EMB_TYPE

# Parameters
MANUAL_SEED = 42
C_RANGE = list(np.logspace(start=-5, stop=5, num=11, base=10))
GAMMA_RANGE = ['auto', 'scale'] + C_RANGE
CACHE_SIZE = 10240
KERNEL_TYPE = 'rbf'
SVM_LIGHT = ROOT_PATH + "tool/svm_light/"

# Model Logs
RESULT_PATH = ROOT_PATH + "result/"
RESULT_KIND = RESULT_PATH + "{}/" + DATASET  # EMB_TYPE
LOG_PATH = RESULT_PATH + RESULT_KIND + ".log"
MODEL_PATH = RESULT_PATH + RESULT_KIND + ".model"


# Auto sets
def auto_update_types(emb_type, feature_type):
    global DATA_VEC, LOG_PATH, MODEL_PATH
    DATA_VEC = DATA_VEC.format(emb_type)
    LOG_PATH = LOG_PATH.format(emb_type, feature_type)
    MODEL_PATH = MODEL_PATH.format(emb_type, feature_type)


colors = ['red', 'green', 'blue', 'black', 'grey', 'pink', 'yellow', 'orange', 'silver', 'maroon']
