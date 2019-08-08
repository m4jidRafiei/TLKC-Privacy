from pm4py.objects.log.importer.xes import factory as xes_import_factory
import simplifyDeleteTracesStand5
import mvsBoxplot
import PatternMFS
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
logtime = time.time()
print(logtime-start)
L = 10
K = 15
C = 0.9
# Output: Minimal violating sequence V (T )
violating = mvsBoxplot.mvs(T, L, K, C, sensitive, logsimple, cont)
del L, K, C, cont
mvstime = time.time()
print(mvstime-logtime)
print("length violating", len(violating))
K = 5
frequent = PatternMFS.mfs(T, K)
print("length frequent", len(frequent))
mfstime = time.time()
print(mfstime-mvstime)
