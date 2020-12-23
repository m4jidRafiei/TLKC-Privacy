from p_tlkc_privacy.privacyPreserving import privacyPreserving
import os

event_log = "BPI_Challenge_2012_APP.xes"

L = [6]
C = [1]
K = [60]
K2 = [0.5]
sensitive = []
# sensitive = []
T = ["minutes"]
cont = []
bk_type = "relative" #set, multiset, sequence, relative

if not os.path.exists("./xes_results"):
    os.makedirs("./xes_results")

privacy_aware_log_dir = "xes_results"
privacy_aware_log_path = event_log[:-4] + " anon " + bk_type + ".xes"

pp = privacyPreserving(event_log, "Sepsis Cases")
result = pp.apply(T, L, K, C, K2, sensitive, cont, bk_type, privacy_aware_log_dir, privacy_aware_log_path)

print(result)

