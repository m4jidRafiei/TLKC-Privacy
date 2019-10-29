import gc
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.log.exporter.xes import factory as xes_exporter
from pm4py.statistics.traces.tracelog import case_statistics
from home_version import Annonymizer
from home_version import Results
import time
import xlsxwriter

gc.collect()

annonymizer = Annonymizer.Annonymizer()
results = Results.Results()

event_log = "Sepsis Cases - Event Log.xes"

L = [1, 2, 4, 8, 16]
C = [0.2, 0.3, 0.4, 0.5]
K = [20, 40, 80, 160]
K2 = [0.7, 0.8, 0.9]
sensitive = ['Age', 'Diagnose']
spectime2 = ["hours", "minutes"]
cont = ['Age']

for l in L:
    print("time variant for l = " + str(l) + " is running...")
    i = 1
    workbook = xlsxwriter.Workbook('results/set' + str(l) + '.xlsx')
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
    worksheet.write_string(0, 9, "f1-score")
    worksheet.write_string(0, 10, "variants")
    worksheet.write_string(0, 11, "number of activities")
    worksheet.write_string(0, 12, "activities")
    worksheet.write_string(0, 13, "error")
    for k2 in K2:
        for k in K:
            for c in C:
                worksheet.write_number(i, 0, l)
                worksheet.write_number(i, 1, k)
                worksheet.write_number(i, 2, c)
                worksheet.write_number(i, 3, k2)

                worksheet.write_number(i+1, 0, l)
                worksheet.write_number(i+1, 1, k)
                worksheet.write_number(i+1, 2, c)
                worksheet.write_number(i+1, 3, k2)
                start = time.time()
                try:
                    for t in spectime2:
                        log_new = xes_import_factory.apply(
                                                "xes/" + "seq_time" + "_" + str(l) + "_" + str(k) + "_" + str(c) + "_" + str(
                                                    k2) + "_"+ t + ".xes")
                        print("seq_time" + "_" + str(l) + "_" + str(k) + "_" + str(c) + "_" + str(
                            k2) + "_" + t + ".xes" + " has been imported!")
                        worksheet.write_string(i, 4, t)
                        log = xes_import_factory.apply(event_log)
                        fitness_set, precision_set, perc_fit_tr_set, average_fitness_set, activ_set, variants_set, activ1_set, f1_score_set =\
                            results.results_log(log_new, log)
                        worksheet.write_number(i, 5, fitness_set)
                        worksheet.write_number(i, 8, precision_set)
                        worksheet.write_number(i, 7, perc_fit_tr_set)
                        worksheet.write_number(i, 6, average_fitness_set)
                        worksheet.write_number(i, 9, f1_score_set)
                        worksheet.write_number(i, 10, variants_set)
                        worksheet.write_number(i, 11, activ_set)
                        worksheet.write_string(i, 12, " ".join(activ1_set))
                        i += 1
                except Exception as e:
                    print(e)
                    worksheet.write_string(i, 13, str(repr(e)))
                    i += 1
    workbook.close()
    gc.collect()