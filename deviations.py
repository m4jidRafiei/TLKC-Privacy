import numpy
#calculating for every continous sensitive attribute the standard deviation times contbound
#input: sensitivies (dict) containing for all sensitive attributes all values
#input: cont (list) all continous sensitive attributes
#input: contbound (integer)
#output: dev (dict) containing for all continious sensitive attributes the result of standard deviation times contbound
def deviations(sensitives, cont,contbound):
    dev = {}
    for c in cont:
        dev[c] = contbound[c]*numpy.std(sensitives[c])
    return dev
