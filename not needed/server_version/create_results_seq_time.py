import gc
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.log.exporter.xes import factory as xes_exporter
from server_version import Annonymizer
from server_version import Results
import time
import xlsxwriter

gc.collect()

annonymizer = Annonymizer.Annonymizer()
results = Results.Results()

event_log = "Sepsis Cases - Event Log.xes"

L = [1, 3]#, 4, 8, 16]
C = [0.1, 0.6]
K = [ 20, 160]
K2 = [0.5,0.9]
sensitive = ['Age', 'Diagnose']
spectime2 = ["hours", "minutes"]
cont = ['Age']

contbound2 = [{"Age":1}]#, {"Age": 2}]

dict1 = {l: {k: {c: {t: {k2: {"w": [],"x": [], "v": []} for k2 in K2} for t in spectime2} for c in C}for k in K}
             for l in range(0,L[len(L)-1]+1)}
for l in L:
    print("Seq_time variant for l = " + str(l) + " is running...")
    i = 0
    workbook = xlsxwriter.Workbook('results/seq_time' + str(l) + '.xlsx')
    worksheet = workbook.add_worksheet("seq_time")
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
    worksheet.write_string(0, 10, "len frequent")
    worksheet.write_string(0, 11, "len violating")
    worksheet.write_string(0, 12, "deleted elements")
    worksheet.write_string(0, 13, "deleted traces")
    worksheet.write_string(0, 14, "variants")
    worksheet.write_string(0, 15, "number of activities")
    worksheet.write_string(0, 16, "activities")
    worksheet.write_string(0, 17, "time")
    worksheet.write_string(0, 18, "error")
    for k2 in K2:
        for k in K:
            for c in C:
                for t in spectime2:
                    i += 1
                    worksheet.write_number(i, 0, l)
                    worksheet.write_number(i, 1, k)
                    worksheet.write_number(i, 2, c)
                    worksheet.write_number(i, 3, k2)
                    worksheet.write_string(i, 4, t)
                    start = time.time()
                    try:
                        log = xes_import_factory.apply(event_log)

                        log_time, frequent_length_time, violating_length_time, d_time, d_l_time, dict2 = \
                            annonymizer.seq_time(log, sensitive,cont,t,l,k,c,k2,dict1)
                        finish1 = time.time()
                        xes_exporter.export_log(log_time, "xes/seq_time" + "_"  + str(l) + "_" + str(k) + "_" + str(c) + "_" + str(k2) + "_" + t  + ".xes")
                        print("seq_time" + "_" + str(l) + "_" + str(k) + "_" + str(c) + "_" + str(k2) + "_" + t + ".xes" + " has been exported!")
                        dict1 = dict2
                        worksheet.write_number(i, 10, frequent_length_time)
                        worksheet.write_number(i, 11, violating_length_time)
                        worksheet.write_number(i, 12, d_time)
                        worksheet.write_number(i, 13, d_l_time)
                        worktime_time = finish1 - start
                        worksheet.write_number(i, 17, worktime_time)
                        log = xes_import_factory.apply(event_log)
                        fitness_time, precision_time, perc_fit_tr_time, average_fitness_time, activ_time, variants_time, activ1_time, f1_score_time =\
                            results.results_log(log_time, log)
                        worksheet.write_number(i, 5, fitness_time)
                        worksheet.write_number(i, 6, average_fitness_time)
                        worksheet.write_number(i, 7, perc_fit_tr_time)
                        worksheet.write_number(i, 8, precision_time)
                        worksheet.write_number(i, 9, f1_score_time)
                        worksheet.write_number(i, 14, variants_time)
                        worksheet.write_number(i, 15, activ_time)
                        worksheet.write_string(i, 16, " ".join(activ1_time))
                    except Exception as e:
                        print(e)
                        finish1 = time.time()
                        worktime_time = finish1 - start
                        worksheet.write_number(i, 17, worktime_time)
                        worksheet.write_string(i, 18, str(repr(e)))
    workbook.close()

gc.collect()