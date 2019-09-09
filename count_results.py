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
timeout = 4000
L = [8, 16]
C = [0.4, 0.8]
K = [40, 80]
K2 = [0.9]
sensitive = ['Age', 'Diagnose']
spectime2 = ["minutes"]
cont = ['Age']
#contbound2 = [{"Age":1}]#, {"Age": 2}]
#
log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")#, parameters={"max_no_traces_to_import": 1000})
# #print(log)
net, initial_marking, final_marking = inductive_miner.apply(log)
fitness = replay_factory.apply(log, net, initial_marking, final_marking)
precision = precision_factory.apply(log, net, initial_marking, final_marking)
workbook = xlsxwriter.Workbook('resultscount2.xlsx')
worksheet = workbook.add_worksheet("original")
worksheet.write_string(0,0, "fitness")
worksheet.write_string(0,1, "precision")
worksheet.write_number(1,0,fitness["log_fitness"])
worksheet.write_number(1,1,precision)
worksheet = workbook.add_worksheet("count")
worksheet.write_string(0,0, "L")
worksheet.write_string(0,1, "K")
worksheet.write_string(0,2, "C")
worksheet.write_string(0,3, "K'")
worksheet.write_string(0,4, "spectime")
worksheet.write_string(0,5, "fitness")
worksheet.write_string(0,6, "precision")
worksheet.write_string(0,7, "len frequent")
worksheet.write_string(0,8, "len violating")
worksheet.write_string(0,9, "deleted elements")
worksheet.write_string(0,10, "deleted traces")
worksheet.write_string(0,11, "time")
worksheet.write_string(0,12, "error")


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
    l1.put(len(frequent_count))
    l2.put(len(violating_count))

    sup_count = repres.suppression(violating_count, frequent_count)
    T_count = repres.suppressT(logsimple_count, sup_count)
    log_count, d_count1, d_l_count1 = repres.createEventLog(T_count, spec)
    d_count.put(d_count1)
    d_l_count.put(d_l_count1)
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    net_count, initial_marking_count, final_marking_count = inductive_miner.apply(log_count)
    fitness_count.put(replay_factory.apply(log, net_count, initial_marking_count,
                                         final_marking_count)["log_fitness"])
    precision_count.put(precision_factory.apply(log, net_count, initial_marking_count,
                                              final_marking_count))

# def count_dev(l, k, c, k2, l1, l2, d_count, d_l_count, fitness_count, precision_count,spec,contbound):
#     log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
#     repres = ELRepresentation(log)
#     logsimple_count, T_count, sensitives_count = repres.simplify_LKC_without_time_count(
#                 sensitive)
#     frequent_count = mfs.frequent_seq_activity(T_count, k2 * len(T_count))
#     print("frequent count", "\n", len(frequent_count))
#     mvs = MVS(T_count, logsimple_count, sensitive, cont, sensitives_count, True)
#     violating_count = mvs.mvs(l, k, c,type="dev",contbound=contbound)
#     print("violating count:", "\n", len(violating_count))
#     l1.put(len(frequent_count))
#     l2.put(len(violating_count))
#
#     sup_count = repres.suppression(violating_count, frequent_count)
#     T_count = repres.suppressT(logsimple_count, sup_count)
#     log_count, d_count1, d_l_count1 = repres.createEventLog(T_count, spec)
#     d_count.put(d_count1)
#     d_l_count.put(d_l_count1)
#     log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
#     net_count, initial_marking_count, final_marking_count = inductive_miner.apply(log_count)
#     fitness_count.put(replay_factory.apply(log, net_count, initial_marking_count,
#                                                  final_marking_count)["log_fitness"])
#     precision_count.put(precision_factory.apply(log, net_count, initial_marking_count,
#                                                       final_marking_count))

i = 0
if __name__ == '__main__':

    for l in L:
        for c in C:
            for k in K:
                for k2 in K2:
                    for spec in spectime2:
                        i += 1
                        worksheet.write_number(i, 0, l)
                        worksheet.write_number(i, 1, k)
                        worksheet.write_number(i, 2, c)
                        worksheet.write_number(i, 3, k2)
                        worksheet.write_string(i, 4, spec)
                        start = time.time()
                        try:
                            l1 = Queue()
                            l2 = Queue()
                            d_count = Queue()
                            d_l_count = Queue()
                            fitness_count = Queue()
                            precision_count = Queue()
                            p = Process(target=count, name="count", args=(l,k,c,k2,l1,l2,d_count,
                                                                                          d_l_count,fitness_count
                                                                                          ,precision_count,spec))
                            p.start()
                            # Wait a maximum of 10 seconds for foo
                            # Usage: join([timeout in seconds])
                            p.join(timeout)

                            # If thread is active
                            if p.is_alive():
                                print("foo is running... let's kill it...")
                                worksheet.write_string(i, 12, "TimedOut")
                                # Terminate foo
                                p.terminate()
                                p.join()
                                fitness_count.put(-1)
                                precision_count.put(-1)
                                l1.put(-1)
                                l2.put(-1)
                                d_count.put(-1)
                                d_l_count.put(-1)


                            worksheet.write_number(i, 7, l1.get())
                            worksheet.write_number(i, 8, l2.get())

                            worksheet.write_number(i, 9, d_count.get())
                            worksheet.write_number(i, 10, d_l_count.get())
                            #print("count", "\n", "fitness", fitness_count.get(), "\n", "precision", precision_count.get())
                            worksheet.write_number(i, 5, fitness_count.get())
                            worksheet.write_number(i, 6, precision_count.get())
                            finish1 = time.time()
                            t = finish1 - start
                            worksheet.write_number(i, 11, t)
                        except Exception as e:
                            finish1 = time.time()
                            t = finish1 - start
                            worksheet.write_number(i, 11, t)
                            worksheet.write_string(i, 12, str(repr(e)))
                            print(e)

    # worksheet = workbook.add_worksheet("count dev")
    # worksheet.write_string(0, 0, "L")
    # worksheet.write_string(0, 1, "K")
    # worksheet.write_string(0, 2, "C")
    # worksheet.write_string(0, 3, "K'")
    # worksheet.write_string(0, 4, "spectime")
    # worksheet.write_string(0, 5, "dev bound")
    # worksheet.write_string(0, 6, "fitness")
    # worksheet.write_string(0, 7, "precision")
    # worksheet.write_string(0, 8, "len frequent")
    # worksheet.write_string(0, 9, "len violating")
    # worksheet.write_string(0, 10, "deleted elements")
    # worksheet.write_string(0, 11, "deleted traces")
    # worksheet.write_string(0, 12, "time")
    # worksheet.write_string(0, 13, "error")
    #
    # mfs = MFS()
    #
    #
    #
    #
    # i = 0
    # for l in L:
    #     for c in C:
    #         for k in K:
    #             for k2 in K2:
    #                 for contbound in contbound2:
    #                     for spec in spectime2:
    #                         i += 1
    #                         worksheet.write_number(i, 0, l)
    #                         worksheet.write_number(i, 1, k)
    #                         worksheet.write_number(i, 2, c)
    #                         worksheet.write_number(i, 3, k2)
    #                         worksheet.write_string(i, 4, spec)
    #                         worksheet.write_number(i, 5, contbound["Age"])
    #                         start = time.time()
    #                         try:
    #                             l1 = Queue()
    #                             l2 = Queue()
    #                             d_count = Queue()
    #                             d_l_count = Queue()
    #                             fitness_count = Queue()
    #                             precision_count = Queue()
    #                             p = Process(target=count_dev, name="count_dev", args=(l, k, c, k2, l1, l2, d_count, d_l_count,
    #                                                                                   fitness_count, precision_count
    #                                                                                   ,spec,contbound))
    #                             p.start()
    #                             # Wait a maximum of 10 seconds for foo
    #                             # Usage: join([timeout in seconds])
    #                             #
    #                             p.join(timeout)
    #                                 # If thread is active
    #                             if p.is_alive():
    #                                 print("foo is running... let's kill it...")
    #                                 worksheet.write_string(i, 13, "TimedOut")
    #                                 # Terminate foo
    #                                 p.terminate()
    #                                 p.join()
    #                                 fitness_count.put(-1)
    #                                 precision_count.put(-1)
    #                                 l1.put(-1)
    #                                 l2.put(-1)
    #                                 d_l_count.put(-1)
    #                                 d_count.put(-1)
    #
    #                             worksheet.write_number(i, 8, l1.get())
    #                             worksheet.write_number(i, 9, l2.get())
    #                             worksheet.write_number(i, 10, d_count.get())
    #                             worksheet.write_number(i, 11, d_l_count.get())
    #                             worksheet.write_number(i, 6, fitness_count.get())
    #                             worksheet.write_number(i, 7, precision_count.get())
    #                             finish1 = time.time()
    #                             t = finish1 - start
    #                             worksheet.write_number(i, 12 , t)
    #                         except Exception as e:
    #                             finish1 = time.time()
    #                             t = finish1 - start
    #                             worksheet.write_number(i, 12, t)
    #                             worksheet.write_string(i, 13, str(repr(e)))
    #                             print(e)

    workbook.close()