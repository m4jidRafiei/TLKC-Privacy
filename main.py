from p_tlkc_privacy.privacyPreserving import privacyPreserving

event_log = "Sepsis Cases - Event Log.xes"

L = [2]
C = [0.5]
K = [20]
K2 = [0.7]
sensitive = ['Diagnose']
T = ["minutes"]
cont = []
bk_type = "sequence" #set, multiset, sequence, relative

privacy_aware_log_dir = "xes_results"

pp = privacyPreserving(event_log)
pp.apply(T, L, K, C, K2, sensitive, cont, bk_type, privacy_aware_log_dir)


