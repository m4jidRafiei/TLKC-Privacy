from p_tlkc_privacy.privacyPreserving import privacyPreserving

event_log = "Sepsis Cases - Event Log.xes"

L = [6]
C = [1]
K = [100]
K2 = [0.5]
# sensitive = ['creator']
sensitive = []
T = ["seconds"]
cont = []
bk_type = "sequence" #set, multiset, sequence, relative

privacy_aware_log_dir = "xes_results"
privacy_aware_log_path = "Sepsis Cases - Event Log - anon.xes"

pp = privacyPreserving(event_log, "Sepsis Cases")
result = pp.apply(T, L, K, C, K2, sensitive, cont, bk_type, privacy_aware_log_dir, privacy_aware_log_path)

print(result)

