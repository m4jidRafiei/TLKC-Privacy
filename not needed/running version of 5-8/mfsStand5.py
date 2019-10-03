import sys
import operator
import DFS6
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
    #pruning all single elements not occuring often enough
    singleElementsUpd = []
    for s in singleElements:
        if counts[tuple(s)] < K:
            singleElementDict[int(s[1])].remove(s)
            del counts[tuple(s)]
        else:
            singleElementsUpd.append(s)
    singleElements = singleElementsUpd
    del singleElementsUpd
    cand = singleElements.copy()
    frequent = []
    #for all candidates test of appending one element is still frequent
    candidates = cand.copy()
    for c1 in cand:
        # Mark the current node as visited and store in path
        path = []
        visited = {tuple(c): False for c in candidates}
        parent = [True]
        frequent_cache = []
        frequent, el_traces = DFS6.dfs(c1,K,path,visited,el_traces,frequent, candidates, parent, frequent_cache)

    return frequent

