import re

HCB, HCN, HCBCX, HCNCX = [], [], [], []


def get_row(r):
    r = ["{:.2f}".format(float(x)) if re.match('[0-9]+.[0-9]+', x) else x for x in r]
    r = "& \\" + r[1] + " & " + " & ".join(r[3:])
    r = r + " \\\\ \\cline{2-5}"
    return r


with open("result.csv") as f_result:
    for line in f_result:
        line = line.strip()
        if len(line) < 1: continue
        vals = line.split(",")
        if "HCB" == vals[1]:
            HCB.append(vals)
        elif "HCN" == vals[1]:
            HCN.append(vals)
        elif "HCBCX" == vals[1]:
            HCBCX.append(vals)
        elif "HCNCX" == vals[1]:
            HCNCX.append(vals)

for br, nr, bxr, nxr in zip(HCB, HCN, HCBCX, HCNCX):
    print("\\multirow{4}{*}{" + br[0] + "}")
    print(get_row(br), '\n', get_row(nr), '\n', get_row(bxr), '\n', get_row(nxr))
    print("\\hline")
    print()
