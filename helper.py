import config as cf
from sklearn.datasets import dump_svmlight_file
import os, pathlib

# Save Log Message
def save_log_msg(msg):
    print(msg)
    with open(cf.LOG_PATH, "a") as log_file:
        log_file.write(msg + "\n")

# Save Light Format
def save_svm_light_format(df, light_file):
    light_file = light_file.replace(".csv", ".dat")
    vector_X, target_y = df.iloc[:, 2:-1], df.iloc[:, -1]
    pathlib.Path(os.path.dirname(light_file)).mkdir(parents=True, exist_ok=True)
    with open(light_file, "wb") as f_light:
        dump_svmlight_file(X=vector_X, y=target_y, f=f_light, zero_based=False, multilabel=False)

# Parse output of svm
def parse_svm_light_output(output):
    acc, pre, rec, f1s = 0.0, 0.0, 0.0, 0.0
    lines = output.split('\n')
    for line in lines:
        if "Accuracy" in line:
            acc = float((line.split('%')[0]).split()[-1])
        elif "Precision" in line:
            pre = float((line.split('%')[0]).split()[-1])
            rec = float((line.split('%')[1]).replace('/',''))
            f1s =  round(2 * (pre * rec) / (pre + rec), 2)
    return acc, pre, rec, f1s
