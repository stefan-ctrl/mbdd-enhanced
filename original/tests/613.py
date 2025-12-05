assert maximum_value([('key1', [3, 4, 5]), ('key2', [1, 4, 2]), ('key3', [9, 3])]) == [('key1', 5), ('key2', 4), ('key3', 9)]
assert maximum_value([('key1', [4, 5, 6]), ('key2', [2, 5, 3]), ('key3', [10, 4])]) == [('key1', 6), ('key2', 5), ('key3', 10)]
assert maximum_value([('key1', [5, 6, 7]), ('key2', [3, 6, 4]), ('key3', [11, 5])]) == [('key1', 7), ('key2', 6), ('key3', 11)]
