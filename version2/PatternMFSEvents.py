import pyfpgrowth
import operator

def mfs(T, K):
    T_ = []
    #creating all traces without timedelta, but as tuple (event,count) where count is the count of the event in the trace
    for t in T:
        tr = []
        c = []
        for el in t:
            count_el = c.count(el[0])
            tr.append((el[0],count_el + 1))
            c.append(el[0])
        T_.append(tr)
    #getting the frequent itemsets (fp-growth tree)
    patterns = pyfpgrowth.find_frequent_patterns(T_,500)
    #sort by length of frequent set (shortest first)
    patterns = sorted(list(patterns.keys()), key=len)
    #get longest frequent subtrace and add to list of all maximal frequent subtraces
    frequent = [patterns.pop()]
    while len(patterns) > 0:
        #check if the next candidate subtrace is contained as subtrace of another frequent subtrace that is longer and
        #because of that already in frequent
        candidate = patterns.pop()
        super = True
        for f in frequent:
            if all(elem in f for elem in candidate):
                super = False
                break
        if super:
            frequent.append(candidate)
    #translate back to tuples (event,timedelta)
    new_frequent = []
    for f in frequent:
        for tr in T:
            #cand creates the new version of the trace
            cand = []
            #collects the event tuples and contains the count for each event in f
            dict_f = {f_el[0]: (f_el[1], []) for f_el in f}
            for t in tr:
                if t[0] in dict_f.keys():
                    dict_f[t[0]][1].append(t)
            for key in dict_f.keys():
                #the noccurence of an event has to be the same in the whole trace then in the candidate trace
                #TODO: maybe better if it also can be larger and then get all versions of it (how exaclty solve that?) running time?
                if dict_f[key][0] != len(dict_f[key][1]):
                        break
                else:
                    cand.extend(dict_f[key][1])
            #recheck of the subtraces have the same length
            if len(cand) == len(f):
                new_frequent.append(sorted(cand,key=operator.itemgetter(1)))
    frequent = new_frequent
    return frequent