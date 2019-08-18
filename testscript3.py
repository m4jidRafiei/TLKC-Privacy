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


logsimple, T, sensitives = repres.simplify_LKC_with_time(sensitive, spectime) #this is simplifyDeleteTracesStand5.simplify()
logsimple_count, T_count, sensitives_count = repres.simplify_LKC_without_time_count(sensitive, spectime)

logtime = time.time()
print("Time creating:", logtime-start)
K = 500

frequent = mfs.frequent_seq_activity(T_count, K)   #this is PatternMFSEvent
frequent2 = mfs.frequent_seq_activityTime(T,K)  # this is PatternMFS
mfstime = time.time()
print("PatternMFSEvent len frequent", len(frequent))
print("PatternMFS len frequent", len(frequent2))
print("Time MFS:", mfstime-logtime)

L = 2
K = 5
C = 0.5

mvs = MVS(T,logsimple,sensitive,cont,sensitives)
contBound = {'Age': 10}
violating = mvs.mvs(L,K,C)
violating2 = mvs.mvs(L,K,C, "dev", contBound)
mvs2 = MVS(T_count,logsimple_count,sensitives_count,cont,sensitives_count,True)
L = 2
K = 50
C = 0.5
violating_count = mvs2.mvs(L,K,C)
violating2_count = mvs2.mvs(L,K,C, "dev", contBound)
mvstime = time.time()
#print("len violating boxplot", len(violating))
#print("len violating deviations", len(violating2))
print("len violating boxplot count", len(violating_count))
print("len violating deviations count", len(violating2_count))
print("Time MVS: ", mvstime - logtime)

sup = repres.suppression(violating_count, frequent)
suptime = time.time()
print("Suppresion: ", suptime-mvstime)
T_ = repres.suppressT(logsimple, sup)
anonymizertime = time.time()
print("Annonymizer: ", anonymizertime-suptime)

log_new = repres.createEventLog(logsimple, spectime)
