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
K = [20, 160]
K2 = [0.5, 0.9]
sensitive = ['Age', 'Diagnose']
spectime2 = ["hours"]#, "minutes"]
cont = ['Age']

contbound2 = [{"Age":1}]#, {"Age": 2}]
dict1 = {l: {k: {c: {t: {k2: {"w": [],"x": [], "v": []} for k2 in K2} for t in spectime2} for c in C}for k in K}
             for l in range(0,L[len(L)-1]+1)}
for l in L:
    print("Seq_count variant for l = " + str(l) + " is running...")
    i = 0
    workbook = xlsxwriter.Workbook('results/seq_count' + str(l) + '.xlsx')
    worksheet = workbook.add_worksheet("seq_count")
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
                        log_seq_count, frequent_length_seq_count, violating_length_seq_count, d_seq_count, d_l_seq_count, dict2 = \
                            annonymizer.seq_count(log, sensitive,cont,t,l,k,c,k2,dict1)
                        finish1 = time.time()
                        dict1 = dict2
                        xes_exporter.export_log(log_seq_count,
                                                "xes/seq_count" + "_" + str(l) + "_" + str(k) + "_" + str(c) + "_" + str(k2) + "_" + t  + ".xes")
                        print("seq_count" + "_" + str(l) + "_" + str(k) + "_" + str(c) + "_" + str(k2) + "_" + t  + ".xes" + " has been exported!" )
                        worksheet.write_number(i, 10, frequent_length_seq_count)
                        worksheet.write_number(i, 11, violating_length_seq_count)
                        worksheet.write_number(i, 12, d_seq_count)
                        worksheet.write_number(i, 13, d_l_seq_count)
                        worktime_seq_count = finish1 - start
                        worksheet.write_number(i, 17, worktime_seq_count)
                        log = xes_import_factory.apply(event_log)
                        fitness_seq_count, precision_seq_count, perc_fit_tr_seq_count, average_fitness_seq_count, activ_seq_count, variants_seq_count, activ1_seq_count, f1_score_seq_count =\
                            results.results_log(log_seq_count, log)
                        worksheet.write_number(i, 5, fitness_seq_count)
                        worksheet.write_number(i, 6, average_fitness_seq_count)
                        worksheet.write_number(i, 7, perc_fit_tr_seq_count)
                        worksheet.write_number(i, 8, precision_seq_count)
                        worksheet.write_number(i, 9, f1_score_seq_count)
                        worksheet.write_number(i, 14, variants_seq_count)
                        worksheet.write_number(i, 15, activ_seq_count)
                        worksheet.write_string(i, 16, " ".join(activ1_seq_count))
                    except Exception as e:
                        print(e)
                        finish1 = time.time()
                        worktime_seq_count = finish1 - start
                        worksheet.write_number(i, 17, worktime_seq_count)
                        worksheet.write_string(i, 18, str(repr(e)))
    workbook.close()
gc.collect()

