def mvs(T, L, K, C, sensitive, logsimple):
    # Input: Raw trajectory data table T
    # Input: Thresholds L, K, and C
    # Input: Sensitive values S
    # 1: X1 ! set of all distinct pairs in T;
    flat_list = [item for sublist in T for item in sublist]
    X1 = list(set(flat_list))
    # 2: i = 1;
    count = {el: 0 for el in X1}
    prob = {el: {el: [] for el in sensitive} for el in X1}
    for q in X1:
        for key, value in logsimple.items():
            tr = value["trace"]
            S = value["sensitive"]
            if q in tr:
                # print("test")
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
    # 5: for all q  in Xi where |T(q)| > 0 do
    gen = [q for q in X1 if count[tuple(q)] > 0]
    violating = [[]]
    w = [[]]
    for q in gen:
        # 6: if |T(q)|< K or P(s|q) > C then
        if count[q] < K:
            violating[0].append(q)
        else:
            highestC = 0
            for s in sensitive:
                if highestC > C:
                    break
                if (len(prob[q][s]) > 1):
                    for key, value in prob[q][s].items():
                        if highestC > C:
                            break
                        if value > highestC:
                            highestC = value
                            if highestC > C:
                                break

            # 7: Add q to Vi;
            if highestC > C:
                violating[0].append(q)
            # 8: else
            # 9: Add q to Wi;
            else:
                w[0].append(q)
    # 10: end if
    # 11: end for
    import operator
    w[0].sort(key=operator.itemgetter(1))
    X1.clear()
    # 12: Xi+1 ! Wi ! Wi;
    while len(w[0]) > 1:
        candidate = w[0].pop(0)
        for comb in w[0]:
            if comb[1] > candidate[1]:
                X1.append([candidate, comb])
    # 13: for %q & Xi+1 do
    # should not be necessary for first round
    # 15: Remove q from Xi+1;
    # 16: end if
    # 17: end for
    print("first setlength:", len(X1))
    i = 1
    # 3: while i <= L or Xi not empty do
    while i + 1 <= L and len(X1) > 0:
        # 4: Scan T to compute |T(q)| and P(s|q), for all q in Xi, for all s in S;
        w.append([])
        violating.append([])
        count = {tuple(el): 0 for el in X1}
        prob = {tuple(el): {el: [] for el in sensitive} for el in X1}
        for q in X1:
            for key, value in logsimple.items():
                tr = value["trace"]
                S = value["sensitive"]
                included = True
                for qparts in q:
                    if qparts not in tr:
                        included = False
                        break
                if included:
                    count[tuple(q)] += 1
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
        # 5: for all q  in Xi where |T(q)| > 0 do
        gen = [q for q in X1 if count[tuple(q)] > 0]
        #print(len(gen))
        for q in gen:
            # 6: if |T(q)|< K or P(s|q) > C then
            if count[tuple(q)] < K:
                violating[i].append(q)
            else:
                highestC = 0
                for s in sensitive:
                    if highestC > C:
                        break
                    if len(prob[tuple(q)][s]) > 1:
                        for key, value in prob[tuple(q)][s].items():
                            if highestC > C:
                                break
                            if value > highestC:
                                highestC = value
                                if highestC > C:
                                    break
                # 7: Add q to Vi;
                if highestC > C:
                    violating[i].append(q)
                # 8: else
                # 9: Add q to Wi;
                else:
                    w[i].append(q)
        # 10: end if
        # 11: end for
        X1.clear()
        # 12: Xi+1 ! Wi ! Wi;
        for candidate in w[i]:
            for comb in w[i]:
                if comb[1] <= candidate[1]:
                    break
                if candidate[0:i - 1] == comb[0:i - 1] and candidate[i][1] < comb[i][1]:
                    X1.append([])
                    X1[len(X1) - 1] = candidate[:]
                    X1[len(X1) - 1].append(comb[i])
                    if X1[len(X1) - 1] in X1[0:len(X1) - 2]:
                        del X1[-1]
                    else:
                        # 13: for %q & Xi+1 do
                        # 14: if q is a super sequence of any v & Vi then
                        # 15: Remove q from Xi+1;
                        for v in violating[i]:
                            if len(X1) == 0:
                                break
                            if all(elem in X1[len(X1) - 1] for elem in v):
                                del X1[-1]
        # 18: i++;
        i += 1
    # 19: end while
    # 20: return V (T) = V1 ' · · · ' Vi−1;
    violatingConj = [item for sublist in violating for item in sublist]
    return violatingConj
