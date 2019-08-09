import pyfpgrowth


def mfs(T, K):
    T_ = []
    for t in T:
        tr = []
        for el in t:
            tr.append(el[0])
        T_.append(tr)
    print(T_)
    patterns = pyfpgrowth.find_frequent_patterns(T_,K)
    print(len(patterns))
    patterns = sorted(list(patterns.keys()), key=len)
    print(len(patterns))
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
    print(len(frequent))
    for f in frequent:
        for t in tr:
            f_new = [t_el for t_el in t if t in f]
            from operator import itemgetter
            test = map(itemgetter(0),f_new)
            print(f_new)
            print(test)
            print("f", f)


    return frequent