import sys


def mfs(K, T):
    Tdict = {}
    singleElementDict = {}
    for t in T:
        if len(t) not in Tdict.keys():
            Tdict[len(t)] = [t]
        else:
            Tdict[len(t)].append(t)
    flat_list = [item for sublist in T for item in sublist]
    singleElements = sorted(list(set(flat_list)), key=lambda x: x[1])
    del flat_list
    countSingleElements = {tuple(el): 0 for el in singleElements}
    for v in singleElements:
        for t in T:
            if v in t:
                countSingleElements[tuple(v)] += 1
        if int(v[1]) not in singleElementDict.keys():
            singleElementDict[int(v[1])] = [v]
        else:
            singleElementDict[int(v[1])].append(v)
    del T
    #start by shortest
    keys = sorted(list(Tdict.keys()), reverse=True)
    #pruning all single elements not occuring often enough
    singleElementsUpd = []
    for s in singleElements:
        if countSingleElements[tuple(s)] < K:
            singleElementDict[int(s[1])].remove(s)
            del countSingleElements[tuple(s)]
        else:
            singleElementsUpd.append([s])
    singleElements = singleElementsUpd
    del singleElementsUpd, countSingleElements
    cand = singleElements.copy()
    times = sorted(list(singleElementDict.keys()))
    frequent = []
    while len(cand) > 0:
        newcand = []
        newsmallest = sys.maxsize
        #for all candidates test of appending one element is still frequent
        for c in cand:
            nosuper = True
            #timestamp of last element
            timec = c[len(c)-1][1]
            for t in [tim for tim in times if tim > timec]:
                for com in singleElementDict[t]:
                    comb = c.copy()
                    comb.append(com)
                    countcomb = 0
                    #count appearence of subsequence in log
                    for key in [k for k in keys if k >= len(comb)]:
                        for le in Tdict[key]:
                            if all(elem in le for elem in comb):
                                countcomb += 1
                    if countcomb > K and comb not in newcand:
                        newcand.append(comb)
                        nosuper = False
            if nosuper:
                frequent.append(c)
            else:
                if timec < newsmallest:
                    newsmallest = timec
        #all times that are smaller than smallest in the end of candidate set are unnecessary
        times = [tim for tim in times if tim > newsmallest]
        #new candidates
        cand = newcand
    return frequent