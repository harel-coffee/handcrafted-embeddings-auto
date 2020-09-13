import numpy as np

ROOT_PATH = "/scratch/rabin/deployment/root-hc/GitHub/"
DATASET = "top10/deduplication/java-large"
SVM_LIGHT = ROOT_PATH + "tool/svm_light/"

# Top 10 methods
TOP_LABELS = ["equals", "main", "setUp", "onCreate", "toString", "run", "hashCode", "init", "execute", "get"]
LABELS2INDEX = {m: i for i, m in enumerate(TOP_LABELS)}
INDEX2LABELS = {i: m for i, m in enumerate(TOP_LABELS)}

CURRENT_VEC = "handcrafted"
PARTITIONS = ['train', 'validation', 'test']
HFE_TYPES = ["HC33", "HC33X"]
EMB_TYPES = ["binary", "norm", "count"]

DATA_PATH = ROOT_PATH + "data/"
DATA_VEC = DATA_PATH + "{}/".format(CURRENT_VEC) + DATASET

# Parameters
MANUAL_SEED = 42
C_RANGE = list(np.logspace(start=-5, stop=5, num=11, base=10))
GAMMA_RANGE = ['auto', 'scale'] + C_RANGE
CACHE_SIZE = 10240
KERNEL_TYPE = 'rbf'

# Model Logs
RESULT_PATH = ROOT_PATH + "result/"
LOG_PATH = RESULT_PATH + "{}.log"

# Plots
TOP_COLORS = ['red', 'green', 'blue', 'black', 'grey', 'pink', 'yellow', 'orange', 'silver', 'maroon']
