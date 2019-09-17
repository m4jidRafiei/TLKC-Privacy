import gc
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.algo.discovery.inductive import factory as inductive_miner
from pm4py.evaluation.replay_fitness import factory as replay_factory
from pm4py.evaluation.precision import factory as precision_factory
from pm4py.statistics.traces.tracelog import case_statistics
from ELRepresentation import ELRepresentation
from MFS import MFS
from MVS3 import MVS
import time
from multiprocessing import Process, Queue
import xlsxwriter

gc.collect()
timeout = 200
L = [2, 4]
C = [ 0.4, 0.8]
K = [ 40, 80]
#L,K,C
dict ={2: {40: {0.4:{"": {"w" : [], "x": [], "v" : []}}}}}
K2 = [0.7,  0.9]
sensitive = ['Age', 'Diagnose']
spectime2 = ["days", "minutes"]
cont = ['Age']
contbound2 = [{"Age":1}]#, {"Age": 2}]
#
log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")#, parameters={"max_no_traces_to_import": 1000})
var_with_count = case_statistics.get_variant_statistics(log)
activ_or = {""}
for el in var_with_count:
    el['variant'] = el['variant'].split(',')
    if len(el['variant']) == 1:
        activ_or.add(el['variant'])
    else:
        activ_or.update(el['variant'])
activ_or.remove("")
activ_or = len(activ_or)
variants_count = sum([1 for x in var_with_count])

# #print(log)
net, initial_marking, final_marking = inductive_miner.apply(log)
fitness = replay_factory.apply(log, net, initial_marking, final_marking)
precision = precision_factory.apply(log, net, initial_marking, final_marking)

workbook4 = xlsxwriter.Workbook('resultstime.xlsx')
worksheet4 = workbook4.add_worksheet("original")
worksheet4.write_string(0,0, "fitness")
worksheet4.write_string(0,1, "precision")
worksheet4.write_number(1,0,fitness["log_fitness"])
worksheet4.write_number(1,1,precision)
worksheet4.write_string(0,2, "variants")
worksheet4.write_number(1,2,variants_count)
worksheet4.write_string(0,3, "activities")
worksheet4.write_number(1,3,activ_or)
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
worksheet4.write_string(0,13, "variants")

worksheet4.write_string(0,14, "activities")


mfs = MFS()

def time2(l, k, c, k2, l1, l2, d_time, d_l_time, fitness_time, precision_time, spec,variants,activ_num):
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
    var_with_count = case_statistics.get_variant_statistics(log_time)
    activ_time = {""}
    for el in var_with_count:
        el['variant'] = el['variant'].split(',')
        activ_time.update(el['variant'])
    activ_time.remove("")
    activ_num.put(len(activ_time))
    variants.put(sum([1 for x in var_with_count]))


def time_dev(l, k, c, k2, l1, l2, d_time_dev, d_l_time_dev, fitness_time, precision_time, spec, contbound,activ_num, variants):
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
    var_with_count = case_statistics.get_variant_statistics(log_time_dev)
    activ_time = {""}
    for el in var_with_count:
        el['variant'] = el['variant'].split(',')
        if len(el['variant']) == 1:
            activ_time.add(el['variant'])
        else:
            activ_time.update(el['variant'])
    activ_time.remove("")
    activ_num.put(len(activ_time))
    variants.put(sum([1 for x in var_with_count]))
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
                            variants = Queue()
                            activ_num = Queue()
                            p = Process(target=time2, name="time2", args=(l, k, c, k2, l1, l2,
                                                                          d_time, d_l_time,
                                                                          fitness_time, precision_time, spec,variants,activ_num))
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
                                variants.put(-1)
                                activ_num.put(-1)

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
                            worksheet4.write_number(i,13,variants.get())
                            worksheet4.write_number(i,14,activ_num.get())
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
    worksheet.write_string(0, 14,"variants")
    worksheet.write_string(0,15, "activities")




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
                                variants = Queue()
                                activ_num = Queue()
                                p = Process(target=time_dev, name="time_dev", args=(l, k, c, k2, l1, l2, d_time_dev,
                                                                                    d_l_time_dev, fitness_time,
                                                                                    precision_time, spec, contbound,
                                                                                    activ_num, variants))
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
                                    variants.put(-1)
                                    activ_num.put(-1)

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
                                worksheet.write_number(i, 14, variants.get())
                                worksheet.write_number(i, 15, activ_num.get())
                            except Exception as e:
                                finish1 = time.time()
                                t = finish1 - start
                                worksheet.write_number(i, 12, t)
                                worksheet.write_string(i, 13, str(repr(e)))
                                print(e)

    workbook4.close()
