from pm4py.objects.log.importer.xes import factory as xes_import_factory
from ELRepresentation import ELRepresentation
from MFS import MFS
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

repres = ELRepresentation(log)  #All the event log manipulations (changes in representation) are supposed to be done in this class
variants, counts = repres.simplify_variants()  #new method to extract sequence of activities (variants) and their frequency

mfs = MFS()  # All the methods assiciated with MFS are supposed to be developed in this class
threshold = 5
frequency = mfs.frequent_variants(variants, counts, threshold) #new method to extract the variants w.r.t a threshold


logsimple, T = repres.simplify_LKC(sensitive, spectime) #this is simplifyDeleteTracesStand5.simplify()

#del log[0].events[0]
#log[0]._list.remove(log[0][21])
import createEventLog

logtime = time.time()
print(logtime-start)
K = 500

frequent = mfs.frequent_seq_activity(T, K)   #this is PatternMFSEvent
frequent = mfs.frequent_seq_activityTime(T,K)  # this is PatternMFS

print(len(frequent))
print(frequent)

mvstime = time.time()
print(mvstime-logtime)
