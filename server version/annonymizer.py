from ELRepresentation import ELRepresentation
from MFS import MFS
from MVS3 import MVS

def count_priv(log, sensitive,cont,t,l,k,c,k2):
    mfs = MFS()
    repres = ELRepresentation(log)
    logsimple_count, T_count, sensitives_count = repres.simplify_LKC_without_time_count(
        sensitive)
    frequent_count = mfs.frequent_seq_activity(T_count, k2 * len(T_count))
    mvs = MVS(T_count, logsimple_count, sensitive, cont, sensitives_count, True)
    violating_count = mvs.mvs(l, k, c)
    sup_count = repres.suppression(violating_count, frequent_count)
    T_count = repres.suppressT(logsimple_count, sup_count)
    log_count, d_count, d_l_count = repres.createEventLog(T_count, t)
    return log_count, len(frequent_count), len(violating_count), d_count, d_l_count

def count_dev(og, sensitive,cont,t,l,k,c,k2,contbound):
    mfs = MFS()
    log = xes_import_factory.apply("Sepsis Cases - Event Log.xes")
    repres = ELRepresentation(log)
    logsimple_count, T_count, sensitives_count = repres.simplify_LKC_without_time_count(
                sensitive)
    frequent_count = mfs.frequent_seq_activity(T_count, k2 * len(T_count))
    print("frequent count", "\n", len(frequent_count))
    mvs = MVS(T_count, logsimple_count, sensitive, cont, sensitives_count, True)
    violating_count = mvs.mvs(l, k, c,type="dev",contbound=contbound)
    print("violating count:", "\n", len(violating_count))
    sup_count = repres.suppression(violating_count, frequent_count)
    T_count = repres.suppressT(logsimple_count, sup_count)
    log_count, d_count, d_l_count = repres.createEventLog(T_count, t)
    return log_count, len(frequent_count), len(violating_count), d_count, d_l_count