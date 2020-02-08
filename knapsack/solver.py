#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])
items = []

def Branch_and_Bound(K, n, j, tmp, w, best_value, best_taken, est):
    '''
    Basically DFS + pruning
    K: capacity
    n: item_count
    j: current # iterated item
    tmp: template of taken
    w: current weight
    best_value: best value
    best_taken: the combination that leads to the best value
    est: optimistic estimation
    '''

    if j == n:
        value = 0
        for idx, item in enumerate(items):
            value += item.value * tmp[idx]
        # print(tmp, value, w, est)
        if value > best_value:
            best_value = value
            best_taken = tmp[:]
        return (best_value, best_taken)

    for val in (1, 0):
        tmp[j] = val
        w_ = w + val * items[j].weight
        if w_ <= K:
            est_ = est - (1 - val) * items[j].value
            if est_ >= best_value:
                best_value, best_taken = Branch_and_Bound(
                    K, n, j+1, tmp, w_, best_value, best_taken, est_)

    return best_value, best_taken

def DP(K, j, taken):
    '''
    Input
        K: capcacity
        j: item[0,...,j] are available
    Output
        (value, taken)
    '''
    item = items[j]

    if j > 0:
        if item.weight > K:
            taken_cp = taken[:]
            val, taken_cp = DP(K, j-1, taken_cp)
            taken = [*taken_cp]
            return (val, taken)
        else:
            taken_cp1 = taken[:]
            taken_cp2 = taken[:]

            not_take, taken_cp1 = DP(K, j-1, taken_cp1)

            taken_cp2[j] = 1
            val, taken_cp2 = DP(K-item.weight, j-1, taken_cp2)
            take = item.value + val

            taken = taken_cp1[:] if not_take > take else taken_cp2[:]
            return (max(not_take, take), taken)
    else:
        if item.weight > K:
            taken[j] = 0
            return (0, taken)
        else:
            taken[j] = 1
            return (item.value, taken)

def Linear_Relaxation(capacity, items, tmp=None):
    weight = 0
    value = 0
    taken = [0]*len(items)
    items_ = sorted(items, reverse=True, key=lambda item: item.value/item.weight)

    for item in items_:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
        else:
            taken[item.index] = (capacity - weight) / item.weight
            value += taken[item.index] * item.value
            return (value, taken)

def Greedy(capacity, taken, mode=0):
    '''
    mode 0: take until it is full
    mode 1: sorted by the value-weight ratio first and do mode 1
    '''
    
    value = 0
    weight = 0
    if mode == 1:
        items.sort(reverse=True, key=lambda item: item.value/item.weight) # in-place, descending order
        # for item in items:
        #     print(item.value/item.weight)

    # mode 0
    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight

    return (value, taken)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items.clear() # Remember to clean the global variable

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    taken = [0]*len(items)
    opt = 0

    if item_count <= 45:
        tmp = [0]*len(items)
        best_taken = [0]*len(items)
        est = 0

        for _, item in enumerate(items):
            est += item.value

        est, est_taken = Linear_Relaxation(capacity, items, tmp=None) # Linear relaxation as estimation
        print(est, est_taken)
        value, taken = Branch_and_Bound(capacity, item_count, 0, tmp, 0, -1, best_taken, est)
        opt = 1
    elif item_count <= 40:
        value, taken = DP(capacity, item_count-1, taken)
        opt = 1
    else:
        value, taken = Greedy(capacity, taken, mode=1)
        opt = 0
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(opt) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        import time
        t0 = time.time()
        print(solve_it(input_data))
        t1  = time.time()
        print('Time elapsed: {:.3f}s'.format(t1-t0))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

