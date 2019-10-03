import sys
import operator
import DFS
#adding parents pruning


def mfs(K, T):
    #Tdict = {}
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
    del T
    #pruning all single elements not occuring often enough
    singleElementsUpd = []
    for s in singleElements:
        if counts[tuple(s)] < K:
            del counts[tuple(s)]
        else:
            singleElementsUpd.append((s,counts[tuple(s)]))
    #tuple of count and element
    singleElements = singleElementsUpd
    del singleElementsUpd
    cand = singleElements.copy()
    cand.sort(key=operator.itemgetter(1))
    frequent = []
    #for all candidates test of appending one element is still frequent
    candidates = cand.copy()
    for c1 in cand:
        # Mark the current node as visited and store in path
        path = []
        visited = {tuple(c): False for c in candidates}
        parent = [True]
        frequent, el_traces = DFS.dfs(c1,K,path,visited,el_traces,frequent, candidates,parent)

    return frequent

