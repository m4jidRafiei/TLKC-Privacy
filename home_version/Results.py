from pm4py.algo.discovery.inductive import factory as inductive_miner
from pm4py.evaluation.replay_fitness import factory as replay_factory
from pm4py.evaluation.precision import factory as precision_factory
from pm4py.statistics.traces.tracelog import case_statistics
from pm4py.evaluation.replay_fitness import factory as replay_fitness_factory
from pm4py.algo.conformance.alignments import factory as align_factory


class Results():
    def __init__(self):
        self = self

    def results_log(self, log_annon, log):
        net, initial_marking, final_marking = inductive_miner.apply(log_annon)
        fitness = replay_factory.apply(log, net, initial_marking, final_marking)["log_fitness"]
        precision = precision_factory.apply(log, net, initial_marking, final_marking)
        var_with_count = case_statistics.get_variant_statistics(log_annon)
        activ1 = {""}
        for el in var_with_count:
            el['variant'] = el['variant'].split(',')
            activ1.update(el['variant'])
        activ1.remove("")
        activ = len(activ1)
        variants = sum([1 for x in var_with_count])
        if(precision+fitness != 0):
            f1_score = 2*precision*fitness/(precision+fitness)
        else:
            f1_score = 0
        return fitness, precision, activ, variants, activ1, f1_score
