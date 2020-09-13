import os
import shutil
from subprocess import check_output

import numpy as np

import config as cf
import helper as hp

# Custom params
cg_range = list(np.logspace(start=-3, stop=3, num=7, base=10))

# For each feature embeddings of method
for hfe_type in cf.HFE_TYPES:
    for emb_type in cf.EMB_TYPES:
        light_root = cf.DATA_VEC + "/light/{}/{}".format(hfe_type, emb_type)
        for method in cf.TOP_LABELS:
            light_path = light_root + "/" + method

            # Log file
            cf.LOG_PATH = light_path + "/train.log"
            open(cf.LOG_PATH, 'w').close()
            hp.save_log_msg("\nStart: {}-{}-{}.\n".format(hfe_type, emb_type, method))

            # Data files
            train_dat = light_path + "/train.dat"
            val_dat = light_path + "/validation.dat"
            test_dat = light_path + "/test.dat"

            # Result files
            train_model = light_path + "/train.mod"
            best_model = light_path + "/best.mod"
            val_result = light_path + "/validation.out"
            test_result = light_path + "/test.out"

            # Tuning hyper-params
            hp.save_log_msg("\nTraining started...")
            best_f1 = 0.0
            for c_range in cg_range:  # cf.C_RANGE
                for g_range in cg_range:  # cf.GAMMA_RANGE
                    hp.save_log_msg("\nChecking for c={} and g={}:".format(c_range, g_range))
                    c_str, g_str = str("%f" % c_range), str("%f" % g_range)
                    train_out = check_output([cf.SVM_LIGHT + "svm_learn", "-z", "c", "-t", "2",
                                              "-c", c_str, "-g", g_str, train_dat, train_model])
                    val_out = check_output([cf.SVM_LIGHT + "svm_classify", val_dat, train_model, val_result])
                    val_out = val_out.decode(encoding="utf-8")
                    val_acc, val_pre, val_rec, val_f1 = hp.parse_svm_light_output(val_out)
                    hp.save_log_msg("[Val] Accuracy={}, Precision={}, Recall={}, F1-score = {}".
                                    format(val_acc, val_pre, val_rec, val_f1))
                    if val_f1 > best_f1:
                        best_f1 = val_f1
                        os.remove(best_model) if os.path.exists(best_model) else None
                        shutil.copy2(train_model, best_model)
                        hp.save_log_msg("\nUpdated best f1 score = {}%".format(best_f1))
            hp.save_log_msg("Training completed.")

            # Evaluate best model
            hp.save_log_msg("\nEvaluating best model...")
            test_out = check_output([cf.SVM_LIGHT + "svm_classify", test_dat, best_model, test_result])
            test_out = test_out.decode(encoding="utf-8")
            test_acc, test_pre, test_rec, test_f1 = hp.parse_svm_light_output(test_out)
            hp.save_log_msg("\n[Test] Accuracy={}, Precision={}, Recall={}, F1-score = {}%\n".
                            format(test_acc, test_pre, test_rec, test_f1))

            # Save result to common file
            with open(light_root + "/result.csv", 'a') as f_result:
                f_result.write("{},{},{},{},{},{}\n".format(method, emb_type, test_acc, test_pre, test_rec, test_f1))

            hp.save_log_msg("\nDone: {}-{}-{}.\n".format(hfe_type, emb_type, method))
