

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
from MVS3 import MVS
import time
import xlsxwriter
gc.collect()
timeout = 4000
L = [2, 4]
C = [0.4]
K = [40]
K2 = [0.6]
sensitive = ['Age', 'Diagnose']
spectime2 = ["hours"]
cont = ['Age']
contbound2 = [{"Age":1}]#, {"Age": 2}]
dict1 ={2: {40: {0.4:{None: {"w" : [], "x": [], "v" : []}, "dev": {"w" : [], "x": [], "v" : []}},
                0.8: {None:{"w" : [], "x": [], "v" : []}, "dev": {"w" : [], "x": [], "v" : []}}},
           80: {0.4:{None: {"w" : [], "x": [], "v" : []}, "dev": {"w" : [], "x": [], "v" : []}}
               , 0.8: {None:{"w" : [], "x": [], "v" : []}, "dev": {"w" : [], "x": [], "v" : []}}}},
      4: {40: {0.4:{None: {"w" : [], "x": [], "v" : []}, "dev": {"w" : [], "x": [], "v" : []}}
             , 0.8: {None:{"w" : [], "x": [], "v" : []}, "dev": {"w" : [], "x": [], "v" : []}}},
           80: {0.4:{None: {"w" : [], "x": [], "v" : []}, "dev": {"w" : [], "x": [], "v" : []}}
               , 0.8: {None:{"w" : [], "x": [], "v" : []}, "dev": {"w" : [], "x": [], "v" : []}}}}}
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
workbook = xlsxwriter.Workbook('resultscounttest.xlsx')
# worksheet = workbook.add_worksheet("original")
# worksheet.write_string(0,0, "fitness")
# worksheet.write_string(0,1, "precision")
# worksheet.write_number(1,0,fitness["log_fitness"])
# worksheet.write_number(1,1,precision)
# worksheet.write_string(0,2, "variants")
# worksheet.write_number(1,2,variants_count)
# worksheet.write_string(0,3, "activities")
# worksheet.write_number(1,3,activ_or)
# worksheet.write_string(0,4,"alignment fitness")
# worksheet.write_number(1,4,log_fitness["percFitTraces"])
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
worksheet.write_string(0,13, "variants")
worksheet.write_string(0,14, "activities")
worksheet.write_string(0,15,"alignment fitness")


mfs = MFS()


def count(l, k, c, k2, spec,dict1):
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    repres = ELRepresentation(log)
    logsimple_count, T_count, sensitives_count = repres.simplify_LKC_without_time_count(
        sensitive)
    frequent_count = mfs.frequent_seq_activity(T_count, k2 * len(T_count))
    print("frequent count", "\n", len(frequent_count))
    mvs = MVS(T_count, logsimple_count, sensitive, cont, sensitives_count, True,dict_safe=dict1)
    violating_count, dict1 = mvs.mvs(l, k, c)
    print("violating count:", "\n", len(violating_count))
    l1 = len(frequent_count)
    l2 = len(violating_count)
    sup_count = repres.suppression(violating_count, frequent_count)
    T_count = repres.suppressT(logsimple_count, sup_count)
    log_count, d_count, d_l_count = repres.createEventLog(T_count, spec)
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    net_count, initial_marking_count, final_marking_count = inductive_miner.apply(log_count)
    fitness_count = replay_factory.apply(log, net_count, initial_marking_count,
                                         final_marking_count)["log_fitness"]
    precision_count = precision_factory.apply(log, net_count, initial_marking_count,
                                              final_marking_count)
    alignments = align_factory.apply_log(log, net_count, initial_marking_count, final_marking_count)
    log_fitness = replay_fitness_factory.evaluate(alignments, variant="alignments")
    fit_al = log_fitness["percFitTraces"]
    var_with_count = case_statistics.get_variant_statistics(log_count)
    activ_time = {""}
    for el in var_with_count:
        el['variant'] = el['variant'].split(',')
        activ_time.update(el['variant'])
    activ_time.remove("")
    activ  = len(activ_time)
    variants = sum([1 for x in var_with_count])
    return l1, l2, d_count, d_l_count, fitness_count, precision_count, fit_al, activ, variants, dict1

def count_dev(l, k, c, k2,spec,contbound, dict1):
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    repres = ELRepresentation(log)
    logsimple_count, T_count, sensitives_count = repres.simplify_LKC_without_time_count(
                sensitive)
    frequent_count = mfs.frequent_seq_activity(T_count, k2 * len(T_count))
    print("frequent count", "\n", len(frequent_count))
    mvs = MVS(T_count, logsimple_count, sensitive, cont, sensitives_count, True, dict_safe=dict1)
    violating_count, dict1 = mvs.mvs(l, k, c,type="dev",contbound=contbound)
    print("violating count:", "\n", len(violating_count))
    l1 = len(frequent_count)
    l2 = len(violating_count)
    sup_count = repres.suppression(violating_count, frequent_count)
    T_count = repres.suppressT(logsimple_count, sup_count)
    log_count, d_count, d_l_count = repres.createEventLog(T_count, spec)
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    net_count, initial_marking_count, final_marking_count = inductive_miner.apply(log_count)
    fitness_count = replay_factory.apply(log, net_count, initial_marking_count,
                                                 final_marking_count)["log_fitness"]
    precision_count = precision_factory.apply(log, net_count, initial_marking_count,
                                                      final_marking_count)
    alignments = align_factory.apply_log(log, net_count, initial_marking_count, final_marking_count)
    log_fitness = replay_fitness_factory.evaluate(alignments, variant="alignments")
    fit_al = log_fitness["percFitTraces"]
    var_with_count = case_statistics.get_variant_statistics(log_count)
    activ_time = {""}
    for el in var_with_count:
        el['variant'] = el['variant'].split(',')
        activ_time.update(el['variant'])
    activ_time.remove("")
    activ = len(activ_time)
    variants = sum([1 for x in var_with_count])
    return l1, l2, d_count, d_l_count, fitness_count, precision_count, fit_al,activ, variants, dict1

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
                            l1, l2, d_count,d_l_count, fitness_count, precision_count, fit_al, activ, variants,dict1 = count(l,k,c,k2, spec,dict1)


                            worksheet.write_number(i, 7, l1)
                            worksheet.write_number(i, 8, l2)
                            worksheet.write_number(i, 9, d_count)
                            worksheet.write_number(i, 10, d_l_count)
                            #print("count", "\n", "fitness", fitness_count.get(), "\n", "precision", precision_count.get())
                            worksheet.write_number(i, 5, fitness_count)
                            worksheet.write_number(i, 6, precision_count)
                            worksheet.write_number(i, 13, variants)
                            worksheet.write_number(i, 14, activ)
                            worksheet.write_number(i, 15, fit_al)
                            finish1 = time.time()
                            t = finish1 - start
                            worksheet.write_number(i, 11, t)
                        except Exception as e:
                            finish1 = time.time()
                            t = finish1 - start
                            worksheet.write_number(i, 11, t)
                            worksheet.write_string(i, 12, str(repr(e)))
                            print(e)

    worksheet = workbook.add_worksheet("count dev")
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
    worksheet.write_string(0, 13, "variants")
    worksheet.write_string(0, 14, "activities")
    worksheet.write_string(0, 15, "alignment fitness")

    mfs = MFS()




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
                                l1, l2, d_count, d_l_count, fitness_count, precision_count, fit_al,activ, variants, dict1 = count_dev(l, k, c, k2, spec, contbound,dict1)

                                worksheet.write_number(i, 8, l1)
                                worksheet.write_number(i, 9, l2)
                                worksheet.write_number(i, 10, d_count)
                                worksheet.write_number(i, 11, d_l_count)
                                worksheet.write_number(i, 6, fitness_count)
                                worksheet.write_number(i, 7, precision_count)
                                worksheet.write_number(i, 14, variants)
                                worksheet.write_number(i, 15, activ)
                                worksheet.write_number(i, 16, fit_al)
                                finish1 = time.time()
                                t = finish1 - start
                                worksheet.write_number(i, 12 , t)
                            except Exception as e:
                                finish1 = time.time()
                                t = finish1 - start
                                worksheet.write_number(i, 12, t)
                                worksheet.write_string(i, 13, str(repr(e)))
                                print(e)
    print(dict1)
    workbook.close()