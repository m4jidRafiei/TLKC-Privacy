from datetime import timedelta,datetime,timezone, MINYEAR

from pm4py.objects.log.importer.xes import factory as xes_import_factory

import numpy
log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
#print(len(log))
#print(log[0])
#l = list([])
#for case_index, case in enumerate(log):
#    for event_index, event in enumerate(case):
#        for key in event.keys():
#            l.append(key)
#print(list(dict.fromkeys(l)))
sensitive = ['Age', 'Diagnose']
timeind = "minutes"

concept = ["concept:name"]
time = ['time:timestamp']
newDict = dict()
# Iterate over all the items in dictionary and filter items which has even keys
c = {}
traces = []
sensitives = []
for case_index, case in enumerate(log):
    sens = {}
    trace = []
    starttime = datetime(MINYEAR ,1,1,0,0,0, tzinfo=timezone(timedelta(0, 7200)))
    for event_index, event in enumerate(case):
        pair = []
        for key, value in event.items():
    # Check if key is even then add pair to new dictionary
            if key in time:
                if event_index == 0:
                    starttime = value
                    pair.append(0)
                else:
                    if timeind == "seconds":
                        #print((value - starttime).total_minutes())
                        pair.append((value-starttime).total_seconds())
                    elif timeind == "minutes":
                        #print((value.replace(second=0, microsecond=0) - starttime.replace(second=0, microsecond=0)))
                        pair.append((value.replace(second=0, microsecond=0) - starttime.replace(second=0, microsecond=0)).total_seconds()/60)
            elif key in concept:
                pair.append(value)
            elif key in sensitive:
                sens[key] = value
        tuple = (pair[0], pair[1])
        trace.append(tuple)
        #trace.append(pair)
    c[case.attributes["concept:name"]] = {"trace": trace, "sensitive": sens}
    traces.append(trace)
    sensitives.append(sens)
#print('Filtered Dictionary : ')
#print(c)
# Input: Raw trajectory data table T
T = traces
# Input: Thresholds L, K, and C
L = 2
K = 2
C = 0.5
# Input: Sensitive values S
S = sensitives
# Output: Minimal violating sequence V (T )
# 1: X1 ! set of all distinct pairs in T;
#print(T)
flat_list = [item for sublist in T for item in sublist]
flat_list2 = [item for sublist in sensitives for item in sublist]
s = list(set(flat_list2))
#print(len(T))
#print(len(flat_list))
X1 = list(set(flat_list))
#X1 = [item for item in list(set(flat_list))]
#print(len(X1))
#print(X1)

# 2: i = 1;
i = 1
# 3: while i <= L or Xi not empty do
while i <= L-1 and len(X1) > 0:
# 4: Scan T to compute |T(q)| and P(s|q), for all q in Xi, for all s in S;
    if i == 1:
        count = {el: 0 for el in X1}
        prob = {el: {el: [] for el in sensitive} for el in X1}
    else:
        count = {tuple(el): 0 for el in X1}
        prob = {tuple(el): {el: [] for el in sensitive} for el in X1}
    for q in X1:
        included = False
        if i == 1:
            for key, value in c.items():
                tr = value["trace"]
                 #print(T)
                S = value["sensitive"]
                 #for tr in T:
                     #print(tr)
                     #print(q)
                if q in tr:
                    #print("test")
                    count[q] += 1
                    for key2, value2 in S.items():
                        prob[q][key2].append(value2)
            for key in sensitive:
                freq = {}
                for item in prob[q][key]:
                    if item in freq:
                        freq[item] += 1
                    else:
                        freq[item] = 1
                    freq[item] = freq[item] / count[q]
                    prob[q][key] = freq
        else:
            for key, value in c.items():
                tr = value["trace"]
            # print(T)
                S = value["sensitive"]
                included = True
                for qparts in q:
                    if qparts not in tr:
                        included = False
                        break
                if included:
                    count[q] += 1
                    for key2, value2 in S.items():
                        prob[tuple(q)][key2].append(value2)
            for key in sensitive:
                freq = {}
                for item in prob[tuple(q)][key]:
                    if item in freq:
                        freq[item] += 1
                    else:
                        freq[item] = 1
                    freq[item] = freq[item] / count[tuple(q)]
                    prob[tuple(q)][key] = freq

    #print(prob)
    #print(count)
# 5: for all q  in Xi where |T(q)| > 0 do
    gen = (q for q in X1 if count[q] > 0)
    violating = []
    w = []
    for q in gen:
# 6: if |T(q)|< K or P(s|q) > C then
        if count[q] < K:
            violating.append(q)
        else:
            highestC = 0
            for s in sensitive:
                if highestC > C:
                    break
                print(s)
                print(prob[q][s])
                if(len(prob[q][s])>1):
                    for key, value in prob[q][s].items():
                        if highestC > C:
                            break
                        if value > highestC:
                            highestC = value
                            if highestC > C:
                                break

 # 7: Add q to Vi;
            if highestC > C:
                violating.append(q)
 # 8: else
# 9: Add q to Wi;
            else:
                w.append(q)
# 10: end if
# 11: end for
    #print(len(violating))
    #print(len(w))
    import operator
    w.sort(key=operator.itemgetter(1))
    #print(w)
    X2 = []
    while len(w) > 1:
        candidate = w.pop(0)
        for comb in w:
            X2.append([candidate, comb])
    print(X2)
# 12: Xi+1 ! Wi ! Wi;
# 13: for %q & Xi+1 do
# 14: if q is a super sequence of any v & Vi then
# 15: Remove q from Xi+1;
# 16: end if
# 17: end for
# 18: i++;
    i += 1
# 19: end while
# 20: return V (T) = V1 ' · · · ' Vi−1;