from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.log.exporter.xes import factory as xes_exporter
from TLKC import Annonymizer
import time


event_log = "Sepsis Cases - Event Log.xes"

# L = [1, 2, 4, 8, 16]
# C = [0.2, 0.3, 0.4, 0.5]
# K = [20, 40, 80, 160]
# K2 = [0.7, 0.8, 0.9]
# sensitive = ['Age', 'Diagnose']
# spectime2 = ["hours", "minutes"]
# cont = ['Age']

L = [2]
C = [0.5]
K = [20]
K2 = [0.7]
sensitive = ['Diagnose']
spectime2 = ["minutes"]
cont = []
bk_type = "relative" #set, multiset, sequence, relative


if bk_type == "relative":
    dict1 = {l: {k: {c: {t: {k2: {"w": [], "x": [], "v": []} for k2 in K2} for t in spectime2} for c in C} for k in K}
             for l in range(0, L[len(L) - 1] + 1)}
else:
    dict1 = {l: {k: {c: {k2: {"w": [],"x": [], "v": []} for k2 in K2} for c in C}for k in K}
             for l in range(0,L[len(L)-1]+1)}


annonymizer = Annonymizer.Annonymizer()
log = xes_import_factory.apply(event_log)

for l in L:
    print("Set variant for l = " + str(l) + " is running...")
    for k2 in K2:
        for k in K:
            for c in C:
                try:
                    if bk_type == "set":
                        log2 = {t: None for t in spectime2}
                        for t in spectime2:
                            log2[t] = xes_import_factory.apply(event_log)

                        log_set, frequent_length_set, violating_length_set, d_set, d_l_set, dict2 = \
                            annonymizer.set_1(log, log2, sensitive,cont,l,k,c,k2,dict1,spectime2)
                        dict1 = dict2
                        for t in spectime2:
                            xes_exporter.export_log(log_set[t],
                                                    "xes/" + "set" + "_" + str(l) + "_" + str(k) + "_" + str(c) + "_" + str(
                                                        k2) + "_"+ t + ".xes")
                            print("set" + "_" + str(l) + "_" + str(k) + "_" + str(c) + "_" + str(
                                k2) + "_" + t + ".xes" + " has been exported!")
                    elif bk_type == "multiset":
                        log2 = {t: None for t in spectime2}
                        for t in spectime2:
                            log2[t] = xes_import_factory.apply(event_log)
                        log_set_count, frequent_length_set_count, violating_length_set_count, d_set_count, d_l_set_count, dict2 = \
                            annonymizer.set_count(log, log2, sensitive, cont, l, k, c, k2, dict1, spectime2)
                        dict1 = dict2
                        for t in spectime2:
                            xes_exporter.export_log(log_set_count[t],
                                                    "xes/multiset" + "_" + str(l) + "_" + str(k) + "_" + str(
                                                        c) + "_" + str(k2) + "_" + t + ".xes")
                            print("multiset" + "_" + str(l) + "_" + str(k) + "_" + str(c) + "_" + str(
                                k2) + "_" + t + ".xes" + " has been exported!")
                    elif bk_type == "sequence":
                        log2 = {t: None for t in spectime2}
                        for t in spectime2:
                            log2[t] = xes_import_factory.apply(event_log)

                        log_seq_count, frequent_length_seq_count, violating_length_seq_count, d_seq_count, d_l_seq_count, dict2 = \
                            annonymizer.seq_count(log, log2, sensitive, cont, l, k, c, k2, dict1, spectime2)
                        dict1 = dict2
                        for t in spectime2:
                            xes_exporter.export_log(log_seq_count[t],
                                                    "xes/sequence" + "_" + str(l) + "_" + str(k) + "_" + str(
                                                        c) + "_" + str(k2) + "_" + t + ".xes")
                            print("sequence" + "_" + str(l) + "_" + str(k) + "_" + str(c) + "_" + str(
                                k2) + "_" + t + ".xes" + " has been exported!")
                    elif bk_type == "relative":
                        for t in spectime2:
                            log_time, frequent_length_time, violating_length_time, d_time, d_l_time, dict2 = \
                                annonymizer.seq_time(log, sensitive, cont, t, l, k, c, k2, dict1)
                            xes_exporter.export_log(log_time,
                                                    "xes/relative" + "_" + str(l) + "_" + str(k) + "_" + str(c) + "_" + str(
                                                        k2) + "_" + t + ".xes")
                            print("relative" + "_" + str(l) + "_" + str(k) + "_" + str(c) + "_" + str(
                                k2) + "_" + t + ".xes" + " has been exported!")
                            dict1 = dict2
                except Exception as e:
                    print(e)