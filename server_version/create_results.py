import gc
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from server_version import Annonymizer
from server_version import Results
import time
import xlsxwriter

gc.collect()

annonymizer = Annonymizer.Annonymizer()
results = Results.Results()

L = [1, 2, 3]
C = [0.4, 0.8]
K = [80]
K2 = [0.7]#,  0.9]
sensitive = ['Age', 'Diagnose']
spectime2 = ["minutes"]#, "minutes"]
cont = ['Age']

contbound2 = [{"Age":1}]#, {"Age": 2}]
dict1 = {l: {k: {c: {t: {"w": [],"x": [], "v": []} for t in spectime2} for c in C}for k in K}
             for l in range(0, L[len(L)-1])}
# for l in L:
#     i = 0
#     workbook = xlsxwriter.Workbook('set' + str(l) + '.xlsx')
#     worksheet = workbook.add_worksheet("set")
#     worksheet.write_string(0, 0, "L")
#     worksheet.write_string(0, 1, "K")
#     worksheet.write_string(0, 2, "C")
#     worksheet.write_string(0, 3, "K'")
#     worksheet.write_string(0, 4, "t")
#     worksheet.write_string(0, 5, "fitness")
#     worksheet.write_string(0, 6, "alignment fitness")
#     worksheet.write_string(0, 7, "perc fit traces")
#     worksheet.write_string(0, 8, "precision")
#     worksheet.write_string(0, 9, "len frequent")
#     worksheet.write_string(0, 10, "len violating")
#     worksheet.write_string(0, 11, "deleted elements")
#     worksheet.write_string(0, 12, "deleted traces")
#     worksheet.write_string(0, 13, "variants")
#     worksheet.write_string(0, 14, "number of activities")
#     worksheet.write_string(0, 15, "time")
#     worksheet.write_string(0, 16, "error")
#     worksheet.write_string(0, 17, "activities")
#
#     for k2 in K2:
#         for k in K:
#             for c in C:
#                 for t in spectime2:
#                     i += 1
#                     worksheet.write_number(i, 0, l)
#                     worksheet.write_number(i, 1, k)
#                     worksheet.write_number(i, 2, c)
#                     worksheet.write_number(i, 3, k2)
#                     worksheet.write_string(i, 4, t)
#                     start = time.time()
#                     try:
#                         log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
#
#                         log_count, frequent_length, violating_length, d, d_l, dict2 = \
#                             annonymizer.set1(log, sensitive,cont,t,l,k,c,k2,dict1)
#                         finish1 = time.time()
#                         dict1 = dict2
#                         worksheet.write_number(i, 9, frequent_length)
#                         worksheet.write_number(i, 10, violating_length)
#                         worksheet.write_number(i, 11, d)
#                         worksheet.write_number(i, 12, d_l)
#                         worktime = finish1 - start
#                         worksheet.write_number(i, 15, worktime)
#                         log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
#                         fitness, precision, perc_fit_tr, average_fitness, activ, variants, activ1 =results.results_log(log_count, log)
#                         worksheet.write_number(i, 5, fitness)
#                         worksheet.write_number(i, 6, average_fitness)
#                         worksheet.write_number(i, 7, perc_fit_tr)
#                         worksheet.write_number(i, 8, precision)
#                         worksheet.write_number(i, 13, variants)
#                         worksheet.write_number(i, 14, activ)
#                         print(activ1)
#                         worksheet.write_string(i, 17, " ".join(activ1))
#                         print("done")
#                     except Exception as e:
#                         finish1 = time.time()
#                         worktime = finish1 - start
#                         worksheet.write_number(i, 15, worktime)
#                         worksheet.write_string(i, 16, str(repr(e)))
#                         print(e)
#     workbook.close()
#
# ##set_count
# dict1 = {l: {k: {c: {t: {"w": [],"x": [], "v": []} for t in spectime2} for c in C}for k in K}
#              for l in range(0, L[len(L)-1])}
# for l in L:
#     i = 0
#     workbook = xlsxwriter.Workbook('set_count' + str(l) + '.xlsx')
#     worksheet = workbook.add_worksheet("set_count")
#     worksheet.write_string(0, 0, "L")
#     worksheet.write_string(0, 1, "K")
#     worksheet.write_string(0, 2, "C")
#     worksheet.write_string(0, 3, "K'")
#     worksheet.write_string(0, 4, "t")
#     worksheet.write_string(0, 5, "fitness")
#     worksheet.write_string(0, 6, "alignment fitness")
#     worksheet.write_string(0, 7, "perc fit traces")
#     worksheet.write_string(0, 8, "precision")
#     worksheet.write_string(0, 9, "len frequent")
#     worksheet.write_string(0, 10, "len violating")
#     worksheet.write_string(0, 11, "deleted elements")
#     worksheet.write_string(0, 12, "deleted traces")
#     worksheet.write_string(0, 13, "variants")
#     worksheet.write_string(0, 14, "number of activities")
#     worksheet.write_string(0, 15, "time")
#     worksheet.write_string(0, 16, "error")
#     worksheet.write_string(0, 17, "activities")
#
#     for k2 in K2:
#         for k in K:
#             for c in C:
#                 for t in spectime2:
#                     i += 1
#                     worksheet.write_number(i, 0, l)
#                     worksheet.write_number(i, 1, k)
#                     worksheet.write_number(i, 2, c)
#                     worksheet.write_number(i, 3, k2)
#                     worksheet.write_string(i, 4, t)
#                     start = time.time()
#                     try:
#                         log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
#
#                         log_count, frequent_length, violating_length, d, d_l, dict2 = \
#                             annonymizer.set_count(log, sensitive,cont,t,l,k,c,k2,dict1)
#                         finish1 = time.time()
#                         dict1 = dict2
#                         worksheet.write_number(i, 9, frequent_length)
#                         worksheet.write_number(i, 10, violating_length)
#                         worksheet.write_number(i, 11, d)
#                         worksheet.write_number(i, 12, d_l)
#                         worktime = finish1 - start
#                         worksheet.write_number(i, 15, worktime)
#                         log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
#                         fitness, precision, perc_fit_tr, average_fitness, activ, variants, activ1 =results.results_log(log_count, log)
#                         worksheet.write_number(i, 5, fitness)
#                         worksheet.write_number(i, 6, average_fitness)
#                         worksheet.write_number(i, 7, perc_fit_tr)
#                         worksheet.write_number(i, 8, precision)
#                         worksheet.write_number(i, 13, variants)
#                         worksheet.write_number(i, 14, activ)
#                         print(activ1)
#                         worksheet.write_string(i, 17, " ".join(activ1))
#                         print("done")
#                     except Exception as e:
#                         finish1 = time.time()
#                         worktime = finish1 - start
#                         worksheet.write_number(i, 15, worktime)
#                         worksheet.write_string(i, 16, str(repr(e)))
#                         print(e)
#     workbook.close()
#
# dict1 = {l: {k: {c: {t: {"w": [],"x": [], "v": []} for t in spectime2} for c in C}for k in K}
#              for l in range(0, L[len(L)-1])}
# for l in L:
#     i = 0
#     workbook = xlsxwriter.Workbook('time' + str(l) + '.xlsx')
#     worksheet = workbook.add_worksheet("time")
#     worksheet.write_string(0, 0, "L")
#     worksheet.write_string(0, 1, "K")
#     worksheet.write_string(0, 2, "C")
#     worksheet.write_string(0, 3, "K'")
#     worksheet.write_string(0, 4, "t")
#     worksheet.write_string(0, 5, "fitness")
#     worksheet.write_string(0, 6, "alignment fitness")
#     worksheet.write_string(0, 7, "perc fit traces")
#     worksheet.write_string(0, 8, "precision")
#     worksheet.write_string(0, 9, "len frequent")
#     worksheet.write_string(0, 10, "len violating")
#     worksheet.write_string(0, 11, "deleted elements")
#     worksheet.write_string(0, 12, "deleted traces")
#     worksheet.write_string(0, 13, "variants")
#     worksheet.write_string(0, 14, "number of activities")
#     worksheet.write_string(0, 15, "time")
#     worksheet.write_string(0, 16, "error")
#     worksheet.write_string(0, 17, "activities")
#
#     for k2 in K2:
#         for k in K:
#             for c in C:
#                 for t in spectime2:
#                     i += 1
#                     worksheet.write_number(i, 0, l)
#                     worksheet.write_number(i, 1, k)
#                     worksheet.write_number(i, 2, c)
#                     worksheet.write_number(i, 3, k2)
#                     worksheet.write_string(i, 4, t)
#                     start = time.time()
#                     try:
#                         log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
#
#                         log_count, frequent_length, violating_length, d, d_l, dict2 = \
#                             annonymizer.time2(log, sensitive,cont,t,l,k,c,k2,dict1)
#                         finish1 = time.time()
#                         dict1 = dict2
#                         worksheet.write_number(i, 9, frequent_length)
#                         worksheet.write_number(i, 10, violating_length)
#                         worksheet.write_number(i, 11, d)
#                         worksheet.write_number(i, 12, d_l)
#                         worktime = finish1 - start
#                         worksheet.write_number(i, 15, worktime)
#                         log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
#                         fitness, precision, perc_fit_tr, average_fitness, activ, variants, activ1 =results.results_log(log_count, log)
#                         worksheet.write_number(i, 5, fitness)
#                         worksheet.write_number(i, 6, average_fitness)
#                         worksheet.write_number(i, 7, perc_fit_tr)
#                         worksheet.write_number(i, 8, precision)
#                         worksheet.write_number(i, 13, variants)
#                         worksheet.write_number(i, 14, activ)
#                         print(activ1)
#                         worksheet.write_string(i, 17, " ".join(activ1))
#                         print("done")
#                     except Exception as e:
#                         finish1 = time.time()
#                         worktime = finish1 - start
#                         worksheet.write_number(i, 15, worktime)
#                         worksheet.write_string(i, 16, str(repr(e)))
#                         print(e)
#     workbook.close()
#
# dict1 = {l: {k: {c: {t: {"w": [],"x": [], "v": []} for t in spectime2} for c in C}for k in K}
#              for l in range(0, L[len(L)-1])}
# for l in L:
#     i = 0
#     workbook = xlsxwriter.Workbook('count' + str(l) + '.xlsx')
#     worksheet = workbook.add_worksheet("count")
#     worksheet.write_string(0, 0, "L")
#     worksheet.write_string(0, 1, "K")
#     worksheet.write_string(0, 2, "C")
#     worksheet.write_string(0, 3, "K'")
#     worksheet.write_string(0, 4, "t")
#     worksheet.write_string(0, 5, "fitness")
#     worksheet.write_string(0, 6, "alignment fitness")
#     worksheet.write_string(0, 7, "perc fit traces")
#     worksheet.write_string(0, 8, "precision")
#     worksheet.write_string(0, 9, "len frequent")
#     worksheet.write_string(0, 10, "len violating")
#     worksheet.write_string(0, 11, "deleted elements")
#     worksheet.write_string(0, 12, "deleted traces")
#     worksheet.write_string(0, 13, "variants")
#     worksheet.write_string(0, 14, "number of activities")
#     worksheet.write_string(0, 15, "time")
#     worksheet.write_string(0, 16, "error")
#     worksheet.write_string(0, 17, "activities")
#
#     for k2 in K2:
#         for k in K:
#             for c in C:
#                 for t in spectime2:
#                     i += 1
#                     worksheet.write_number(i, 0, l)
#                     worksheet.write_number(i, 1, k)
#                     worksheet.write_number(i, 2, c)
#                     worksheet.write_number(i, 3, k2)
#                     worksheet.write_string(i, 4, t)
#                     start = time.time()
#                     try:
#                         log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
#
#                         log_count, frequent_length, violating_length, d, d_l, dict2 = \
#                             annonymizer.count(log, sensitive,cont,t,l,k,c,k2,dict1)
#                         finish1 = time.time()
#                         dict1 = dict2
#                         worksheet.write_number(i, 9, frequent_length)
#                         worksheet.write_number(i, 10, violating_length)
#                         worksheet.write_number(i, 11, d)
#                         worksheet.write_number(i, 12, d_l)
#                         worktime = finish1 - start
#                         worksheet.write_number(i, 15, worktime)
#                         log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
#                         fitness, precision, perc_fit_tr, average_fitness, activ, variants, activ1 =results.results_log(log_count, log)
#                         worksheet.write_number(i, 5, fitness)
#                         worksheet.write_number(i, 6, average_fitness)
#                         worksheet.write_number(i, 7, perc_fit_tr)
#                         worksheet.write_number(i, 8, precision)
#                         worksheet.write_number(i, 13, variants)
#                         worksheet.write_number(i, 14, activ)
#                         print(activ1)
#                         worksheet.write_string(i, 17, " ".join(activ1))
#                         print("done")
#                     except Exception as e:
#                         finish1 = time.time()
#                         worktime = finish1 - start
#                         worksheet.write_number(i, 15, worktime)
#                         worksheet.write_string(i, 16, str(repr(e)))
#                         print(e)
#     workbook.close()

dict1 = {l: {k: {c: {t: {bound["Age"]: {"w": [],"x": [], "v": []} for bound in contbound2} for t in spectime2} for c in C}for k in K}
             for l in range(0, L[len(L)-1])}
for l in L:
    i = 0
    workbook = xlsxwriter.Workbook('set_dev' + str(l) + '.xlsx')
    worksheet = workbook.add_worksheet("set")
    worksheet.write_string(0, 0, "L")
    worksheet.write_string(0, 1, "K")
    worksheet.write_string(0, 2, "C")
    worksheet.write_string(0, 3, "K'")
    worksheet.write_string(0, 4, "t")
    worksheet.write_string(0, 5, "fitness")
    worksheet.write_string(0, 6, "alignment fitness")
    worksheet.write_string(0, 7, "perc fit traces")
    worksheet.write_string(0, 8, "precision")
    worksheet.write_string(0, 9, "len frequent")
    worksheet.write_string(0, 10, "len violating")
    worksheet.write_string(0, 11, "deleted elements")
    worksheet.write_string(0, 12, "deleted traces")
    worksheet.write_string(0, 13, "variants")
    worksheet.write_string(0, 14, "number of activities")
    worksheet.write_string(0, 15, "time")
    worksheet.write_string(0, 16, "error")
    worksheet.write_string(0, 17, "activities")
    worksheet.write_string(0, 18, "contbound")

    for k2 in K2:
        for k in K:
            for c in C:
                for t in spectime2:
                    for bound in contbound2:
                        i += 1
                        worksheet.write_number(i, 0, l)
                        worksheet.write_number(i, 1, k)
                        worksheet.write_number(i, 2, c)
                        worksheet.write_number(i, 3, k2)
                        worksheet.write_string(i, 4, t)
                        worksheet.write_number(i, 18, bound["Age"])
                        start = time.time()
                        try:
                            log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")

                            log_count, frequent_length, violating_length, d, d_l, dict2 = \
                                annonymizer.set_dev(log, sensitive,cont,t,l,k,c,k2,bound,dict1)
                            finish1 = time.time()
                            dict1 = dict2
                            worksheet.write_number(i, 9, frequent_length)
                            worksheet.write_number(i, 10, violating_length)
                            worksheet.write_number(i, 11, d)
                            worksheet.write_number(i, 12, d_l)
                            worktime = finish1 - start
                            worksheet.write_number(i, 15, worktime)
                            log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
                            fitness, precision, perc_fit_tr, average_fitness, activ, variants, activ1 =results.results_log(log_count, log)
                            worksheet.write_number(i, 5, fitness)
                            worksheet.write_number(i, 6, average_fitness)
                            worksheet.write_number(i, 7, perc_fit_tr)
                            worksheet.write_number(i, 8, precision)
                            worksheet.write_number(i, 13, variants)
                            worksheet.write_number(i, 14, activ)
                            print(activ1)
                            worksheet.write_string(i, 17, " ".join(activ1))
                            print("done")
                        except Exception as e:
                            finish1 = time.time()
                            worktime = finish1 - start
                            worksheet.write_number(i, 15, worktime)
                            worksheet.write_string(i, 16, str(repr(e)))
                            print(e)
    workbook.close()

dict1 = {l: {k: {c: {t: {bound["Age"]: {"w": [],"x": [], "v": []} for bound in contbound2} for t in spectime2} for c in C}for k in K}
             for l in range(0, L[len(L)-1])}
for l in L:
    i = 0
    workbook = xlsxwriter.Workbook('set_count_dev' + str(l) + '.xlsx')
    worksheet = workbook.add_worksheet("set_count")
    worksheet.write_string(0, 0, "L")
    worksheet.write_string(0, 1, "K")
    worksheet.write_string(0, 2, "C")
    worksheet.write_string(0, 3, "K'")
    worksheet.write_string(0, 4, "t")
    worksheet.write_string(0, 5, "fitness")
    worksheet.write_string(0, 6, "alignment fitness")
    worksheet.write_string(0, 7, "perc fit traces")
    worksheet.write_string(0, 8, "precision")
    worksheet.write_string(0, 9, "len frequent")
    worksheet.write_string(0, 10, "len violating")
    worksheet.write_string(0, 11, "deleted elements")
    worksheet.write_string(0, 12, "deleted traces")
    worksheet.write_string(0, 13, "variants")
    worksheet.write_string(0, 14, "number of activities")
    worksheet.write_string(0, 15, "time")
    worksheet.write_string(0, 16, "error")
    worksheet.write_string(0, 17, "activities")
    worksheet.write_string(0, 18, "contbound")

    for k2 in K2:
        for k in K:
            for c in C:
                for t in spectime2:
                    for bound in contbound2:
                        i += 1
                        worksheet.write_number(i, 0, l)
                        worksheet.write_number(i, 1, k)
                        worksheet.write_number(i, 2, c)
                        worksheet.write_number(i, 3, k2)
                        worksheet.write_string(i, 4, t)
                        worksheet.write_number(i, 18, bound["Age"])
                        start = time.time()
                        try:
                            log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")

                            log_count, frequent_length, violating_length, d, d_l, dict2 = \
                                annonymizer.set_count_dev(log, sensitive, cont, t, l, k, c, k2, bound, dict1)
                            finish1 = time.time()
                            dict1 = dict2
                            worksheet.write_number(i, 9, frequent_length)
                            worksheet.write_number(i, 10, violating_length)
                            worksheet.write_number(i, 11, d)
                            worksheet.write_number(i, 12, d_l)
                            worktime = finish1 - start
                            worksheet.write_number(i, 15, worktime)
                            log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
                            fitness, precision, perc_fit_tr, average_fitness, activ, variants, activ1 = results.results_log(
                                log_count, log)
                            worksheet.write_number(i, 5, fitness)
                            worksheet.write_number(i, 6, average_fitness)
                            worksheet.write_number(i, 7, perc_fit_tr)
                            worksheet.write_number(i, 8, precision)
                            worksheet.write_number(i, 13, variants)
                            worksheet.write_number(i, 14, activ)
                            print(activ1)
                            worksheet.write_string(i, 17, " ".join(activ1))
                            print("done")
                        except Exception as e:
                            finish1 = time.time()
                            worktime = finish1 - start
                            worksheet.write_number(i, 15, worktime)
                            worksheet.write_string(i, 16, str(repr(e)))
                            print(e)
    workbook.close()

dict1 = {l: {k: {c: {t: {bound["Age"]: {"w": [],"x": [], "v": []} for bound in contbound2} for t in spectime2} for c in C}for k in K}
             for l in range(0, L[len(L)-1])}
for l in L:
    i = 0
    workbook = xlsxwriter.Workbook('time_dev' + str(l) + '.xlsx')
    worksheet = workbook.add_worksheet("time")
    worksheet.write_string(0, 0, "L")
    worksheet.write_string(0, 1, "K")
    worksheet.write_string(0, 2, "C")
    worksheet.write_string(0, 3, "K'")
    worksheet.write_string(0, 4, "t")
    worksheet.write_string(0, 5, "fitness")
    worksheet.write_string(0, 6, "alignment fitness")
    worksheet.write_string(0, 7, "perc fit traces")
    worksheet.write_string(0, 8, "precision")
    worksheet.write_string(0, 9, "len frequent")
    worksheet.write_string(0, 10, "len violating")
    worksheet.write_string(0, 11, "deleted elements")
    worksheet.write_string(0, 12, "deleted traces")
    worksheet.write_string(0, 13, "variants")
    worksheet.write_string(0, 14, "number of activities")
    worksheet.write_string(0, 15, "time")
    worksheet.write_string(0, 16, "error")
    worksheet.write_string(0, 17, "activities")
    worksheet.write_string(0, 18, "contbound")

    for k2 in K2:
        for k in K:
            for c in C:
                for t in spectime2:
                    for bound in contbound2:
                        i += 1
                        worksheet.write_number(i, 0, l)
                        worksheet.write_number(i, 1, k)
                        worksheet.write_number(i, 2, c)
                        worksheet.write_number(i, 3, k2)
                        worksheet.write_string(i, 4, t)
                        worksheet.write_number(i, 18, bound["Age"])
                        start = time.time()
                        try:
                            log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")

                            log_count, frequent_length, violating_length, d, d_l, dict2 = \
                                annonymizer.time_dev(log, sensitive, cont, t, l, k, c, k2, bound, dict1)
                            finish1 = time.time()
                            dict1 = dict2
                            worksheet.write_number(i, 9, frequent_length)
                            worksheet.write_number(i, 10, violating_length)
                            worksheet.write_number(i, 11, d)
                            worksheet.write_number(i, 12, d_l)
                            worktime = finish1 - start
                            worksheet.write_number(i, 15, worktime)
                            log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
                            fitness, precision, perc_fit_tr, average_fitness, activ, variants, activ1 = results.results_log(
                                log_count, log)
                            worksheet.write_number(i, 5, fitness)
                            worksheet.write_number(i, 6, average_fitness)
                            worksheet.write_number(i, 7, perc_fit_tr)
                            worksheet.write_number(i, 8, precision)
                            worksheet.write_number(i, 13, variants)
                            worksheet.write_number(i, 14, activ)
                            print(activ1)
                            worksheet.write_string(i, 17, " ".join(activ1))
                            print("done")
                        except Exception as e:
                            finish1 = time.time()
                            worktime = finish1 - start
                            worksheet.write_number(i, 15, worktime)
                            worksheet.write_string(i, 16, str(repr(e)))
                            print(e)
    workbook.close()

dict1 = {l: {k: {c: {t: {bound["Age"]: {"w": [],"x": [], "v": []} for bound in contbound2} for t in spectime2} for c in C}for k in K}
             for l in range(0, L[len(L)-1])}
for l in L:
    i = 0
    workbook = xlsxwriter.Workbook('count_dev' + str(l) + '.xlsx')
    worksheet = workbook.add_worksheet("count")
    worksheet.write_string(0, 0, "L")
    worksheet.write_string(0, 1, "K")
    worksheet.write_string(0, 2, "C")
    worksheet.write_string(0, 3, "K'")
    worksheet.write_string(0, 4, "t")
    worksheet.write_string(0, 5, "fitness")
    worksheet.write_string(0, 6, "alignment fitness")
    worksheet.write_string(0, 7, "perc fit traces")
    worksheet.write_string(0, 8, "precision")
    worksheet.write_string(0, 9, "len frequent")
    worksheet.write_string(0, 10, "len violating")
    worksheet.write_string(0, 11, "deleted elements")
    worksheet.write_string(0, 12, "deleted traces")
    worksheet.write_string(0, 13, "variants")
    worksheet.write_string(0, 14, "number of activities")
    worksheet.write_string(0, 15, "time")
    worksheet.write_string(0, 16, "error")
    worksheet.write_string(0, 17, "activities")
    worksheet.write_string(0, 18, "contbound")

    for k2 in K2:
        for k in K:
            for c in C:
                for t in spectime2:
                    for bound in contbound2:
                        i += 1
                        worksheet.write_number(i, 0, l)
                        worksheet.write_number(i, 1, k)
                        worksheet.write_number(i, 2, c)
                        worksheet.write_number(i, 3, k2)
                        worksheet.write_string(i, 4, t)
                        worksheet.write_number(i, 18, bound["Age"])
                        start = time.time()
                        try:
                            log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")

                            log_count, frequent_length, violating_length, d, d_l, dict2 = \
                                annonymizer.count_dev(log, sensitive, cont, t, l, k, c, k2, bound, dict1)
                            finish1 = time.time()
                            dict1 = dict2
                            worksheet.write_number(i, 9, frequent_length)
                            worksheet.write_number(i, 10, violating_length)
                            worksheet.write_number(i, 11, d)
                            worksheet.write_number(i, 12, d_l)
                            worktime = finish1 - start
                            worksheet.write_number(i, 15, worktime)
                            log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
                            fitness, precision, perc_fit_tr, average_fitness, activ, variants, activ1 = results.results_log(
                                log_count, log)
                            worksheet.write_number(i, 5, fitness)
                            worksheet.write_number(i, 6, average_fitness)
                            worksheet.write_number(i, 7, perc_fit_tr)
                            worksheet.write_number(i, 8, precision)
                            worksheet.write_number(i, 13, variants)
                            worksheet.write_number(i, 14, activ)
                            print(activ1)
                            worksheet.write_string(i, 17, " ".join(activ1))
                            print("done")
                        except Exception as e:
                            finish1 = time.time()
                            worktime = finish1 - start
                            worksheet.write_number(i, 15, worktime)
                            worksheet.write_string(i, 16, str(repr(e)))
                            print(e)
    workbook.close()