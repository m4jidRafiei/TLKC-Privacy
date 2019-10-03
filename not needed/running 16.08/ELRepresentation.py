from collections import Counter
import operator


class ELRepresentation():

    def __init__(self, log):
        self.log = log


    def simplify_variants(self):
        classifier = ["concept:name"]
        el =[]
        for case_index, case in enumerate(self.log):
            variant = []
            for index, event in enumerate(case):
                for key, value in event.items():
                    if key in classifier:
                        variant.append(value)
            el.append(variant)

        counts =[]
        for var in el:
            counts.append(el.count(var))


        return el, counts


    def simplify_LKC_with_time(self, sensitive, spectime):
        concept = ["concept:name"]
        time = ['time:timestamp']
        logsimple = {}
        traces = []
        sensitives = {el: [] for el in sensitive}
        for case_index, case in enumerate(self.log):
            # as cache for each case
            sens = {}
            trace = []
            bol = True
            for event_index, event in enumerate(case):
                # basis for tuple of (event,time)
                pair = [[], []]
                for key, value in event.items():
                    # Filtering out the needed attributes and create new log out of it
                    # simplify timestamp to timeintervalls as precise as spectime
                    # pair[1] = time
                    if key in time:
                        if event_index == 0:
                            starttime = value
                            pair[1] = 0
                        else:
                            if spectime == "seconds":
                                pair[1] = (value - starttime).total_seconds()
                            elif spectime == "minutes":
                                pair[1] = (value.replace(second=0, microsecond=0)
                                           - starttime.replace(second=0, microsecond=0)).total_seconds() / 60
                            elif spectime == "hours":
                                pair[1] = (value.replace(minute=0, second=0, microsecond=0)
                                           - starttime.replace(minute=0, second=0, microsecond=0)).total_seconds() / 360
                            elif spectime == "days":
                                pair[1] = (value.replace(hour=0, minute=0, second=0, microsecond=0)
                                           - starttime.replace(hour=0, minute=0, second=0,
                                                               microsecond=0)).total_seconds() \
                                          / 8640
                    # pair[0] = event
                    elif key in concept:
                        pair[0] = value
                    elif key in sensitive:
                        # sample all sensitive values for one trace in sens
                        sens[key] = value
                # checking if timestamps are the same, then deleting
                if len(trace) == 0:
                    tu = (pair[0], pair[1])
                    # create trace with pairs (event,time)
                    trace.append(tu)
                # just adding pair if the timestamp is bigger then the one before
                elif pair[1] < trace[len(trace) - 1][1] or (
                        pair[0] == trace[len(trace) - 1][0] and pair[1] == trace[len(trace) - 1][1]):
                    bol = False
                    break
                else:
                    tu = (pair[0], pair[1])
                    trace.append(tu)
            # create simplified log containing new trace (event,time), sensitive attributes
            if bol:
                logsimple[case.attributes["concept:name"]] = {"trace": trace, "sensitive": sens}
                # list with all traces without CaseID
                traces.append(trace)
                # sample all values for a specific sensitive attribute (key) in dict
                for key in sens.keys():
                    # sample all values for a specific sensitive attribute (key) in dict
                    sensitives[key].append(sens[key])
        return logsimple, traces, sensitives

    def simplify_LKC_without_time_count(self, sensitive, spectime):
        concept = ["concept:name"]
        time = ['time:timestamp']
        logsimple = {}
        traces = []
        sensitives = {el: [] for el in sensitive}
        for case_index, case in enumerate(self.log):
            # as cache for each case
            sens = {}
            trace = []
            c = []
            for event_index, event in enumerate(case):
                # basis for tuple of (event,time)
                pair = [[], []]
                for key, value in event.items():
                    # Filtering out the needed attributes and create new log out of it

                    # simplify timestamp to timeintervalls as precise as spectime
                    if key in concept:
                        pair[0] = value
                    elif key in sensitive:
                        # sample all sensitive values for one trace in sens
                        sens[key] = value
                #pair of event, occurence
                count_el = c.count(pair[0])
                tu = (pair[0], count_el + 1)
                c.append(pair[0])
                # create trace with pairs (event,time)
                trace.append(tu)
            #create simplified log
            logsimple[case.attributes["concept:name"]] = {"trace": trace, "sensitive": sens}
            # list with all traces without CaseID
            traces.append(trace)
            # sample all values for a specific sensitive attribute (key) in dict
            for key in sens.keys():
               # sample all values for a specific sensitive attribute (key) in dict
                sensitives[key].append(sens[key])
        return logsimple, traces, sensitives

    def suppression(self, violating, frequent):
        sup = []
        X1 = []
        for v in violating + frequent:
            if isinstance(v[0], str):
                X1.append(v)
            else:
                for sub in v:
                    X1.append(sub)
        X1 = list(set(X1))
        score_res, mvsEl, mfsEl = self.score(violating, frequent, X1)
        # while PG table is not empty do
        while len(score_res) > 0:
            # 4: select a pair w that has the highest Score to suppress;
            w = max(score_res.items(), key=operator.itemgetter(1))[0]
            # 5: delete all MVS and MFS containing w from MVS -tree and MFS - tree;
            list_mvs = mvsEl[w]
            for l in list_mvs:
                violating.remove(l)
            list_mfs = mfsEl[w]
            for l in list_mfs:
                frequent.remove(l)
            # 6: update the Score(p) if both w and p are contained in the same MVS or MFS;
            X1 = []
            for v in violating + frequent:
                if isinstance(v[0], str):
                    X1.append(v)
                else:
                    for sub in v:
                        X1.append(sub)
            X1 = list(set(X1))
            # 7: remove w from PG Table;
            score_res, mvsEl, mfsEl = self.score(violating, frequent, X1)
            # 8: add w to Sup;
            sup.append(w)
        # 9: end
        return sup

    def score(self,violating, frequent, X1):
        priv = {v: 0 for v in X1}
        ut = {f: 0 for f in X1}
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
            if isinstance(f[0], str):
                ut[f] += 1
                mfsEle[f].append(f)
            else:
                for el in f:
                    ut[el] += 1
                    mfsEle[el].append(f)
        score = {el: 0 for el in X1}
        for el in X1:
            score[el] = priv[el] / (ut[el] + 1)
            if score[el] == 0:
                del score[el]
        return score, mvsEle, mfsEle

    def suppressT(self,logsimple, sup):
        for key in logsimple.keys():
            list_trace = logsimple[key]['trace']
            for sub in list_trace:
                if sub in sup:
                    list_trace.remove(sub)
            logsimple[key]['trace'] = list_trace
        return logsimple

