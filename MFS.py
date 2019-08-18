import pyfpgrowth
import operator

class MFS():

    def __init__(self):
        self = self


    def frequent_variants(self, variants, counts, threshold):

        most_freq = []
        for index, count in enumerate(counts):
            if(count >= threshold ):
                most_freq.append(variants[index])

        return most_freq

    def frequent_seq_activityTime(self, T, K):
        patterns = pyfpgrowth.find_frequent_patterns(T, K)
        patterns = sorted(list(patterns.keys()), key=len)
        frequent = [patterns.pop()]
        while len(patterns) > 0:
            candidate = patterns.pop()
            super = True
            for f in frequent:
                if all(elem in f for elem in candidate):
                    super = False
                    break
            if super:
                frequent.append(candidate)
        return frequent

    def frequent_seq_activity(self, T, K):
        patterns = pyfpgrowth.find_frequent_patterns(T, K)
        patterns = sorted(list(patterns.keys()), key=len)
        frequent = [patterns.pop()]
        while len(patterns) > 0:
            candidate = patterns.pop()
            super = True
            for f in frequent:
                if all(elem in f for elem in candidate):
                    super = False
                    break
            if super:
                frequent.append(candidate)
        return frequent


