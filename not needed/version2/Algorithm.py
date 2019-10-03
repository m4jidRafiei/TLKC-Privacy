
import simplifyDeleteTracesStand5
import mvsBoxplot
import PatternMFSEvents
import TrajectoryDataAnonymizer

def anonymization(log,sensitive,spectime,cont, L,K,C,K_):

    #T are all traces
    logsimple, T = simplifyDeleteTracesStand5.simplify(log, sensitive, spectime)
    # Output: Minimal violating sequence V (T )
    violating = mvsBoxplot.mvs(T, L, K, C, sensitive, logsimple, cont)
    frequent = PatternMFSEvents.mfs(T, K_)
    sup = TrajectoryDataAnonymizer.suppression(violating, frequent)
    T_ = TrajectoryDataAnonymizer.suppressT(logsimple, sup)
    return T_
