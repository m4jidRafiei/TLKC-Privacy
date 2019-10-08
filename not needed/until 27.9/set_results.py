import gc
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.algo.discovery.inductive import factory as inductive_miner
from pm4py.evaluation.replay_fitness import factory as replay_factory
from pm4py.evaluation.precision import factory as precision_factory
from pm4py.statistics.traces.tracelog import case_statistics
from pm4py.evaluation.replay_fitness import factory as replay_fitness_factory
from pm4py.algo.conformance.alignments import factory as align_factory
from ELRepresentation import ELRepresentation
from MFS import MFS
from MVS import MVS
import time
from multiprocessing import Process, Queue
import xlsxwriter
gc.collect()
timeout = 20000
L = [2, 4]
C = [0.4, 0.8]
K = [40, 80]
K2 = [0.7 ,0.9]
sensitive = ['Age', 'Diagnose']
spectime2 = ["hours","minutes"]#["days", "minutes"]
cont = ['Age']
contbound2 = [{"Age":1}]#, {"Age": 2}]
#
# log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")#, parameters={"max_no_traces_to_import": 1000})
# var_with_count = case_statistics.get_variant_statistics(log)
# activ_or = {""}
# for el in var_with_count:
#     el['variant'] = el['variant'].split(',')
#     activ_or.update(el['variant'])
# activ_or.remove("")
# activ_or = len(activ_or)
# variants_count = sum([1 for x in var_with_count])
# # #print(log)
# net, initial_marking, final_marking = inductive_miner.apply(log)
# fitness = replay_factory.apply(log, net, initial_marking, final_marking)
# precision = precision_factory.apply(log, net, initial_marking, final_marking)
# alignments = align_factory.apply_log(log, net, initial_marking, final_marking)
# log_fitness = replay_fitness_factory.evaluate(alignments, variant="alignments")
workbook2 = xlsxwriter.Workbook('resultsset2.xlsx')
# worksheet2 = workbook2.add_worksheet("original")
# worksheet2.write_string(0,0, "fitness")
# worksheet2.write_string(0,1, "precision")
# worksheet2.write_number(1,0,fitness["log_fitness"])
# worksheet2.write_number(1,1,precision)
# worksheet2.write_string(0,2, "variants")
# worksheet2.write_number(1,2,variants_count)
# worksheet2.write_string(0,3, "activities")
# worksheet2.write_number(1,3,activ_or)
# worksheet2.write_string(0,4,"alignment fitness")
# worksheet2.write_number(1,4,log_fitness["percFitTraces"])
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
worksheet2.write_string(0,13, "variants")
worksheet2.write_string(0,14, "activities")
worksheet2.write_string(0,15,"alignment fitness")



mfs = MFS()


def set1(l, k, c, k2, l1, l2, d_set, d_l_set, fitness_set, precision_set, spec,fit_al,activ,variants):
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    repres = ELRepresentation(log)
    logsimple_set, T_set, sensitives_set = repres.simplify_LKC_without_time_set(sensitive)
    frequent_items_set = mfs.frequent_set_miner(T_set, k2)
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
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    net_set, initial_marking_set, final_marking_set = inductive_miner.apply(log_set)
    fitness_set.put(replay_factory.apply(log, net_set, initial_marking_set, final_marking_set)["log_fitness"])
    precision_set.put(precision_factory.apply(log, net_set, initial_marking_set, final_marking_set))
    alignments = align_factory.apply_log(log, net_set, initial_marking_set, final_marking_set)
    log_fitness = replay_fitness_factory.evaluate(alignments, variant="alignments")
    fit_al.put(log_fitness["percFitTraces"])
    var_with_count = case_statistics.get_variant_statistics(log_set)
    activ_time = {""}
    for el in var_with_count:
        el['variant'] = el['variant'].split(',')
        activ_time.update(el['variant'])
    activ_time.remove("")
    activ.put(len(activ_time))
    variants.put(sum([1 for x in var_with_count]))

def set_dev(l, k, c, k2, l1, l2, d_set, d_l_set, fitness_set, precision_set,spec,contbound,fit_al,activ,variants):
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    repres = ELRepresentation(log)
    logsimple_set, T_set, sensitives_set = repres.simplify_LKC_without_time_set(sensitive)
    frequent_items_set = mfs.frequent_set_miner(T_set, k2)
    print("frequent set", "\n", len(frequent_items_set))
    mvs = MVS(T_set, logsimple_set, sensitive, cont, sensitives_set, count=False, set1=True)
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
    alignments = align_factory.apply_log(log, net_set, initial_marking_set, final_marking_set)
    log_fitness = replay_fitness_factory.evaluate(alignments, variant="alignments")
    fit_al.put(log_fitness["percFitTraces"])
    var_with_count = case_statistics.get_variant_statistics(log_set)
    activ_time = {""}
    for el in var_with_count:
        el['variant'] = el['variant'].split(',')
        activ_time.update(el['variant'])
    activ_time.remove("")
    activ.put(len(activ_time))
    variants.put(sum([1 for x in var_with_count]))



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
                            fit_al = Queue()
                            activ = Queue()
                            variants = Queue()
                            p = Process(target=set1, name="set1", args=(l,k,c,k2,l1,l2,d_set,d_l_set,fitness_set,
                                                                      precision_set,spec,fit_al,activ,variants))
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
                                fit_al.put(-1)
                                activ.put(-1)
                                variants.put(-1)


                            worksheet2.write_number(i, 7, l1.get())
                            worksheet2.write_number(i, 8, l2.get())

                            worksheet2.write_number(i, 9, d_set.get())
                            worksheet2.write_number(i, 10, d_l_set.get())
                            #print("set", "\n", "fitness", fitness_set.get(), "\n", "precision", precision_set.get())
                            worksheet2.write_number(i, 5, fitness_set.get())
                            worksheet2.write_number(i, 6, precision_set.get())
                            worksheet2.write_number(i, 13, variants.get())
                            worksheet2.write_number(i, 14, activ.get())
                            worksheet2.write_number(i, 15, fit_al.get())
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
    worksheet.write_string(0, 14, "variants")
    worksheet.write_string(0, 15, "activities")
    worksheet.write_string(0, 16, "alignment fitness")




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
                                variants = Queue()
                                fit_al = Queue()
                                activ = Queue()
                                p = Process(target=set_dev, name="set_dev", args=(l, k, c, k2, l1, l2, d_set,
                                                                                  d_l_set, fitness_set,
                                                                                  precision_set,spec,contbound,fit_al,
                                                                                  activ,variants))
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
                                    variants.put(-1)
                                    fit_al.put(-1)
                                    activ.put(-1)

                                worksheet.write_number(i, 8, l1.get())
                                worksheet.write_number(i, 9, l2.get())
                                worksheet.write_number(i, 10, d_set.get())
                                worksheet.write_number(i, 11, d_l_set.get())
                                #print("set", "\n", "fitness", fitness_set.get(), "\n", "precision", precision_set.get())
                                worksheet.write_number(i, 6, fitness_set.get())
                                worksheet.write_number(i, 7, precision_set.get())
                                worksheet.write_number(i, 14, variants.get())
                                worksheet.write_number(i, 15, activ.get())
                                worksheet.write_number(i, 16, fit_al.get())
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
