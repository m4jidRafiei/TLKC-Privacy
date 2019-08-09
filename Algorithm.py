from pm4py.objects.log.importer.xes import factory as xes_import_factory
import simplifyDeleteTracesStand5
import mvsBoxplot
import PatternMFS
import time
import TrajectoryDataAnonymizer
#import log (parameters={"max_no_traces_to_import": n} to have a faster workflow), specify sensitive values and how time should be handled
log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")#, parameters={"max_no_traces_to_import": 1000})
print(log)
sensitive = ['Age', 'Diagnose']
spectime = "minutes"
cont = ['Age']
#contBord * standard deviation is similar


start = time.time()
#T are all traces
logsimple, T = simplifyDeleteTracesStand5.simplify(log, sensitive, spectime)
logtime = time.time()
print(logtime-start)
L = 2
K = 5
C = 0.5
# Output: Minimal violating sequence V (T )
violating = mvsBoxplot.mvs(T, L, K, C, sensitive, logsimple, cont)
#print(len(violating))
#print(violating)
frequent = PatternMFS.mfs(T, K)
#print(len(frequent))
#print(frequent)

sup = TrajectoryDataAnonymizer.suppression(violating, frequent)

T_ = TrajectoryDataAnonymizer.suppressT(logsimple, sup)
mvstime = time.time()
print(mvstime-logtime)
