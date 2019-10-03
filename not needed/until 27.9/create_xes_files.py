import gc
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from server_version import Annonymizer
from pm4py.objects.log.exporter.xes import factory as xes_exporter

gc.collect()

annonymizer = Annonymizer.Annonymizer()

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
for l in L:
    for k2 in K2:
        for k in K:
            for c in C:
                for t in spectime2:
                    try:
                        log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")

                        log_count, frequent_length, violating_length, d, d_l, dict2 = \
                            annonymizer.set1(log, sensitive,cont,t,l,k,c,k2,dict1)
                        xes_exporter.export_log(log, "set"+ str(l)+str(k)+str(c)+".xes")
                        dict1 = dict2
                        print("done ")
                        print(str(l) + " " + str(k)+ " " + str(c))
                    except Exception as e:
                        print(e)

dict1 = {l: {k: {c: {t: {"w": [],"x": [], "v": []} for t in spectime2} for c in C}for k in K}
             for l in range(0, L[len(L)-1])}
for l in L:
    for k2 in K2:
        for k in K:
            for c in C:
                for t in spectime2:
                    try:
                        log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")

                        log_count, frequent_length, violating_length, d, d_l, dict2 = \
                            annonymizer.time2(log, sensitive,cont,t,l,k,c,k2,dict1)
                        xes_exporter.export_log(log, "time"+ str(l)+str(k)+str(c)+".xes")
                        dict1 = dict2
                        print("done ")
                        print(str(l) + " " + str(k)+ " " + str(c))
                    except Exception as e:
                        print(e)

# #set_count
dict1 = {l: {k: {c: {t: {"w": [],"x": [], "v": []} for t in spectime2} for c in C}for k in K}
             for l in range(0, L[len(L)-1])}
for l in L:
    for k2 in K2:
        for k in K:
            for c in C:
                for t in spectime2:
                    try:
                        log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")

                        log_count, frequent_length, violating_length, d, d_l, dict2 = \
                            annonymizer.set_count(log, sensitive,cont,t,l,k,c,k2,dict1)
                        xes_exporter.export_log(log, "set_count"+ str(l)+str(k)+str(c)+".xes")
                        dict1 = dict2
                        print("done ")
                        print(str(l) + " " + str(k)+ " " + str(c))
                    except Exception as e:
                        print(e)

dict1 = {l: {k: {c: {t: {"w": [],"x": [], "v": []} for t in spectime2} for c in C}for k in K}
             for l in range(0, L[len(L)-1])}
for l in L:
   for k2 in K2:
        for k in K:
            for c in C:
                for t in spectime2:
                    try:
                        log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
                        log_count, frequent_length, violating_length, d, d_l, dict2 = \
                            annonymizer.count(log, sensitive,cont,t,l,k,c,k2,dict1)

                        xes_exporter.export_log(log, "count"+ str(l)+str(k)+str(c)+".xes")
                        dict1 = dict2
                        print("done ")
                        print(str(l) + " " + str(k)+ " " + str(c))
                    except Exception as e:
                        print(e)

##set dev
dict1 = {
    l: {k: {c: {t: {bound["Age"]: {"w": [], "x": [], "v": []} for bound in contbound2} for t in spectime2} for c in C}
        for k in K}
    for l in range(0, L[len(L) - 1])}
for l in L:
    for k2 in K2:
        for k in K:
            for c in C:
                for t in spectime2:
                    for bound in contbound2:
                        try:
                            log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
                            log_count, frequent_length, violating_length, d, d_l, dict2 = \
                                annonymizer.set_dev(log, sensitive, cont, t, l, k, c, k2, bound, dict1)

                            xes_exporter.export_log(log, "set_dev" + str(l) + str(k) + str(c) + ".xes")
                            dict1 = dict2
                            print("done ")
                            print(str(l) + " " + str(k) + " " + str(c))
                        except Exception as e:
                            print(e)

##set count dev
dict1 = {
    l: {k: {c: {t: {bound["Age"]: {"w": [], "x": [], "v": []} for bound in contbound2} for t in spectime2} for c in C}
        for k in K}
    for l in range(0, L[len(L) - 1])}
for l in L:
    for k2 in K2:
        for k in K:
            for c in C:
                for t in spectime2:
                    for bound in contbound2:
                        try:
                            log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")

                            log_count, frequent_length, violating_length, d, d_l, dict2 = \
                                annonymizer.set_count_dev(log, sensitive, cont, t, l, k, c, k2, bound, dict1)

                            xes_exporter.export_log(log, "set_count_dev" + str(l) + str(k) + str(c) + ".xes")
                            dict1 = dict2
                            print("done ")
                            print(str(l) + " " + str(k) + " " + str(c))
                        except Exception as e:
                            print(e)
#
# ##time dev
dict1 = {l: {k: {c: {t: {bound["Age"]: {"w": [],"x": [], "v": []} for bound in contbound2} for t in spectime2} for c in C}for k in K}
             for l in range(0, L[len(L)-1])}
for l in L:
    for k2 in K2:
        for k in K:
            for c in C:
                for t in spectime2:
                    for bound in contbound2:
                        try:
                            log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")

                            log_count, frequent_length, violating_length, d, d_l, dict2 = \
                                annonymizer.time_dev(log, sensitive,cont,t,l,k,c,k2,bound,dict1)

                            xes_exporter.export_log(log, "time_dev" + str(l) + str(k) + str(c) + ".xes")
                            dict1 = dict2
                            print("done ")
                            print(str(l) + " " + str(k) + " " + str(c))
                        except Exception as e:
                            print(e)


##count dev
dict1 = {
    l: {k: {c: {t: {bound["Age"]: {"w": [], "x": [], "v": []} for bound in contbound2} for t in spectime2} for c in C}
        for k in K}
    for l in range(0, L[len(L) - 1])}
for l in L:
    for k2 in K2:
        for k in K:
            for c in C:
                for t in spectime2:
                    for bound in contbound2:
                        try:
                            log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")

                            log_count, frequent_length, violating_length, d, d_l, dict2 = \
                                annonymizer.count_dev(log, sensitive, cont, t, l, k, c, k2, bound, dict1)

                            xes_exporter.export_log(log, "count_dev" + str(l) + str(k) + str(c) + ".xes")
                            dict1 = dict2
                            print("done ")
                            print(str(l) + " " + str(k) + " " + str(c))
                        except Exception as e:
                            print(e)
