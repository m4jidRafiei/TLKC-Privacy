#Input: log (dict) log given by the user
#Input: sensitive (list) sensitive attributes
#Input: spectime (str) accuracy of timestamp
#Output: log (dict) with simplified entries {traces: (event,timestamp), sensitive: {att:[values]}}
#Output: traces (list) containing all possible traces
#Output: sensitives (dict) containing for each sensitive attribute all values
def simplify(log, sensitive, spectime):
    concept = ["concept:name"]
    time = ['time:timestamp']
    logsimple = {}
    traces = []
    sensitives = {el: [] for el in sensitive}
    for case_index, case in enumerate(log):
        #as cache for each case
        sens = {}
        trace = []
        for event_index, event in enumerate(case):
            #basis for tuple of (event,time)
            pair = [[],[]]
            for key, value in event.items():
                #Filtering out the needed attributes and create new log out of it

                #simplify timestamp to timeintervalls as precise as spectime
                #pair[1] = time
                if key in time:
                    if event_index == 0:
                        starttime = value
                        pair[1] = 0
                    else:
                        if spectime == "seconds":
                            pair[1] = (value - starttime).total_seconds()
                        elif spectime == "minutes":
                            pair[1] = (value.replace(second=0, microsecond=0)
                                         - starttime.replace(second=0, microsecond=0)).total_seconds()/60
                        elif spectime == "hours":
                            pair[1] = (value.replace(minute=0, second=0, microsecond=0)
                                         - starttime.replace(minute=0, second=0, microsecond=0)).total_seconds()/360
                        elif spectime == "days":
                            pair[1] = (value.replace(hour=0, minute=0, second=0, microsecond=0) - starttime.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()/8640
                #pair[0] = event
                elif key in concept:
                    pair[0] = value
                elif key in sensitive:
                    #sample all sensitive values for one trace in sens
                    sens[key] = value
                    #sample all values for a specific sensitive attribute (key) in dict
                    sensitives[key].append(value)
            #checking if timestamps are the same, then deleting
            # TODO: maybe different handeling
            if len(trace) == 0:
                tu = (pair[0], pair[1])
                # create trace with pairs (event,time)
                trace.append(tu)
            #just adding pair if the timestamp is bigger then the one before
            elif pair[1] > trace[len(trace)-1][1]:
                tu = (pair[0], pair[1])
                #create trace with pairs (event,time)
                trace.append(tu)
        #create simplified log containing new trace (event,time), sensitive attributes
        logsimple[case.attributes["concept:name"]] = {"trace": trace, "sensitive": sens}
        #list with all traces without CaseID
        traces.append(trace)
    return logsimple, traces, sensitives
