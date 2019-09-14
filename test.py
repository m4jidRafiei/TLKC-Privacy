import gc
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.algo.discovery.inductive import factory as inductive_miner
from pm4py.evaluation.replay_fitness import factory as replay_factory
from pm4py.evaluation.precision import factory as precision_factory
from ELRepresentation import ELRepresentation
from MFS import MFS
from MVS2 import MVS
import time
from multiprocessing import Process, Queue
import xlsxwriter
gc.collect()
timeout = 4000
L = [2]
C = [0.5]
K = [2]
K2 = [2]
sensitive = {'Diagnose': ["AIDS"]}
spectime2 = ["minutes"]
cont=[]
#cont = ['Age']
#contbound2 = [{"Age":1}]#, {"Age": 2}]
#
log = xes_import_factory.apply("LKC_Artificial.xes")#, parameters={"max_no_traces_to_import": 1000})
# #print(log)
mfs = MFS()


def count(l, k, c, k2, l1, l2, d_count, d_l_count, fitness_count, precision_count, spec):
    log = xes_import_factory.apply("LKC_Artificial.xes")
    repres = ELRepresentation(log)
    logsimple_count, T_count, sensitives_count = repres.simplify_LKC_without_time_count(
        sensitive)
    frequent_count = mfs.frequent_seq_activity(T_count, k2 )
    print("frequent count", "\n", len(frequent_count))
    mvs = MVS(T_count, logsimple_count, sensitive, cont, sensitives_count, True)
    violating_count = mvs.mvs(l, k, c)
    print("violating count:", "\n", len(violating_count))
    l1.put(len(frequent_count))
    l2.put(len(violating_count))
    sup_count = repres.suppression(violating_count, frequent_count)
    T_count = repres.suppressT(logsimple_count, sup_count)
    log_count, d_count1, d_l_count1 = repres.createEventLog(T_count, spec)
    d_count.put(d_count1)
    from pm4py.objects.log.exporter.xes import factory as xes_exporter

    xes_exporter.export_log(log_count, "exportedLog.xes")
    d_l_count.put(d_l_count1)

def set1(l, k, c, k2, l1, l2, d_set, d_l_set, fitness_set, precision_set, spec):
    #log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    repres = ELRepresentation(log)
    logsimple_set, T_set, sensitives_set = repres.simplify_LKC_without_time_set(sensitive)
    frequent_items_set = mfs.frequent_set_miner(T_set, k2/len(T_set))
    print("frequent set", "\n", len(frequent_items_set))
    mvs = MVS(T_set, logsimple_set, sensitive, cont, sensitives_set, count=False, set1=True)
    violating_set = mvs.mvs(l, k, c)
    print("violating set:", "\n", len(violating_set))
    l1.put(len(frequent_items_set))
    l2.put(len(violating_set))
    sup_set = repres.suppression(violating_set, frequent_items_set)
    T_set = repres.suppressT(logsimple_set, sup_set)
    log_set, d_set1, d_l_set1 = repres.createEventLog(T_set, spec)
    d_set.put(d_set1)
    d_l_set.put(d_l_set1)

def time2(l, k, c, k2, l1, l2, d_time, d_l_time, fitness_time, precision_time, spec):
    repres = ELRepresentation(log)
    logsimple, T, sensitives = repres.simplify_LKC_with_time(sensitive, spec)
    frequent_time = mfs.frequent_seq_activityTime(T, k2 * len(T))
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

def count_dev(l, k, c, k2, l1, l2, d_count, d_l_count, fitness_count, precision_count,spec,contbound):
    log = xes_import_factory.apply("LKC_Artificial.xes")
    repres = ELRepresentation(log)
    logsimple_count, T_count, sensitives_count = repres.simplify_LKC_without_time_count(
                sensitive)
    frequent_count = mfs.frequent_seq_activity(T_count, k2)
    print("frequent count", "\n", len(frequent_count))
    mvs = MVS(T_count, logsimple_count, sensitive, cont, sensitives_count, True)
    violating_count = mvs.mvs(l, k, c,type="dev",contbound=contbound)
    print("violating count:", "\n", len(violating_count))
    l1.put(len(frequent_count))
    l2.put(len(violating_count))

    sup_count = repres.suppression(violating_count, frequent_count)
    T_count = repres.suppressT(logsimple_count, sup_count)
    log_count, d_count1, d_l_count1 = repres.createEventLog(T_count, spec)
    d_count.put(d_count1)
    d_l_count.put(d_l_count1)
if __name__ == '__main__':
    l1 = Queue()
    l2 = Queue()
    d_count = Queue()
    d_l_count = Queue()
    fitness_count = Queue()
    precision_count = Queue()
    p = Process(target=set1, name="set1",
                args=(2,2,0.5,2,l1,l2,d_count,d_l_count,fitness_count,precision_count,"minutes"))
    p.start()
    p.join()

