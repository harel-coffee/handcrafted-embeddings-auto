import pandas as pd
import os, pathlib, shutil
import config as cf
import common.grid_search as gs

# params
mClfs = ["NB", "LR", "SVM", "GBDT", "PT"]
mFeatureTypes = ["flat"]

# main
for salg in mClfs:
    mroot = "../../result/code2vec/score/" + cf.DATASET + "/" + salg
    print("Start: ", mroot)
    mcols = ['methodClf','algClf','accuracy','precision','recall','f1-score','type-1','type-2']
    mdf = pd.DataFrame(columns=mcols)
    for mtarget in cf.TOP_LABELS:
        print("Start: ", mtarget)
        for sft in mFeatureTypes:
            smodel = mtarget + "_" + sft
            mpath = "../../data/code2vec/" + cf.DATASET + "/" + sft + "/" + mtarget + ".csv"
            X_all, y_all = gs.get_dataset(mpath)
            rlist = gs.evaluate_model(smodel, salg, sft, X_all, y_all)
            tdf = pd.DataFrame(rlist, columns=mcols)
            mdf = mdf.append(tdf, ignore_index=True)
        print("Done: ", mtarget)
    mpath = mroot + "_skf.csv"
    pathlib.Path(os.path.dirname(mpath)).mkdir(parents=True, exist_ok=True)
    mdf.to_csv(mpath, index=None)
    gs.compute_avg_result(mroot)
