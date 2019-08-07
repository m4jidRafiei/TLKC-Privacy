import pyfpgrowth


def mfs(T, K):
    patterns = pyfpgrowth.find_frequent_patterns(T,K)
    patterns = sorted(list(patterns.keys()),key=len)
    frequent = [patterns.pop()]
    while len(patterns) > 0:
        candidate = patterns.pop()
        print(len(patterns))
        super = True
        for f in frequent:
            if all(elem in f for elem in candidate):
                super = False
                break
        if super:
            frequent.append(candidate)
    return frequent