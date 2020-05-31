from p_tlkc_privacy.privacyPreserving import privacyPreserving

event_log = "running_example.xes"

L = [2]
C = [1]
K = [1]
K2 = [0.1]
# sensitive = ['creator']
sensitive = []
T = ["minutes"]
cont = []
bk_type = "sequence" #set, multiset, sequence, relative

privacy_aware_log_dir = "xes_results"
privacy_aware_log_path = "test.xes"

pp = privacyPreserving(event_log, "example")
result = pp.apply(T, L, K, C, K2, sensitive, cont, bk_type, privacy_aware_log_dir, privacy_aware_log_path)

print(result)

