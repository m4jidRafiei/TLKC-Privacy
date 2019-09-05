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
C = [0.4, 0.8]
K = [40, 80]
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



mfs = MFS()


def set(l, k, c, k2, l1, l2, d_set, d_l_set, fitness_set, precision_set, spec):
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    repres = ELRepresentation(log)
    logsimple_set, T_set, sensitives_set = repres.simplify_LKC_without_time_set(sensitive)
    frequent_items_set = mfs.frequent_set_miner(T_set, k2 * len(T_set))
    print("frequent set", "\n", len(frequent_items_set))
    mvs = MVS(T_set, logsimple_set, sensitive, cont, sensitives_set, count=False, set=True)
    violating_set = mvs.mvs(l, k, c)
    print("violating set:", "\n", len(violating_set))
    l1.put(len(frequent_items_set))
    l2.put(len(violating_set))
    sup_set = repres.suppression(violating_set, frequent_items_set)
    T_set = repres.suppressT(logsimple_set, sup_set)
    log_set, d_set1, d_l_set1 = repres.createEventLog(T_set, spec)
    d_set.put(d_set1)
    d_l_set.put(d_l_set1)
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    net_set, initial_marking_set, final_marking_set = inductive_miner.apply(log_set)
    fitness_set.put(replay_factory.apply(log, net_set, initial_marking_set, final_marking_set)["log_fitness"])
    precision_set.put(precision_factory.apply(log, net_set, initial_marking_set, final_marking_set))

def set_dev(l, k, c, k2, l1, l2, d_set, d_l_set, fitness_set, precision_set,spec,contbound):
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    repres = ELRepresentation(log)
    logsimple_set, T_set, sensitives_set = repres.simplify_LKC_without_time_set(sensitive)
    frequent_items_set = mfs.frequent_set_miner(T_set, k2 * len(T_set))
    print("frequent set", "\n", len(frequent_items_set))
    mvs = MVS(T_set, logsimple_set, sensitive, cont, sensitives_set, count=False, set=True)
    violating_set = mvs.mvs(l, k, c,type="dev",contbound=contbound)
    print("violating set:", "\n", len(violating_set))
    l1.put(len(frequent_items_set))
    l2.put(len(violating_set))
    sup_set = repres.suppression(violating_set, frequent_items_set)
    T_set = repres.suppressT(logsimple_set, sup_set)
    log_set, d_set1, d_l_set1 = repres.createEventLog(T_set, spec)
    d_set.put(d_set1)
    d_l_set.put(d_l_set1)
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    net_set, initial_marking_set, final_marking_set = inductive_miner.apply(log_set)
    fitness_set.put(replay_factory.apply(log, net_set, initial_marking_set, final_marking_set)["log_fitness"])
    precision_set.put(precision_factory.apply(log, net_set, initial_marking_set, final_marking_set))



if __name__ == '__main__':

    ###SET###


    i=0
    for l in L:
        for c in C:
            for k in K:
                for k2 in K2:
                    for spec in spectime2:
                        i += 1
                        worksheet2.write_number(i, 0, l)
                        worksheet2.write_number(i, 1, k)
                        worksheet2.write_number(i, 2, c)
                        worksheet2.write_number(i, 3, k2)
                        worksheet2.write_string(i, 4, spec)
                        start = time.time()
                        try:
                            l1 = Queue()
                            l2 = Queue()
                            d_set = Queue()
                            d_l_set = Queue()
                            fitness_set = Queue()
                            precision_set = Queue()
                            p = Process(target=set, name="set", args=(l,k,c,k2,l1,l2,d_set,d_l_set,fitness_set,
                                                                      precision_set,spec))
                            p.start()
                            # Wait a maximum of 10 seconds for foo
                            # Usage: join([timeout in seconds])
                            p.join(timeout)

                            # If thread is active
                            if p.is_alive():
                                print("foo is running... let's kill it...")
                                worksheet2.write_string(i, 12, "TimedOut")
                                # Terminate foo
                                p.terminate()
                                p.join()
                                fitness_set.put(-1)
                                precision_set.put(-1)
                                l1.put(-1)
                                l2.put(-1)
                                d_set.put(-1)
                                d_l_set.put(-1)


                            worksheet2.write_number(i, 7, l1.get())
                            worksheet2.write_number(i, 8, l2.get())

                            worksheet2.write_number(i, 9, d_set.get())
                            worksheet2.write_number(i, 10, d_l_set.get())
                            #print("set", "\n", "fitness", fitness_set.get(), "\n", "precision", precision_set.get())
                            worksheet2.write_number(i, 5, fitness_set.get())
                            worksheet2.write_number(i, 6, precision_set.get())
                            finish1 = time.time()
                            t = finish1 - start
                            worksheet2.write_number(i, 11, t)
                        except Exception as e:
                            finish1 = time.time()
                            t = finish1 - start
                            worksheet2.write_number(i, 11, t)
                            worksheet2.write_string(i, 12, str(repr(e)))
                            print(e)

    worksheet = workbook2.add_worksheet("set dev")
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
                                d_set = Queue()
                                d_l_set = Queue()
                                fitness_set = Queue()
                                precision_set = Queue()
                                p = Process(target=set_dev, name="set_dev", args=(l, k, c, k2, l1, l2, d_set,
                                                                                  d_l_set, fitness_set,
                                                                                  precision_set,spec,contbound))
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
                                    fitness_set.put(-1)
                                    precision_set.put(-1)
                                    l1.put(-1)
                                    l2.put(-1)
                                    d_set.put(-1)
                                    d_l_set.put(-1)

                                worksheet.write_number(i, 8, l1.get())
                                worksheet.write_number(i, 9, l2.get())
                                worksheet.write_number(i, 10, d_set.get())
                                worksheet.write_number(i, 11, d_l_set.get())
                                #print("set", "\n", "fitness", fitness_set.get(), "\n", "precision", precision_set.get())
                                worksheet.write_number(i, 6, fitness_set.get())
                                worksheet.write_number(i, 7, precision_set.get())
                                finish1 = time.time()
                                t = finish1 - start
                                worksheet.write_number(i, 12 , t)
                            except Exception as e:
                                finish1 = time.time()
                                t = finish1 - start
                                worksheet.write_number(i, 12, t)
                                worksheet.write_string(i, 13, str(repr(e)))
                                print(e)

    workbook2.close()

