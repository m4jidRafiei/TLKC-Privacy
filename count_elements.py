from pm4py.objects.log.importer.xes import factory as xes_import_factory
from ELRepresentation import ELRepresentation

event_log = "Sepsis Cases - Event Log.xes"
sensitive = ['Age', 'Diagnose']
#time
for t in ['hours','minutes', 'seconds']:
    log = xes_import_factory.apply(event_log)
    repres = ELRepresentation(log)
    logsimple, T, sensitives = repres.simplify_LKC_with_time(sensitive, t)
    flat_list = [item for sublist in T for item in sublist]
    X1 = list(set(flat_list))
    elements = len(X1)
    print(t + " has " + str(elements) + " elements")

#count
log = xes_import_factory.apply(event_log)
repres = ELRepresentation(log)
logsimple_count, T_count, sensitives_count = repres.simplify_LKC_without_time_count(
            sensitive)
flat_list = [item for sublist in T_count for item in sublist]
X1 = list(set(flat_list))
elements = len(X1)
print("seq_count" + " has " + str(elements) + " elements")

#set
log = xes_import_factory.apply(event_log)
repres = ELRepresentation(log)
logsimple_set, T_set, sensitives_set = repres.simplify_LKC_without_time_set(sensitive)
flat_list = [item for sublist in T_set for item in sublist]
X1 = list(set(flat_list))
elements = len(X1)
print("set" + " has " + str(elements) + " elements")

#set_count
log = xes_import_factory.apply(event_log)
repres = ELRepresentation(log)
logsimple_set_count, T_set_count, sensitives_set_count = repres.simplify_LKC_without_time_count_set(sensitive)
flat_list = [item for sublist in T_set_count for item in sublist]
X1 = list(set(flat_list))
elements = len(X1)
print("set_count" + " has " + str(elements) + " elements")
