from pm4py.objects.log.importer.xes import factory as xes_import_factory
import simplifyDeleteTracesStand5
import mvsBoxplot
import PatternMFSEvents
import time
#import log (parameters={"max_no_traces_to_import": n} to have a faster workflow), specify sensitive values and how time should be handled
log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")#, parameters={"max_no_traces_to_import": 1000})
sensitive = ['Age', 'Diagnose']
spectime = "seconds"
cont = ['Age']
#contBord * standard deviation is similar


start = time.time()
#T are all traces
logsimple, T = simplifyDeleteTracesStand5.simplify(log, sensitive, spectime)

#del log[0].events[0]
#log[0]._list.remove(log[0][21])
import createEventLog

logtime = time.time()
print(logtime-start)
K = 50

frequent = PatternMFSEvents.mfs(T, K)
print(len(frequent))
print(frequent)

mvstime = time.time()
print(mvstime-logtime)
