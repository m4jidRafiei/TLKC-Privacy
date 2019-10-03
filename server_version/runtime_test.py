import gc
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from server_version import Annonymizer
import time
import xlsxwriter

gc.collect()

annonymizer = Annonymizer.Annonymizer()

event_log = "Sepsis Cases - Event Log.xes"

L = [1, 2]
C = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
K = [20, 40, 80, 160]
K2 = [0.5, 0.6, 0.7, 0.8, 0.9]
sensitive = ['Age', 'Diagnose']
spectime2 = ["hours", "minutes"]
cont = ['Age']

contbound2 = [{"Age":1}]#, {"Age": 2}]
dict1 = {l: {k: {c: {t: {k2: {"w": [],"x": [], "v": []} for k2 in K2} for t in spectime2} for c in C}for k in K}
             for l in range(0,L[len(L)-1]+1)}
for l in L:
    print("Seq_count variant for l = " + str(l) + " is running...")
    i = 0
    for k2 in K2:
        for k in K:
            for c in C:
                for t in spectime2:
                    i += 1
                    start = time.time()
                    # try:
                    log = xes_import_factory.apply(event_log)
                    log_seq_count, frequent_length_seq_count, violating_length_seq_count, d_seq_count, d_l_seq_count, dict2 = \
                        annonymizer.seq_count(log, sensitive,cont,t,l,k,c,k2,dict1)
                    finish1 = time.time()
                    dict1 = dict2
                    runtime =  finish1 - start
                    print("seq_count" + "_" + str(l) + "_" + str(k) + "_" + str(c) + "_" + str(k2) + ":" + str(runtime))
gc.collect()

