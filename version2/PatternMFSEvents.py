import pyfpgrowth
import operator

def mfs(T, K):
    T_ = []
    for t in T:
        tr = []
        c = []
        for el in t:
            count_el = c.count(el[0])
            tr.append((el[0],count_el + 1))
            c.append(el[0])
        T_.append(tr)
    import time
    patterns = pyfpgrowth.find_frequent_patterns(T_,500)
    patterns = sorted(list(patterns.keys()), key=len)
    frequent = [patterns.pop()]
    while len(patterns) > 0:
        candidate = patterns.pop()
        super = True
        for f in frequent:
            if all(elem in f for elem in candidate):
                super = False
                break
        if super:
            frequent.append(candidate)
    new_frequent = []
    for f in frequent:
        dict_f = {f_el[0]: (f_el[1], []) for f_el in f}
        for tr in T:
            cand = []
            dict_f = {f_el[0]: (f_el[1], []) for f_el in f}
            for t in tr:
                if t[0] in dict_f.keys():
                    dict_f[t[0]][1].append(t)
            for key in dict_f.keys():
                if dict_f[key][0] != len(dict_f[key][1]):
                        break
                else:
                    cand.extend(dict_f[key][1])
            if len(cand) == len(f):
                new_frequent.append(sorted(cand,key=operator.itemgetter(1)))
    frequent = new_frequent
    return frequent