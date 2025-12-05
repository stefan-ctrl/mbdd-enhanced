assert remove_tuple((1, 3, 5, 2, 3, 5, 1, 1, 3)) == (1, 2, 3, 5)
assert remove_tuple((2, 3, 4, 4, 5, 6, 6, 7, 8, 8)) == (2, 3, 4, 5, 6, 7, 8)
assert remove_tuple((11, 12, 13, 11, 11, 12, 14, 13)) == (11, 12, 13, 14)
