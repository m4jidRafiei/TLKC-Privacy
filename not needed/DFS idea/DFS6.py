def dfs(c1,K,path,visited,el_traces,frequent, candidates,parent,frequent_cache):
    visited[tuple(c1)] = True
    path.append(c1)
    # If current vertex is same as destination, then print
    # current path[]
    if len(c1) == 1:
        key = c1[0]
    else:
        key = tuple(c1)
    if len(path) == 1:
        freq = len([tr for tr in el_traces[key]])
    elif len(path) == 2:
        el_traces[tuple(path)] = [tr for tr in el_traces[key] if tr in el_traces[tuple(path[0:1][0])]]
        freqalt = len(el_traces[tuple(path[0:1][0])])
        freq = len(el_traces[tuple(path)])
        if freqalt == freq:
            parent.append(False)
    else:
        el_traces[tuple(path)] = [tr for tr in el_traces[tuple(c1)] if tr in el_traces[tuple(path[0:len(path)-1])]]
        freqalt = len(el_traces[tuple(path[0:len(path)][0])])
        freq = len(el_traces[tuple(path)])
        if freqalt == freq:
            parent.append(False)
    if freq < K:
        no_super = True
        for f in frequent:
            if all(elem in f for elem in path[0:len(path)-1]):
                no_super = False
                break
        if no_super:
            frequent_cache.append(path[0:len(path)-1])
            print(path[0:len(path)-1])
            print(parent)
    else:
        # If current vertex is not destination
        # Recur for all the vertices adjacent to this vertex
        for i in candidates:
            if visited[tuple(i)] == False and path[len(path)-1][1] <= i[1] and i not in path:
                dfs(i, K, path, visited, el_traces, frequent, [c for c in candidates if i != c and path[len(path)-1][1] <= i[1]], parent)
                if not parent:
                    break
                    parent.pop()
    # Remove current vertex from path[] and mark it as unvisited
    path.pop()
    visited[tuple(c1)] = False
    return frequent, el_traces