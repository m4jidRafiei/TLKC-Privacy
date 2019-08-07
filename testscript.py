from pm4py.objects.log.importer.xes import factory as xes_import_factory
import simplifyDeleteTracesStand5
import PatternMFS
import time
import deviations
#import log (parameters={"max_no_traces_to_import": n} to have a faster workflow), specify sensitive values and how time should be handled
log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")#, parameters={"max_no_traces_to_import": 1000})
sensitive = ['Age', 'Diagnose']
spectime = "hours"
cont = ['Age']
#contBord * standard deviation is similar
contBound = {'Age': 10}


start = time.time()
#T are all traces
logsimple, T, sensitives = simplifyDeleteTracesStand5.simplify(log, sensitive, spectime)
logtime = time.time()
print(logtime-start)

K = 5
# Output: Minimal violating sequence V (T )

frequent = PatternMFS.mfs(T, K)
#print(frequent)
print(len(frequent))
mvstime = time.time()
print(mvstime-logtime)
