from p_tlkc_privacy.privacyPreserving import privacyPreserving

event_log = "running_example.xes"

L = [2]
C = [1]
K = [10]
K2 = [0.5]
# sensitive = ['creator']
sensitive = []
T = ["minutes"]
cont = []
bk_type = "multiset" #set, multiset, sequence, relative

privacy_aware_log_dir = "xes_results"

pp = privacyPreserving(event_log, "example")
result = pp.apply(T, L, K, C, K2, sensitive, cont, bk_type, privacy_aware_log_dir)

print(result)

