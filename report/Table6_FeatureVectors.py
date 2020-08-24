import re

BGCH, BGTK, HCBCX, C2V = [], [], [], []


def get_row(r):
    r = ["{:.2f}".format(float(x)) if re.match('[0-9]+.[0-9]+', x) else x for x in r]
    r = "& \\" + r[1] + " & " + " & ".join(r[3:])
    r = r + " \\\\ \\cline{2-5}"
    return r


with open("result.csv") as fr:
    for line in fr:
        line = line.strip()
        if len(line) < 1: continue
        vals = line.split(",")
        if "BGCH" == vals[1]:
            BGCH.append(vals)
        elif "BGTK" == vals[1]:
            BGTK.append(vals)
        elif "HCBCX" == vals[1]:
            HCBCX.append(vals)
        elif "code2vec" == vals[1]:
            C2V.append(vals)

for chr, tkr, hcr, cvr in zip(BGCH, BGTK, HCBCX, C2V):
    print("\\multirow{4}{*}{" + chr[0] + "}")
    print(get_row(chr), '\n', get_row(tkr), '\n', get_row(hcr), '\n', get_row(cvr))
    print("\\hline")
    print()
