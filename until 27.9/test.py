import gc
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.algo.discovery.inductive import factory as inductive_miner
from pm4py.evaluation.replay_fitness import factory as replay_factory
from pm4py.evaluation.precision import factory as precision_factory
from pm4py.objects.log.exporter.xes import factory as xes_exporter
from ELRepresentation import ELRepresentation
from pm4py.statistics.traces.tracelog import case_statistics
from MFS import MFS
from MVS import MVS
from multiprocessing import Process, Queue

gc.collect()
timeout = 4000
L = [2]
C = [0.5]
K = [2]
K2 = [2]
sensitive = ['Age']
spectime2 = ["seconds"]
cont=['Age']
#cont = ['Age']
#contbound2 = [{"Age":1}]#, {"Age": 2}]
#
#, parameters={"max_no_traces_to_import": 1000})
# #print(log)
mfs = MFS()


def time2(l, k, c, k2, l1, l2, d_time, d_l_time, fitness_time, precision_time, spec,variants,activ_num):
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes", parameters={"max_no_traces_to_import": 50})
    repres = ELRepresentation(log)
    logsimple, T, sensitives = repres.simplify_LKC_with_time(sensitive, spec)
    frequent_time = mfs.frequent_seq_activityTime(T, k2)
    print("frequent time", "\n", len(frequent_time))
    mvs = MVS(T, logsimple, sensitive, cont, sensitives)
    violating = mvs.mvs(l, k, c)
    print("violating:", "\n", len(violating))
    l1.put(len(frequent_time))
    l2.put(len(violating))
    sup_time = repres.suppression(violating, frequent_time)
    T_time = repres.suppressT(logsimple, sup_time)
    log_time, d_time1, d_l_time1 = repres.createEventLog(T_time, spec)
    d_time.put(d_time1)
    d_l_time.put(d_l_time1)
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    net_time, initial_marking_time, final_marking_time = inductive_miner.apply(log_time)
    fitness_time.put(replay_factory.apply(log, net_time, initial_marking_time, final_marking_time)["log_fitness"])
    precision_time.put(precision_factory.apply(log, net_time, initial_marking_time, final_marking_time))
    var_with_count = case_statistics.get_variant_statistics(log_time)
    activ_time = {""}
    for el in var_with_count:
        el['variant'] = el['variant'].split(',')
        activ_time.update(el['variant'])
    activ_time.remove("")
    activ_num.put(len(activ_time))
    print(activ_time)
    xes_exporter.export_log(log_time, "exportedLog.xes")
    variants.put(sum([1 for x in var_with_count]))
if __name__ == '__main__':
    l1 = Queue()
    l2 = Queue()
    d_count = Queue()
    d_l_count = Queue()
    fitness_count = Queue()
    precision_count = Queue()
    variants = Queue()
    activ_num = Queue()
    p = Process(target=time2, name="set_count",
                args=(2,2,0.5,2,l1,l2,d_count,d_l_count,fitness_count,precision_count,"minutes",variants,activ_num))
    p.start()
    p.join()

