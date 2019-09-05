import runFunction
import gc
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.algo.discovery.inductive import factory as inductive_miner
from pm4py.evaluation.replay_fitness import factory as replay_factory
from pm4py.evaluation.precision import factory as precision_factory

gc.collect()
L = [2, 4, 8, 16]
C = [0.2, 0.4, 0.8]
K = [5, 10, 20, 40, 80]
K2 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
sensitive = ['Age', 'Diagnose']
spectime = ["days", "hours", "minutes", "seconds"]
cont = ['Age']
contbound = [{"Age":1}, { "Age": 2}]
f = open("original.txt", "w")
log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")#, parameters={"max_no_traces_to_import": 1000})
#print(log)
net, initial_marking, final_marking = inductive_miner.apply(log)
fitness = replay_factory.apply(log, net, initial_marking, final_marking)
precision = precision_factory.apply(log, net, initial_marking, final_marking)
f.write("original\n")
f.write("fitness")
f.write(str(fitness))
f.write("\n precision")
f.write(str(precision))
f.close()
for l in L:
    for c in C:
        for k in K:
            for k2 in K2:
                for spec in spectime:
                    for contb in contbound:
                        print(str(l) + str(c)+ str(k)+ str(k2) + str(spec) + str(contb))
                        runFunction.runfunction(l,k,c,k2,sensitive, cont, spec, contb)
                        gc.collect()
