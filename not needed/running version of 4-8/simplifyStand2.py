from datetime import timedelta,datetime,timezone, MINYEAR
from pm4py.objects.log.util import sorting


def simplify(log, sensitive, spectime):
    concept = ["concept:name"]
    time = ['time:timestamp']
#Create log with simplified entries
    logsimple = {}
    traces = []
    sensitives = []
    for case_index, case in enumerate(log):
        sens = {}
        trace = []
        for event_index, event in enumerate(case):
            #basis for tuple of (event,time)
            pair = []
            for key, value in event.items():
                #Filtering out the needed attributes and create new log out of it
                if key in time:
                    if event_index == 0:
                        starttime = value
                        pair.append(0)
                    else:
                        if spectime == "seconds":
                            pair.append((value-starttime).total_seconds())
                        elif spectime == "minutes":
                            pair.append((value.replace(second=0, microsecond=0)
                                         - starttime.replace(second=0, microsecond=0)).total_seconds()/60)
                        elif spectime == "hours":
                            pair.append((value.replace(minute=0, second=0, microsecond=0)
                                         - starttime.replace(minute=0, second=0, microsecond=0)).total_seconds()/360)
                        elif spectime == "day":
                            pair.append((value.replace(hour=0, minute=0, second=0, microsecond=0)
                                         - starttime.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()/8640)
                elif key in concept:
                    pair.append(value)
                elif key in sensitive:
                    sens[key] = value
            #create tuple (event,time) in spectime
            tu = (pair[0], pair[1])
            #create trace with pairs
            trace.append(tu)
        #create simplified log containing new trace (event,time), sensitive attributes
        logsimple[case.attributes["concept:name"]] = {"trace": trace, "sensitive": sens}
        #list with all traces without CaseID
        traces.append(trace)
        #list with all sensitive
        sensitives.append(sens)
    return logsimple, traces, sensitives
