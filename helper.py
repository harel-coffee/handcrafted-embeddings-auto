import config as cf
from sklearn.datasets import dump_svmlight_file
import os, pathlib

# Save Log Message
def save_log_msg(msg):
    print(msg)
    with open(cf.LOG_PATH, "a") as log_file:
        log_file.write(msg + "\n")
