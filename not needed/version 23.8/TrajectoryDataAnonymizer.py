import operator
def suppression(violating,frequent):
    sup = []
    X1 = []
    for v in violating + frequent:
        if isinstance(v[0], str):
            X1.append(v)
        else:
            for sub in v:
                X1.append(sub)
    X1 = list(set(X1))
    score_res,mvsEl,mfsEl = score(violating,frequent,X1)
    #while PG table is not empty do
    while len(score_res)>0:
    #4: select a pair w that has the highest Score to suppress;
        w = max(score_res.items(), key=operator.itemgetter(1))[0]
    #5: delete all MVS and MFS containing w from MVS -tree and MFS - tree;
        list_mvs =mvsEl[w]
        for l in list_mvs:
            violating.remove(l)
        list_mfs = mfsEl[w]
        for l in list_mfs:
            frequent.remove(l)
    #6: update the Score(p) if both w and p are contained in the same MVS or MFS;
        X1 = []
        for v in violating + frequent:
            if isinstance(v[0], str):
                X1.append(v)
            else:
                for sub in v:
                    X1.append(sub)
        X1 = list(set(X1))
        # 7: remove w from PG Table;
        score_res,mvsEl,mfsEl =score(violating,frequent,X1)
        #8: add w to Sup;
        sup.append(w)
    #9: end
    return sup

def score(violating, frequent, X1):
    priv = {v: 0 for v in X1}
    ut = {f: 0 for f in X1}
    #for each element in which violating/frequent subtraces it is containe
    #TODO could be better maybe
    mvsEle = {v: [] for v in X1}
    mfsEle = {f: [] for f in X1}
    for v in violating:
        if isinstance(v[0], str):
            priv[v] += 1
            mvsEle[v].append(v)
        else:
            for el in v:
                priv[el] += 1
                mvsEle[el].append(v)
    for f in frequent:
        if isinstance(f[0],str):
            ut[f] += 1
            mfsEle[f].append(f)
        else:
            for el in f:
                ut[el] += 1
                mfsEle[el].append(f)
    score = {el: 0 for el in X1}
    for el in X1:
        score[el] = priv[el]/(ut[el] + 1)
        if score[el] == 0:
            del score[el]
    return score,mvsEle,mfsEle

def suppressT(logsimple, sup):
    for key in logsimple.keys():
        list_trace = logsimple[key]['trace']
        for sub in list_trace:
            if sub in sup:
                list_trace.remove(sub)
        logsimple[key]['trace'] = list_trace
    return logsimple
