import sys
#adding parents pruning

def mfs(K, T):
    #Tdict = {}
    singleElementDict = {}
    #for t in T:
    #    if len(t) not in Tdict.keys():
    #        Tdict[len(t)] = [t]
    #    else:
    #        Tdict[len(t)].append(t)
    flat_list = [item for sublist in T for item in sublist]
    singleElements = sorted(list(set(flat_list)), key=lambda x: x[1])
    del flat_list
    counts = {tuple(el): 0 for el in singleElements}
    el_traces = {tuple(el): [] for el in singleElements}
    for v in singleElements:
        for t in T:
            if v in t:
                counts[tuple(v)] += 1
                el_traces[tuple(v)].append(t)
        if int(v[1]) not in singleElementDict.keys():
            singleElementDict[int(v[1])] = [v]
        else:
            singleElementDict[int(v[1])].append(v)
    del T
    #start by shortest
    #keys = sorted(list(Tdict.keys()), reverse=True)
    #pruning all single elements not occuring often enough
    singleElementsUpd = []
    for s in singleElements:
        if counts[tuple(s)] < K:
            singleElementDict[int(s[1])].remove(s)
            del counts[tuple(s)]
        else:
            singleElementsUpd.append([s])
    singleElements = singleElementsUpd
    del singleElementsUpd
    cand = singleElements.copy()
    times = sorted(list(singleElementDict.keys()))
    frequent = []
    while len(cand) > 0:
        newcand = []
        newsmallest = sys.maxsize
        #for all candidates test of appending one element is still frequent
        newel_trace = {}
        for c in cand:
            nosuper = True
            #timestamp of last element
            timec = c[len(c)-1][1]
            superfreq = True
            countProb = False
            for t in [tim for tim in times if tim >= timec]:
                for com in singleElementDict[t]:
                    #create new combination
                    comb = c.copy()
                    comb.append(com)
                    if com not in c and comb not in newcand:
                        for f in frequent:
                            #check if f contains all elements in comb
                            if all(elem in f for elem in comb):
                              superfreq = False
                        if superfreq:
                            comb = c.copy()
                            comb.append(com)
                            newel_trace[tuple(comb)] = []
                            countcomb = 0
                            #count appearence of subsequence in log
                            if len(c) == 1:
                                for tr in el_traces[c[0]]:
                                    if len(tr) >= len(comb):
                                        if all(elem in tr for elem in comb):
                                            countcomb += 1
                                            newel_trace[tuple(comb)].append(tr)
                            else:
                                for tr in el_traces[tuple(c)]:
                                    if len(tr) >= len(comb):
                                        if all(elem in tr for elem in comb):
                                            countcomb += 1
                                            newel_trace[tuple(comb)].append(tr)
                            if len(c) == 1:
                                key = c[0]
                            else:
                                key = tuple(c)
                            if counts[key] == countcomb:
                                if comb not in newcand:
                                    newcand.append(comb)
                                    nosuper = False
                                    counts[tuple(comb)] = countcomb
                                countProb = True
                                break
                            elif countcomb > K and comb not in newcand:
                                newcand.append(comb)
                                nosuper = False
                                counts[tuple(comb)] = countcomb
                        else:
                            break
                if countProb or not superfreq:
                    break
            if nosuper:
                frequent.append(c)
            else:
                if timec < newsmallest:
                    newsmallest = timec
        #all times that are smaller than smallest in the end of candidate set are unnecessary
        times = [tim for tim in times if tim >= newsmallest]
        #new candidates
        cand = newcand
        print(newcand)
        el_traces = newel_trace
    return frequent