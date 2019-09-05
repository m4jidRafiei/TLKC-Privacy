import gc
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.algo.discovery.inductive import factory as inductive_miner
from pm4py.evaluation.replay_fitness import factory as replay_factory
from pm4py.evaluation.precision import factory as precision_factory
from ELRepresentation import ELRepresentation
from MFS import MFS
from MVS import MVS
import time
from multiprocessing import Process, Queue
import xlsxwriter
gc.collect()
timeout = 100
L = [2,  8, 16]
C = [ 0.4, 0.8]
K = [ 40, 80]
K2 = [0.7,  0.9]
sensitive = ['Age', 'Diagnose']
spectime2 = ["days", "minutes"]
cont = ['Age']
contbound2 = [{"Age":1}]#, {"Age": 2}]
#
log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")#, parameters={"max_no_traces_to_import": 1000})
# #print(log)
net, initial_marking, final_marking = inductive_miner.apply(log)
fitness = replay_factory.apply(log, net, initial_marking, final_marking)
precision = precision_factory.apply(log, net, initial_marking, final_marking)
# workbook = xlsxwriter.Workbook('resultscount2.xlsx')
# worksheet = workbook.add_worksheet("original")
# worksheet.write_string(0,0, "fitness")
# worksheet.write_string(0,1, "precision")
# worksheet.write_number(1,0,fitness["log_fitness"])
# worksheet.write_number(1,1,precision)
# worksheet = workbook.add_worksheet("count")
# worksheet.write_string(0,0, "L")
# worksheet.write_string(0,1, "K")
# worksheet.write_string(0,2, "C")
# worksheet.write_string(0,3, "K'")
# worksheet.write_string(0,4, "spectime")
# worksheet.write_string(0,5, "fitness")
# worksheet.write_string(0,6, "precision")
# worksheet.write_string(0,7, "len frequent")
# worksheet.write_string(0,8, "len violating")
# worksheet.write_string(0,9, "deleted elements")
# worksheet.write_string(0,10, "deleted traces")
# worksheet.write_string(0,11, "time")
# worksheet.write_string(0,12, "error")
workbook2 = xlsxwriter.Workbook('resultsset2.xlsx')
worksheet2 = workbook2.add_worksheet("original")
worksheet2.write_string(0,0, "fitness")
worksheet2.write_string(0,1, "precision")
worksheet2.write_number(1,0,fitness["log_fitness"])
worksheet2.write_number(1,1,precision)
worksheet2 = workbook2.add_worksheet("set")
worksheet2.write_string(0,0, "L")
worksheet2.write_string(0,1, "K")
worksheet2.write_string(0,2, "C")
worksheet2.write_string(0,3, "K'")
worksheet2.write_string(0,4, "spectime")
worksheet2.write_string(0,5, "fitness")
worksheet2.write_string(0,6, "precision")
worksheet2.write_string(0,7, "len frequent")
worksheet2.write_string(0,8, "len violating")
worksheet2.write_string(0,9, "deleted elements")
worksheet2.write_string(0,10, "deleted traces")
worksheet2.write_string(0,11, "time")
worksheet2.write_string(0,12, "error")
workbook3 = xlsxwriter.Workbook('resultssetcount2.xlsx')
worksheet3 = workbook3.add_worksheet("original")
worksheet3.write_string(0,0, "fitness")
worksheet3.write_string(0,1, "precision")
worksheet3.write_number(1,0,fitness["log_fitness"])
worksheet3.write_number(1,1,precision)
worksheet3 = workbook3.add_worksheet("setcount")
worksheet3.write_string(0,0, "L")
worksheet3.write_string(0,1, "K")
worksheet3.write_string(0,2, "C")
worksheet3.write_string(0,3, "K'")
worksheet3.write_string(0,4, "spectime")
worksheet3.write_string(0,5, "fitness")
worksheet3.write_string(0,6, "precision")
worksheet3.write_string(0,7, "len frequent")
worksheet3.write_string(0,8, "len violating")
worksheet3.write_string(0,9, "deleted elements")
worksheet3.write_string(0,10, "deleted traces")
worksheet3.write_string(0,11, "time")
worksheet3.write_string(0,12, "error")
workbook4 = xlsxwriter.Workbook('resultstime2.xlsx')
worksheet4 = workbook4.add_worksheet("original")
worksheet4.write_string(0,0, "fitness")
worksheet4.write_string(0,1, "precision")
worksheet4.write_number(1,0,fitness["log_fitness"])
worksheet4.write_number(1,1,precision)
worksheet4 = workbook4.add_worksheet("time")
worksheet4.write_string(0,0, "L")
worksheet4.write_string(0,1, "K")
worksheet4.write_string(0,2, "C")
worksheet4.write_string(0,3, "K'")
worksheet4.write_string(0,4, "spectime")
worksheet4.write_string(0,5, "fitness")
worksheet4.write_string(0,6, "precision")
worksheet4.write_string(0,7, "len frequent")
worksheet4.write_string(0,8, "len violating")
worksheet4.write_string(0,9, "deleted elements")
worksheet4.write_string(0,10, "deleted traces")
worksheet4.write_string(0,11, "time")
worksheet4.write_string(0,12, "error")


mfs = MFS()


def count(l, k, c, k2, l1, l2, d_count, d_l_count, fitness_count, precision_count, spec):
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    repres = ELRepresentation(log)
    logsimple_count, T_count, sensitives_count = repres.simplify_LKC_without_time_count(
        sensitive)
    frequent_count = mfs.frequent_seq_activity(T_count, k2 * len(T_count))
    print("frequent count", "\n", len(frequent_count))
    mvs = MVS(T_count, logsimple_count, sensitive, cont, sensitives_count, True)
    violating_count = mvs.mvs(l, k, c)
    print("violating count:", "\n", len(violating_count))
    l1 = len(frequent_count)
    l2 = len(violating_count)

    sup_count = repres.suppression(violating_count, frequent_count)
    T_count = repres.suppressT(logsimple_count, sup_count)
    log_count, d_count, d_l_count = repres.createEventLog(T_count, spec)
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    net_count, initial_marking_count, final_marking_count = inductive_miner.apply(log_count)
    fitness_count.put(replay_factory.apply(log, net_count, initial_marking_count,
                                         final_marking_count)["log_fitness"])
    precision_count.put(precision_factory.apply(log, net_count, initial_marking_count,
                                              final_marking_count))

def count_dev(l, k, c, k2, l1, l2, d_count, d_l_count, fitness_count, precision_count,spec,contbound):
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    repres = ELRepresentation(log)
    logsimple_count, T_count, sensitives_count = repres.simplify_LKC_without_time_count(
                sensitive)
    frequent_count = mfs.frequent_seq_activity(T_count, k2 * len(T_count))
    print("frequent count", "\n", len(frequent_count))
    mvs = MVS(T_count, logsimple_count, sensitive, cont, sensitives_count, True)
    violating_count = mvs.mvs(l, k, c,type="dev",contbound=contbound)
    print("violating count:", "\n", len(violating_count))
    l1 = len(frequent_count)
    l2 = len(violating_count)

    sup_count = repres.suppression(violating_count, frequent_count)
    T_count = repres.suppressT(logsimple_count, sup_count)
    log_count, d_count, d_l_count = repres.createEventLog(T_count, spec)
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    net_count, initial_marking_count, final_marking_count = inductive_miner.apply(log_count)
    fitness_count.put(replay_factory.apply(log, net_count, initial_marking_count,
                                                 final_marking_count)["log_fitness"])
    precision_count.put(precision_factory.apply(log, net_count, initial_marking_count,
                                                      final_marking_count))

def set(l, k, c, k2, l1, l2, d_count, d_l_count, fitness_set, precision_set, spec):
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    repres = ELRepresentation(log)
    logsimple_set, T_set, sensitives_set = repres.simplify_LKC_without_time_set(sensitive)
    frequent_items_set = mfs.frequent_set_miner(T_set, k2 * len(T_set))
    print("frequent set", "\n", len(frequent_items_set))
    mvs = MVS(T_set, logsimple_set, sensitive, cont, sensitives_set, count=False, set=True)
    violating_set = mvs.mvs(l, k, c)
    print("violating set:", "\n", len(violating_set))
    l1 = len(frequent_items_set)
    l2 = len(violating_set)
    sup_set = repres.suppression(violating_set, frequent_items_set)
    T_set = repres.suppressT(logsimple_set, sup_set)
    log_set, d_set, d_l_set = repres.createEventLog(T_set, spec)
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    net_set, initial_marking_set, final_marking_set = inductive_miner.apply(log_set)
    fitness_set.put(replay_factory.apply(log, net_set, initial_marking_set, final_marking_set)["log_fitness"])
    precision_set.put(precision_factory.apply(log, net_set, initial_marking_set, final_marking_set))

def set_dev(l, k, c, k2, l1, l2, d_count, d_l_count, fitness_set, precision_set,spec,contbound):
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    repres = ELRepresentation(log)
    logsimple_set, T_set, sensitives_set = repres.simplify_LKC_without_time_set(sensitive)
    frequent_items_set = mfs.frequent_set_miner(T_set, k2 * len(T_set))
    print("frequent set", "\n", len(frequent_items_set))
    mvs = MVS(T_set, logsimple_set, sensitive, cont, sensitives_set, count=False, set=True)
    violating_set = mvs.mvs(l, k, c,type="dev",contbound=contbound)
    print("violating set:", "\n", len(violating_set))
    l1 = len(frequent_items_set)
    l2 = len(violating_set)
    sup_set = repres.suppression(violating_set, frequent_items_set)
    T_set = repres.suppressT(logsimple_set, sup_set)
    log_set, d_set, d_l_set = repres.createEventLog(T_set, spec)
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    net_set, initial_marking_set, final_marking_set = inductive_miner.apply(log_set)
    fitness_set.put(replay_factory.apply(log, net_set, initial_marking_set, final_marking_set)["log_fitness"])
    precision_set.put(precision_factory.apply(log, net_set, initial_marking_set, final_marking_set))

def set_count(l, k, c, k2, l1, l2, d_count, d_l_count, fitness_set_count, precision_set_count, spec):
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    repres = ELRepresentation(log)
    logsimple_set_count, T_set_count, sensitives_set_count = repres.simplify_LKC_without_time_count_set(sensitive)
    frequent_items_count_set = mfs.frequent_set_miner(T_set_count, k2 * len(T_set_count))
    print("frequent set and count", "\n", len(frequent_items_count_set))
    mvs = MVS(T_set_count, logsimple_set_count, sensitive, cont, sensitives_set_count, True, True)
    violating_count_set = mvs.mvs(l, k, c)
    print("violating count and set:", "\n", len(violating_count_set))
    l1 = len(frequent_items_count_set)
    l2 = len(violating_count_set)
    sup_set_count = repres.suppression(violating_count_set, frequent_items_count_set)
    T_set_count = repres.suppressT(logsimple_set_count, sup_set_count)
    log_set_count, d_set_count, d_l_set_count = repres.createEventLog(T_set_count, spec)
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    net_set_count, initial_marking_set_count, final_marking_set_count = inductive_miner.apply(log_set_count)
    fitness_set_count.put(replay_factory.apply(log, net_set_count, initial_marking_set_count
                                                 , final_marking_set_count))
    precision_set_count.put(precision_factory.apply(log, net_set_count, initial_marking_set_count
                                                      , final_marking_set_count))


def set_count_dev(l, k, c, k2, l1, l2, d_count, d_l_count, fitness_set_count, precision_set_count,spec,contbound):
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    repres = ELRepresentation(log)
    logsimple_set_count, T_set_count, sensitives_set_count = repres.simplify_LKC_without_time_count_set(sensitive)
    frequent_items_count_set = mfs.frequent_set_miner(T_set_count, k2 * len(T_set_count))
    print("frequent set and count", "\n", len(frequent_items_count_set))
    mvs = MVS(T_set_count, logsimple_set_count, sensitive, cont, sensitives_set_count, True, True)
    violating_count_set = mvs.mvs(l, k, c, type="dev", contbound=contbound)
    print("violating count and set dev:", "\n", len(violating_count_set))
    l1 = len(frequent_items_count_set)
    l2 = len(violating_count_set)
    sup_set_count = repres.suppression(violating_count_set, frequent_items_count_set)
    T_set_count = repres.suppressT(logsimple_set_count, sup_set_count)
    log_set_count, d_set_count, d_l_set_count = repres.createEventLog(T_set_count, spec)
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    net_set_count, initial_marking_set_count, final_marking_set_count = inductive_miner.apply(log_set_count)
    fitness_set_count.put(replay_factory.apply(log, net_set_count, initial_marking_set_count
                                                 , final_marking_set_count)["log_fitness"])
    precision_set_count.put(precision_factory.apply(log, net_set_count, initial_marking_set_count
                                                      , final_marking_set_count))

def time2(l, k, c, k2, l1, l2, d_time, d_l_time, fitness_time, precision_time, spec):
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
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
    print("time", "\n", "fitness", fitness_time, "\n", "precision", precision_time)

def time_dev(l, k, c, k2, l1, l2, d_time_dev, d_l_time_dev, fitness_time, precision_time, spec, contbound):
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    repres = ELRepresentation(log)
    logsimple, T, sensitives = repres.simplify_LKC_with_time(sensitive, spec)
    frequent_time = mfs.frequent_seq_activityTime(T, k2 * len(T))
    print("frequent time", "\n", len(frequent_time))
    mvs = MVS(T, logsimple, sensitive, cont, sensitives)
    violating_dev = mvs.mvs(l, k, c, type="dev", contbound=contbound)
    print("violating dev:", "\n", len(violating_dev))
    l1.put(len(frequent_time))
    l2.put(len(violating_dev))
    sup_time_dev = repres.suppression(violating_dev, frequent_time)
    T_time_dev = repres.suppressT(logsimple, sup_time_dev)
    log_time_dev, d_time_dev1, d_l_time_dev1 = repres.createEventLog(T_time_dev, spec)
    d_time_dev.put(d_time_dev1)
    d_l_time_dev.put(d_l_time_dev1)
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    net_time_dev, initial_marking_time_dev, final_marking_time_dev = inductive_miner.apply(log_time_dev)
    fitness_time.put(replay_factory.apply(log, net_time_dev, initial_marking_time_dev, final_marking_time_dev)["log_fitness"])
    precision_time.put(precision_factory.apply(log, net_time_dev, initial_marking_time_dev
                                                     , final_marking_time_dev))


i = 0
if __name__ == '__main__':
    ###time####



    i=0
    for l in L:
        for c in C:
            for k in K:
                for k2 in K2:
                    for spec in spectime2:
                        i += 1
                        worksheet4.write_number(i, 0, l)
                        worksheet4.write_number(i, 1, k)
                        worksheet4.write_number(i, 2, c)
                        worksheet4.write_number(i, 3, k2)
                        worksheet4.write_string(i, 4, spec)
                        start = time.time()
                        try:
                            l1 = Queue()
                            l2 = Queue()
                            d_time = Queue()
                            d_l_time = Queue()
                            fitness_time = Queue()
                            precision_time = Queue()
                            p = Process(target=time2, name="time2", args=(l, k, c, k2, l1, l2,
                                                                          d_time, d_l_time,
                                                                          fitness_time, precision_time, spec))
                            p.start()
                            # Wait a maximum of 10 seconds for foo
                            # Usage: join([timeout in seconds])
                            p.join(timeout)

                            # If thread is active
                            if p.is_alive():
                                print("foo is running... let's kill it...")
                                worksheet4.write_string(i, 12, "TimedOut")
                                # Terminate foo
                                p.terminate()
                                p.join()
                                precision_time.put(-1)
                                fitness_time.put(-1)
                                l1.put(-1)
                                l2.put(-1)
                                d_time.put(-1)
                                d_l_time.put(-1)

                            worksheet4.write_number(i, 7, l1.get())
                            worksheet4.write_number(i, 8, l2.get())

                            worksheet4.write_number(i, 9, d_time.get())
                            worksheet4.write_number(i, 10, d_l_time.get())
                            #print("time", "\n", "fitness", fitness_time.get(), "\n", "precision", precision_time.get())
                            worksheet4.write_number(i, 5, fitness_time.get())
                            worksheet4.write_number(i, 6, precision_time.get())
                            finish1 = time.time()
                            t = finish1 - start
                            worksheet4.write_number(i, 11, t)
                        except Exception as e:
                            finish1 = time.time()
                            t = finish1 - start
                            worksheet4.write_number(i, 11, t)
                            worksheet4.write_string(i, 12, str(repr(e)))
                            print(e)

    worksheet = workbook4.add_worksheet("set dev")
    worksheet.write_string(0, 0, "L")
    worksheet.write_string(0, 1, "K")
    worksheet.write_string(0, 2, "C")
    worksheet.write_string(0, 3, "K'")
    worksheet.write_string(0, 4, "spectime")
    worksheet.write_string(0, 5, "dev bound")
    worksheet.write_string(0, 6, "fitness")
    worksheet.write_string(0, 7, "precision")
    worksheet.write_string(0, 8, "len frequent")
    worksheet.write_string(0, 9, "len violating")
    worksheet.write_string(0, 10, "deleted elements")
    worksheet.write_string(0, 11, "deleted traces")
    worksheet.write_string(0, 12, "time")
    worksheet.write_string(0, 13, "error")




    i = 0
    for l in L:
        for c in C:
            for k in K:
                for k2 in K2:
                    for contbound in contbound2:
                        for spec in spectime2:
                            i += 1
                            worksheet.write_number(i, 0, l)
                            worksheet.write_number(i, 1, k)
                            worksheet.write_number(i, 2, c)
                            worksheet.write_number(i, 3, k2)
                            worksheet.write_string(i, 4, spec)
                            worksheet.write_number(i, 5, contbound["Age"])
                            start = time.time()
                            try:
                                l1 = Queue()
                                l2 = Queue()
                                d_time_dev = Queue()
                                d_l_time_dev = Queue()
                                fitness_time = Queue()
                                precision_time = Queue()
                                p = Process(target=time_dev, name="time_dev", args=(l, k, c, k2, l1, l2, d_time_dev,
                                                                                    d_l_time_dev, fitness_time,
                                                                                    precision_time, spec, contbound))
                                p.start()
                                # Wait a maximum of 10 seconds for foo
                                # Usage: join([timeout in seconds])
                                #
                                p.join(timeout)
                                # If thread is active
                                if p.is_alive():
                                    print("foo is running... let's kill it...")
                                    worksheet.write_string(i, 13, "TimedOut")
                                    # Terminate foo
                                    p.terminate()
                                    p.join()
                                    fitness_time.put(-1)
                                    precision_time.put(-1)
                                    l1.put(-1)
                                    l2.put(-1)
                                    d_time_dev.put(-1)
                                    d_l_time_dev.put(-1)

                                worksheet.write_number(i, 8, l1.get())
                                worksheet.write_number(i, 9, l2.get())
                                worksheet.write_number(i, 10, d_time_dev.get())
                                worksheet.write_number(i, 11, d_l_time_dev.get())
                                #print("time", "\n", "fitness", fitness_time.get(), "\n", "precision", precision_time.get())
                                worksheet.write_number(i, 6, fitness_time.get())
                                worksheet.write_number(i, 7, precision_time.get())
                                finish1 = time.time()
                                t = finish1 - start
                                worksheet.write_number(i, 12, t)
                            except Exception as e:
                                finish1 = time.time()
                                t = finish1 - start
                                worksheet.write_number(i, 12, t)
                                worksheet.write_string(i, 13, str(repr(e)))
                                print(e)

    workbook4.close()