from pm4py.objects.log.importer.xes import factory as xes_import_factory
import simplifyStand3
import mvsStand3
import mfsStand3
import time
import deviations
#import log (parameters={"max_no_traces_to_import": n} to have a faster workflow), specify sensitive values and how time should be handled
log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")#, parameters={"max_no_traces_to_import": 1000})
sensitive = ['Age', 'Diagnose']
spectime = "minutes"
cont = ['Age']
#contBord * standard deviation is similar
contBound = {'Age': 10}


start = time.time()
#T are all traces
logsimple, T, sensitives = simplifyStand3.simplify(log, sensitive, spectime)
logtime = time.time()
print(logtime-start)
dev = deviations.deviations(sensitives, cont, contBound)
L = 3
K = 2
C = 0.5
# Output: Minimal violating sequence V (T )
violating = mvsStand3.mvs(T, L, K, C, sensitive, logsimple,cont,dev,sensitives)
del L, K, C, dev, cont, contBound, sensitives
K = 1000
mvstime = time.time()
print(mvstime-logtime)
print(len(violating))
K2 = 50
frequent = mfsStand3.mfs(K2, T)
print(len(frequent))
mfstime = time.time()
print(mfstime-mvstime)
