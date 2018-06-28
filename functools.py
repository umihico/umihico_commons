def chunks(list_, chunk_len):
    '''
    l = list(range(10))
    print(l)
    print(chunks(l, 3))
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    '''
    return list(list_[i:i + chunk_len] for i in range(0, len(list_), chunk_len))
