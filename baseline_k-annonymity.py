from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.log.exporter.xes import factory as xes_exporter
from pm4py.statistics.traces.tracelog import case_statistics
from pm4py.algo.filtering.tracelog.variants import variants_filter
event_log = "Sepsis Cases - Event Log.xes"

K2 = [0.7, 0.8, 0.9]
for k in K2:
    log = xes_import_factory.apply(event_log)
    var_with_count = case_statistics.get_variant_statistics(log)
    variants_count = sorted(var_with_count, key=lambda x: x['count'], reverse=False)
    to_filter = []
    print(variants_count)
    for j in range(0, len(variants_count)):
        dict = variants_count[j]
        if dict["count"] < k*len(log):
            to_filter.append([dict["variant"]])
    for fil in to_filter:
        log = variants_filter.apply(log, fil)
    xes_exporter.export_log(log, "xes/baseline" + "_" + str(k) + "-" + "Annonymity" + ".xes")
    print("xes/baseline" + "_" + str(k) + "-" + "Annonymity" + ".xes" + " has been exported!")