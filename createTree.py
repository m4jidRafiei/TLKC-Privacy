def createTree(list):
    #create tree with all first elements as key
    tree = {first: ({}, 0) for first in [el[0] for el in list]}
    for el in list:
        element = el.pop(0)
        tree[element][1] +=1

