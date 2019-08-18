from pm4py.objects.log.importer.xes import factory as xes_import_factory
import simplifyDeleteTracesStand5
import MVS
import time
#import log (parameters={"max_no_traces_to_import": n} to have a faster workflow), specify sensitive values and how time should be handled
log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")#, parameters={"max_no_traces_to_import": 1000})
sensitive = ['Age', 'Diagnose']
spectime = "seconds"
cont = ['Age']
#contBord * standard deviation is similar


start = time.time()
#T are all traces
logsimple, T, sensitives = simplifyDeleteTracesStand5.simplify(log, sensitive, spectime)

#del log[0].events[0]
#log[0]._list.remove(log[0][21])

logtime = time.time()
print(logtime-start)
L = 2
K = 5
C = 0.5
# Output: Minimal violating sequence V (T )

mvs = MVS.MVS(T,logsimple,sensitive,cont,sensitives)
contBound = {'Age': 10}
violating = mvs.mvs(L,K,C,"dev",contBound)

print(violating)