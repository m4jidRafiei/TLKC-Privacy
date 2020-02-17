from p_tlkc_privacy.privacyPreserving import privacyPreserving

event_log = "Sepsis Cases - Event Log.xes"

L = [2]
C = [1]
K = [10]
K2 = [0.5]
# sensitive = ['creator']
sensitive = []
T = ["days"]
cont = []
bk_type = "set" #set, multiset, sequence, relative

privacy_aware_log_dir = "xes_results"

pp = privacyPreserving(event_log, "sepsis")
pp.apply(T, L, K, C, K2, sensitive, cont, bk_type, privacy_aware_log_dir)

