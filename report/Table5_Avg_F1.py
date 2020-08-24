import config as cf

avg_result = {}
for k in cf.TOP_LABELS:
    avg_result[k] = {}
n = len(cf.TOP_LABELS)

with open("result.csv") as fin:
    for line in fin:
        line = line.strip()
        if len(line) < 1: continue
        vals = line.split(",")
        f1s = [(float(f) * 1) for f in vals[2:]]
        avg_result[vals[0]][vals[1]] = f1s

vectors = ['BGCH', 'BGTK', 'HCB', 'HCN', 'HCBCX', 'HCNCX', 'code2vec']
for v in vectors:
    acc, pre, rec, f1s = 0.0, 0.0, 0.0, 0.0
    for m in avg_result.keys():
        r = avg_result[m][v]
        acc += r[0]
        pre += r[1]
        rec += r[2]
        f1s += r[3]
    acc, pre, rec, f1s = acc/n, pre/n, rec/n, f1s/n
    print("{} & {} & {} & {} & {}" .format(v, "%.2f" % acc, "%.2f" % pre, "%.2f" % rec, "%.2f" % f1s))
