import gc
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from server_version import Results
import xlsxwriter
results = Results.Results()

workbook = xlsxwriter.Workbook('original' + '.xlsx')
worksheet = workbook.add_worksheet("original")
log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
fitness, precision, perc_fit_tr, average_fitness, activ, variants, activ1, f1_score =\
                            results.results_log(log, log)
worksheet.write_string(0, 1, "fitness")
worksheet.write_string(0, 2, "alignment fitness")
worksheet.write_string(0, 3, "perc fit traces")
worksheet.write_string(0, 4, "precision")
worksheet.write_string(0, 5, "f1-score")

worksheet.write_string(0, 6, "variants")
worksheet.write_string(0, 7, "number of activities")
i=2
worksheet.write_number(i, 1, fitness)
worksheet.write_number(i, 2, average_fitness)
worksheet.write_number(i, 3, perc_fit_tr)
worksheet.write_number(i, 4, precision)
worksheet.write_number(i, 5, f1_score)
worksheet.write_number(i, 6, variants)
worksheet.write_number(i, 7, activ)
workbook.close()