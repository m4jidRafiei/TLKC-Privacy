from ELRepresentation import ELRepresentation
from MFS import MFS
from MVS import MVS
import time


class Annonymizer:

    def __init__(self):
        self = self

    def seq_count(self, log, sensitive,cont,t,l,k,c,k2,dict1):
        mfs = MFS()
        repres = ELRepresentation(log)
        logsimple_count, T_count, sensitives_count = repres.simplify_LKC_without_time_count(
            sensitive)
        frequent_count = mfs.frequent_seq_activity(T_count, k2 * len(T_count))
        freqt = time.time()
        mvs = MVS(T_count, logsimple_count, sensitive, cont, sensitives_count, True, dict_safe= dict1)
        violating_count, dict1 = mvs.mvs(l, k, c, t,k2)
        vt = time.time()
        print("violating")
        print(vt - freqt)
        violating_length = len(violating_count.copy())
        frequent_length = len(frequent_count.copy())
        sup_count = repres.suppression(violating_count, frequent_count)
        T_count = repres.suppressT(logsimple_count.copy(), sup_count)
        log_count, d_count, d_l_count = repres.createEventLog(T_count, t)
        return log_count, frequent_length, violating_length, d_count, d_l_count, dict1


    def seq_time(self, log, sensitive,cont,t,l,k,c,k2,dict1):
        mfs = MFS()
        repres = ELRepresentation(log)
        logsimple, T, sensitives = repres.simplify_LKC_with_time(sensitive, t)
        frequent_time = mfs.frequent_seq_activityTime(T, k2*len(T))
        mvs = MVS(T, logsimple, sensitive, cont, sensitives, dict_safe= dict1)
        violating_time, dict1 = mvs.mvs(l, k, c,t,k2)
        frequent_length_time = len(frequent_time.copy())
        violating_length_time = len(violating_time.copy())
        sup_time = repres.suppression(violating_time, frequent_time)
        T_time = repres.suppressT(logsimple, sup_time)
        log_time, d_time, d_l_time = repres.createEventLog(T_time, t)
        return log_time, frequent_length_time, violating_length_time, d_time, d_l_time, dict1

    def set_1(self, log, sensitive,cont,t,l,k,c,k2,dict1):
        mfs = MFS()
        repres = ELRepresentation(log)
        logsimple_set, T_set, sensitives_set = repres.simplify_LKC_without_time_set(sensitive)
        frequent_set = mfs.frequent_set_miner(T_set, k2)
        mvs = MVS(T_set, logsimple_set, sensitive, cont, sensitives_set, count=False, set1=True,dict_safe=dict1)
        violating_set,dict1 = mvs.mvs(l, k, c,t,k2)
        frequent_length_set = len(frequent_set.copy())
        violating_length_set = len(violating_set.copy())
        sup_set = repres.suppression(violating_set, frequent_set)
        log_set, d_set, d_l_set = repres.suppression2(sup_set, logsimple_set, t)
        return log_set, frequent_length_set, violating_length_set, d_set, d_l_set, dict1

    def set_count(self, log, sensitive,cont,t,l,k,c,k2,dict1):
        mfs = MFS()
        repres = ELRepresentation(log)
        logsimple_set_count, T_set_count, sensitives_set_count = repres.simplify_LKC_without_time_count_set(sensitive)
        frequent_set_count = mfs.frequent_set_miner(T_set_count, k2)
        mvs = MVS(T_set_count, logsimple_set_count, sensitive, cont, sensitives_set_count, True, True,dict_safe=dict1)
        violating_set_count, dict1 = mvs.mvs(l, k, c,t,k2)
        frequent_length_set_count = len(frequent_set_count.copy())
        violating_length_set_count = len(violating_set_count.copy())
        sup_set_count = repres.suppression(violating_set_count, frequent_set_count)
        logsimple_set_count, T_set_count, sensitives_set_count = repres.simplify_LKC_without_time_count(sensitive)
        T_set_count = repres.suppressT(logsimple_set_count, sup_set_count)
        log_set_count, d_set_count, d_l_set_count = repres.createEventLog(T_set_count, t)
        return log_set_count, frequent_length_set_count, violating_length_set_count, d_set_count, d_l_set_count, dict1
