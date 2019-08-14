import Algorithm
from pm4py.objects.log.importer.xes import factory as xes_import_factory

log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")#, parameters={"max_no_traces_to_import": 1000})

sensitive = ['Age', 'Diagnose']
spectime = "minutes"
cont = ['Age']
L = 2
K = 5
C = 0.5
K_ = 500
log2 = Algorithm.anonymization(log, sensitive, spectime, cont, L, K, C, K_)