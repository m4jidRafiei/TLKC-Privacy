import datetime


def createEventLog(log, simplifiedlog, spectime):
    deleteLog = []
    #for each case
    for i in range(0, len(log)):
        caseId = log[i].attributes["concept:name"]
        #deleted traces will be deleted in the end
        if caseId not in simplifiedlog.keys():
            deleteLog.append(i)
            continue
        #get trace of case
        trace = simplifiedlog[caseId]["trace"]
        k = 0
        #length of trace
        j = 0
        while j < len(log[i]):
            #if the next event in trace of the log is the same as in the suppressed log
            if trace[k][0] == log[i][j]["concept:name"]:
                if spectime == "seconds":
                    if j == 0:
                        starttime = log[i][j]['time:timestamp']
                        #give it a new anonym timestamp
                        log[i][j]['time:timestamp'] = datetime.datetime(year=datetime.MINYEAR, month=1, day=1, hour=0,
                                                                        minute=0,
                                                                        second=0)
                    else:
                        timedif = log[i][j]['time:timestamp'] - starttime
                        years = int(timedif.days/365)
                        daystime = timedif.days - years*365
                        if daystime <= 30:
                           month = 0
                           days = daystime
                        elif daystime <= 58:
                            month = 1
                            days = daystime - 30
                        elif daystime <= 89:
                            month = 2
                            days = daystime - 58
                        elif daystime <= 119:
                            month = 3
                            days = daystime - 89
                        elif daystime <= 150:
                            month = 4
                            days = daystime - 119
                        elif daystime <= 180:
                            month = 5
                            days = daystime - 150
                        elif daystime <= 211:
                            month = 6
                            days = daystime - 180
                        elif daystime <= 242:
                            month = 7
                            days = daystime - 211
                        elif daystime <= 273:
                            month = 8
                            days = daystime - 242
                        elif daystime <=303:
                            month = 9
                            days = daystime - 273
                        elif daystime <= 334:
                            month = 10
                            days = daystime-303
                        elif daystime <= 365:
                            month = 11
                            days = daystime - 334
                        if days != 0:
                            days -= 1
                        sectim = timedif.seconds
                        #60sec -> 1 min, 60*60sec -> 60 min -> 1 hour
                        hours = int(sectim/3600)
                        sectim = sectim - hours*3600
                        minutes = int(sectim/60)
                        sectim = sectim - minutes*60
                        log[i][j]['time:timestamp'] = datetime.datetime(year=datetime.MINYEAR, month=1+month, day=1+days, hour=hours,
                                                                        minute=minutes, second=sectim)
                        k += 1
                elif spectime == "minutes":
                    if j == 0:
                        starttime = log[i][j]['time:timestamp']
                        log[i][j]['time:timestamp'] = datetime.datetime(year=datetime.MINYEAR, month=1,day=1,hour=0,minute=0)
                    else:
                        timedif = log[i][j]['time:timestamp'] - starttime
                        years = int(timedif.days/365)
                        daystime = timedif.days - years*365
                        if daystime <= 30:
                           month = 0
                           days = daystime
                        elif daystime<=58:
                            month = 1
                            days = daystime - 30
                        elif daystime <= 89:
                            month = 2
                            days = daystime - 58
                        elif daystime <= 119:
                            month = 3
                            days = daystime - 89
                        elif daystime <= 150:
                            month = 4
                            days = daystime - 119
                        elif daystime <= 180:
                            month = 5
                            days = daystime - 150
                        elif daystime <= 211:
                            month = 6
                            days = daystime - 180
                        elif daystime <= 242:
                            month = 7
                            days = daystime - 211
                        elif daystime <= 273:
                            month = 8
                            days = daystime - 242
                        elif daystime <=303:
                            month = 9
                            days = daystime - 273
                        elif daystime <= 334:
                            month = 10
                            days = daystime-303
                        elif daystime <= 365:
                            month = 11
                            days = daystime - 334
                        if days != 0:
                            days -= 1
                        sectim = timedif.seconds
                        #60sec -> 1 min, 60*60sec -> 60 min -> 1 hour
                        hours = int(sectim/3600)
                        sectim = sectim - hours*3600
                        minutes = int(sectim/60)
                        log[i][j]['time:timestamp'] = datetime.datetime(year=datetime.MINYEAR, month=1+month, day=1+days, hour=hours,
                                                                        minute=minutes)

                        k += 1
                elif spectime == "hours":
                    if j == 0:
                        starttime = log[i][j]['time:timestamp']
                        log[i][j]['time:timestamp'] = datetime.datetime(year=datetime.MINYEAR, month=1,day=1,hour=0)
                    else:
                        timedif = log[i][j]['time:timestamp'] - starttime
                        years = int(timedif.days/365)
                        daystime = timedif.days - years*365
                        if daystime <= 30:
                           month = 0
                           days = daystime
                        elif daystime<=58:
                            month = 1
                            days = daystime - 30
                        elif daystime <= 89:
                            month = 2
                            days = daystime - 58
                        elif daystime <= 119:
                            month = 3
                            days = daystime - 89
                        elif daystime <= 150:
                            month = 4
                            days = daystime - 119
                        elif daystime <= 180:
                            month = 5
                            days = daystime - 150
                        elif daystime <= 211:
                            month = 6
                            days = daystime - 180
                        elif daystime <= 242:
                            month = 7
                            days = daystime - 211
                        elif daystime <= 273:
                            month = 8
                            days = daystime - 242
                        elif daystime <=303:
                            month = 9
                            days = daystime - 273
                        elif daystime <= 334:
                            month = 10
                            days = daystime-303
                        elif daystime <= 365:
                            month = 11
                            days = daystime - 334
                        if days != 0:
                            days -= 1
                        sectim = timedif.seconds
                        #60sec -> 1 min, 60*60sec -> 60 min -> 1 hour
                        hours = int(sectim/3600)
                        log[i][j]['time:timestamp'] = datetime.datetime(year=datetime.MINYEAR, month=1+month, day=1+days, hour=hours)
                # go in suppressed log one further
                k += 1
                # go in normal log one further
                j += 1
            #if not the same event delete event from trace
            else:
                log[i]._list.remove(log[i][j])
    #delete traces
    for i in sorted(deleteLog, reverse=True):
        log._list.remove(log[i])

    return log
