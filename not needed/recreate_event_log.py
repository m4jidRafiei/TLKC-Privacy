from pm4py.objects.log.log import TraceLog
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.log.exporter.xes import factory as xes_exporter

L = [1]
C = [0.2, 0.3, 0.4, 0.5]
K = [20, 40, 80, 160]
K2 = [0.7, 0.8, 0.9]
sensitive = ['Age', 'Diagnose']
spectime2 = ["hours", "minutes"]

for l in L:
    i = 1
    for k2 in K2:
        for k in K:
            for c in C:
                for t in spectime2:
                    try:
                        wrong_log = xes_import_factory.apply("xes/seq_count" + "_"  + str(l) + "_" + str(k) + "_" + str(c) + "_" + str(k2) + "_" + t+ ".xes")
                        log = TraceLog([trace for trace in wrong_log])
                        #log = EventLog([trace for trace in wrong_log])
                        #net, initial_marking, final_marking = inductive_miner.apply(log)
                        #print(log[0])
                        xes_exporter.export_log(log, "xes_new/seq_count" + "_" + str(l) + "_" + str(k) + "_" + str(c) + "_" + str(k2) + "_" + t + ".xes" )
                        del log
                    except Exception as e:
                        print(e)