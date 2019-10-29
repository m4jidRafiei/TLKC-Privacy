from typing import Tuple
import math

class TrieNode(object):
    """
    Our trie node implementation. Very basic. but does the job
    """

    def __init__(self, pair: tuple,parent=None,root_bool = False):
        self.root = root_bool
        self.pair = pair
        self.traces = []
        self.cases = []
        self.children = []
        self.parent = parent
        # Is it the last character of the word.`
        self.trace_finished = False
        # How many times this character appeared in the addition process
        self.counter = 1

    def __repr__(self, level=0):
        ret = "\t" * level + repr(self.pair) + repr(self.counter)+ "\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret

def add(root, trace: list):
    """
    Adding a word in the trie structure
    """
    node = root
    for pair in trace:
        found_in_child = False
        # Search for the character in the children of the present `node`
        for child in node.children:
            if child.pair == pair:
                # We found it, increase the counter by 1 to keep track that another
                # trace has it as well
                child.counter += 1
                child.traces.append(trace)
                # And point the node to the child that contains this char
                node = child
                found_in_child = True
                break
        # We did not find it so add a new chlid
        if not found_in_child:
            new_node = TrieNode(pair, node)
            new_node.traces.append(trace)
            node.children.append(new_node)
            # And then point node to the new child
            node = new_node
    # Everything finished. Mark it as the end of a word.
    node.trace_finished = True


def find_prefix(root, prefix: list) -> Tuple[bool, int]:
    """
    Check and return
      1. If the prefix exsists in any of the words we added so far
      2. If yes then how may words actually have the prefix
    """
    node = root
    # If the root node has no children, then return False.
    # Because it means we are trying to search in an empty trie
    if not root.children:
        return False, 0
    for pair in prefix:
        pair_not_found = True
        # Search through all the children of the present `node`
        for child in node.children:
            if child.pair == pair:
                # We found the char existing in the child.
                pair_not_found = False
                # Assign node as the child containing the char and break
                node = child
                break
        # Return False anyway when we did not find a char.
        if pair_not_found:
            return False, 0
    # Well, we are here means we have found the prefix. Return true to indicate that
    # And also the counter of the last node. This indicates how many words have this
    # prefix
    return True, node.counter

def get_leaf_nodes():
    leafs = []
    def _get_leaf_nodes(node):
        if node is not None:
            if len(node.children) == 0:
                leafs.append(node)
            for n in node.children:
                _get_leaf_nodes(n)
    _get_leaf_nodes(root)
    return leafs

def dfs(root):
    visited, stack = set(), [root]
    has_changes = False
    while stack:
        node = stack.pop()
        if node not in visited:
            if node.counter > 1:
                visited.add(node)
                stack.extend(node.children)
            elif not node.root:
                updateAncestors(root,node)
                prune(root,node)
                t_prime = []
                for trace in node.traces:
                    t_prime.append(findMostSimilar(root,node,trace))
                reconstructTree(root,t_prime)
                has_changes = True
                print(root.__repr__())
            else:
                stack.extend(node.children)
    return has_changes

def check(root):
    has_changes = True
    while has_changes:
        has_changes = dfs(root)
    return root


def updateAncestors(root,node):
    count = node.counter
    parent = node.parent
    while not parent.root:
        parent.counter -= count
        parent = parent.parent

def prune(root,node):
    parent = node.parent
    parent.children.remove(node)
    while not parent.root:
        for trace in node.traces:
            parent.traces.remove(trace)
        parent = parent.parent

def findMostSimilar(root,node,trace):
    parent = node.parent
    traces_parent = parent.traces
    dist = math.inf
    candidate = []
    for trace_candidate in traces_parent:
        dist_cand = distance(root,trace,trace_candidate)
        if dist_cand < dist:
            dist = dist_cand
            candidate = trace_candidate
    return candidate

#trace1 is problem trace2 is candidate
def distance(root, trace1, trace2):
    mismatch = 0
    i = 0
    while i < len(trace1):
        if trace1[i] != trace2[i]:
            mismatch += 1
            i += 1
            break
        else:
            i += 1
    for i2 in range(i,len(trace1)):
        mismatch += 1
    return mismatch

def reconstructTree(root,t_prime):
    for t in t_prime:
        add(root,t)

def paths(node):
    if not node.children:
        return [[node.pair]]  # one path: only contains self.value
    paths_list = []
    for child in node.children:
        for path in paths(child):
            paths_list.append([node.pair] + path)
    return paths_list

def delete_root(paths_list):
    for el in paths_list:
        if len(el) > 0 and [] in el:
            el.remove([])
    if [] in paths_list:
        paths_list.remove([])
    return paths_list

if __name__ == "__main__":
    root = TrieNode([],root_bool=True)
    add(root, [('a',1),('b',1),('a',2),('c',1)])
    add(root,  [('a',1),('b',1),('c',1)])

    print(find_prefix(root,  [('a',1),('b',1),('a',2),('c',1)]))
    print(find_prefix(root,  [('a',1),('b',1)]))
    print(find_prefix(root,  [('b',1),('a',2),('c',1)]))
    print(get_leaf_nodes())
    print(check(root))
    path_list = paths(root)
    print(delete_root(path_list))
    print(find_prefix(root, [('a', 1), ('b', 1), ('a', 2), ('c', 1)]))