from pm4py.objects.log.importer.xes import factory as xes_import_factory
from ELRepresentation import ELRepresentation
from MFS import MFS
from MVS import MVS
import time
#import log (parameters={"max_no_traces_to_import": n} to have a faster workflow), specify sensitive values and how time should be handled
log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")#, parameters={"max_no_traces_to_import": 1000})
sensitive = ['Age', 'Diagnose']
spectime = "seconds"
cont = ['Age']
#contBord * standard deviation is similar


start = time.time()
#T are all traces

repres = ELRepresentation(log)  #All the event log manipulations (changes in representation) are supposed to be done in this class
variants, counts = repres.simplify_variants()  #new method to extract sequence of activities (variants) and their frequency

mfs = MFS()  # All the methods assiciated with MFS are supposed to be developed in this class
threshold = 5
frequency = mfs.frequent_variants(variants, counts, threshold) #new method to extract the variants w.r.t a threshold


logsimple, T, sensitives = repres.simplify_LKC(sensitive, spectime) #this is simplifyDeleteTracesStand5.simplify()

logtime = time.time()
print(logtime-start)
K = 500

frequent = mfs.frequent_seq_activity(T, K)   #this is PatternMFSEvent
frequent2 = mfs.frequent_seq_activityTime(T,K)  # this is PatternMFS

print(len(frequent))
print(frequent)

L = 2
K = 5
C = 0.5

mvs = MVS(T,logsimple,sensitive,cont,sensitives)
contBound = {'Age': 10}
violating = mvs.mvs(L,K,C,"dev",contBound)
mvstime = time.time()
print(mvstime-logtime)

sup = repres.suppression(violating, frequent)
suptime = time.time()
print("suppresion", suptime-mvstime)
T_ = repres.suppressT(logsimple, sup)
anonymizertime = time.time()
print(anonymizertime-suptime)
