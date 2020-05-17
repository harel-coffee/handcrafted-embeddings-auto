import config as cf
import helper as hp
import numpy as np
import os, shutil
from subprocess import check_output

# Set Params
cg_range = list(np.logspace(start=-3, stop=3, num=7, base=10))

# For each embedding
for emb_type in cf.HFE_TYPES:
    print("For emb_type = {}:".format(emb_type))
    light_root = cf.DATA_VEC.format("handcrafted") + "/light/{}".format(emb_type)

    # For each method
    for method in cf.TOP_LABELS:
        print("\nFor method = {}:".format(method))
        light_path = light_root + "/" + method

        # Data files
        train_dat = light_path + "/train.dat"
        val_dat   = light_path + "/val.dat"
        test_dat  = light_path + "/test.dat"

        # Log file
        cf.LOG_PATH = light_path + "/train.log"
        open(cf.LOG_PATH, 'w').close()

        # Result files
        train_model = light_path + "/train.mod"
        best_model  = light_path + "/best.mod"
        val_result  = light_path + "/val.out"
        test_result = light_path + "/test.out"

        # Tuning hyper-params
        hp.save_log_msg("\nTraining started...")
        best_f1s = 0.0
        for c_range in cg_range:
            for g_range in cg_range:
                hp.save_log_msg("\nChecking for c={} and g={}:".format(c_range, g_range))
                c_str, g_str = str("%f"%c_range), str("%f"%g_range)
                train_out = check_output([cf.SVM_LIGHT+"svm_learn", "-z" , "c", "-t", "2", "-c", c_str, "-g", g_str, train_dat, train_model])
                val_out = check_output([cf.SVM_LIGHT+"svm_classify", val_dat, train_model, val_result])
                val_out = val_out.decode(encoding="utf-8")
                val_acc, val_pre, val_rec, val_f1s = hp.parse_svm_light_output(val_out)
                hp.save_log_msg("[Val] Accuracy={}, Precision={}, Recall={}, F1-score = {}".format(val_acc, val_pre, val_rec, val_f1s))
                if val_f1s > best_f1s:
                    best_f1s = val_f1s
                    os.remove(best_model) if os.path.exists(best_model) else None
                    shutil.copy2(train_model, best_model)
                    hp.save_log_msg("\nUpdated best f1 score = {}%".format(best_f1s))
        hp.save_log_msg("Training completed.")

        # Evaluate best model
        hp.save_log_msg("\nEvaluating best model...")
        test_out = check_output([cf.SVM_LIGHT+"svm_classify", test_dat, best_model, test_result])
        test_out = test_out.decode(encoding="utf-8")
        acc, pre, rec, f1s = hp.parse_svm_light_output(test_out)
        hp.save_log_msg("\n[Test] Accuracy={}, Precision={}, Recall={}, F1-score = {}%\n".format(acc, pre, rec, f1s))

        # Save result to common file
        with open(light_root + "/result.csv", 'a') as f_result:
            f_result.write("{},{},{},{},{},{}\n".format(method, "hfe_" + emb_type, acc, pre, rec, f1s))

        hp.save_log_msg("Evaluation completed.")
